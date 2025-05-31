import torch
import os
import clip
import itertools
from PIL import Image

def text_query_keyframes(text, images, image_files, model, device):
    query = clip.tokenize([text]).to(device)

    with torch.no_grad():
        images_tensor = torch.cat(images) # transform la list en Tensor
        images_features = model.encode_image(images_tensor)
        text_features = model.encode_text(query)

    # Normalisation pour similarité cosine
    images_features /= images_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)

    # Calcul similarités
    similarities = (images_features @ text_features.T).squeeze(1)
    values, indices = similarities.topk(5)

    # Affichage des résultats
    print(f"\nTop 5 images pour la requête : {text} \n")
    for i, idx in enumerate(indices):
        filename = image_files[idx]
        score = values[i].item()
        print(f"{i+1}. {filename} — Similarité : {score:.4f}")


def image_similarity(imageFile, images, image_files, model, device, preprocess) : 
    image = preprocess(Image.open(imageFile)).unsqueeze(0).to(device)
    with torch.no_grad():
        images_tensor = torch.cat(images) # transform la list en Tensor
        images_features = model.encode_image(images_tensor)
        image_features =  model.encode_image(image)

    images_features /= images_features.norm(dim=-1, keepdim=True)
    image_features /= image_features.norm(dim=-1, keepdim=True)

    # Calcul similarités
    similarities = (images_features @ image_features.T).squeeze(1)
    values, indices = similarities.topk(5)

    # Affichage des résultats
    print(f"\nTop 5 images pour la requête : {imageFile} \n")
    for i, idx in enumerate(indices):
        filename = image_files[idx]
        score = values[i].item()
        print(f"{i+1}. {filename} — Similarité : {score:.4f}")
    
def embedding(imageFile, preprocess, device, model) : 
    image = preprocess(Image.open(imageFile)).unsqueeze(0).to(device)
    image_embeddings = model.encode_image(image)
    print(image_embeddings)
    return image_embeddings

def main() : 
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)

    folder_path = "keyframes_test"
    images = []
    image_files = []

    for filename in os.listdir(folder_path):
        imageFile = os.path.join(folder_path, filename)
        image = preprocess(Image.open(imageFile)).unsqueeze(0).to(device)
        images.append(image)
        image_files.append(filename)
    
    #text_query_keyframes("a planet with black and white stripes", images, image_files, model, device)
    #image_similarity("keyframes_test/keyframe_shot_003419.jpg", images, image_files, model, device, preprocess)
    embedding("keyframes_test/keyframe_shot_003419.jpg", preprocess, device, model)

if __name__ == "__main__":
    main()
