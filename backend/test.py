from util_db import ShotsDatabase
import pickle
import torch
import os
from analysis_keyframes_clip import init as clip_init, search

db = ShotsDatabase("./db")

images_embeddings = torch.load('./db/all_keyframes_embeddings.pt')
with open('./db/all_keyframes_names.pkl', 'rb') as f:
    images_names = pickle.load(f)

device, model, preprocess = clip_init()

top_k=search("a girl", images_embeddings, images_names, 5, model, device)

print(top_k)