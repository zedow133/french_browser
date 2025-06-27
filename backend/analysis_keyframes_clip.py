import torch
import os
import clip
from tqdm import tqdm
import itertools
from PIL import Image

def init():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    return device, model, preprocess

def text_query_keyframes(text, images_embeddings, images_names, k, model, device):
    query = clip.tokenize([text]).to(device)

    with torch.no_grad():
        text_features = model.encode_text(query)

    # Normalization for cosine similarity
    images_embeddings /= images_embeddings.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)

    # Similarity computation
    similarities = (images_embeddings @ text_features.T).squeeze(1)
    values, indexes = similarities.topk(k)

    # Results display (for logging and debugging purpose)
    top_k=[]
    print(f"\nTop {k} images for the request : {text} \n")
    for i, idx in enumerate(indexes):
        filename = images_names[idx]
        top_k.append(filename)
        score = values[i].item()
        print(f"{i+1}. {filename} — Similarity : {score:.4f}")

    return top_k

def image_similarity(image_embedding, images_embeddings, images_names, k) : 
    # Normalization for cosine similarity
    images_embeddings /= images_embeddings.norm(dim=-1, keepdim=True)
    image_embedding /= image_embedding.norm(dim=-1, keepdim=True)

    # Similarity computation
    similarities = (images_embeddings @ image_embedding.T).squeeze(1)
    values, indices = similarities.topk(k+1)

    # Results display (for logging and debugging purpose)
    top_k=[]
    print(f"\nTop {k} similar images : \n")
    for i, idx in enumerate(indices):
        if i != 0:
            filename = images_names[idx]
            top_k.append(filename)
            score = values[i].item()
            print(f"{i+1}. {filename} — Similarity : {score:.4f}")
        
    return top_k
    
def single_embedding(imageFile, preprocess, device, model) : 
    image = preprocess(Image.open(imageFile)).unsqueeze(0).to(device)
    image_embeddings = model.encode_image(image)
    return image_embeddings