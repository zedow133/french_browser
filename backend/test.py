from analysis_keyframes_clip import init as clip_init
from PIL import Image
import torch

device, clip_model, preprocess = clip_init()

image_paths = ['./db/data/00001/keyframes/00001_5_0.jpg', './db/data/00001/keyframes/00001_6_0.jpg']

preprocessed_images = []

for image_path in image_paths:
    preprocessed_image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    preprocessed_images.append(preprocessed_image)

with torch.no_grad():
    all_images_tensor = torch.cat(preprocessed_images)
    all_images_features = clip_model.encode_image(all_images_tensor)

separate_images_features = []
with torch.no_grad():
    for preprocessed_image in preprocessed_images:
        separate_images_feature = clip_model.encode_image(preprocessed_image)
        separate_images_features.append(separate_images_feature)
    separate_images_features = torch.cat(separate_images_features)

# print(all_images_features.detach().numpy()[0])
# print(separate_images_features)

dist = torch.sqrt(torch.sum(torch.pow(torch.subtract(all_images_features, separate_images_features), 2), dim=0))
print(dist)