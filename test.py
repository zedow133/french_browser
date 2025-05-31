from util_db import ShotsDatabase
import torch
import clip
from analysis_keyframes_clip import embedding, tensor_similarity

db = ShotsDatabase("./db")
# device = "cuda" if torch.cuda.is_available() else "cpu"
# model, preprocess = clip.load("ViT-B/32", device=device)
# tensor_similarity(db.get_shot("00179_1")['embedding'], embedding("./db/data/00179/keyframes/00179_2.jpg", preprocess, device, model))
print(db.get_shot("00179_1"))