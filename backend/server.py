from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from util_db import ShotsDatabase
import uvicorn
from fastapi.staticfiles import StaticFiles

from analysis_keyframes_clip import init as clip_init, text_query_keyframes, image_similarity
from torch import load as torch_load
import pickle

app = FastAPI(
    title="French Browser API",
    description="API for French Browser system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB, model and data init
db = ShotsDatabase("./db")
device, model, preprocess = clip_init()

images_embeddings = torch_load('./db/all_keyframes_embeddings.pt')
with open('./db/all_keyframes_names.pkl', 'rb') as f:
    images_names = pickle.load(f)

app.mount("/media/shots", StaticFiles(directory="db/data"))
app.mount("/media/videos", StaticFiles(directory="videos"))

@app.get("/api/")
async def root():
    """Root of the API"""
    return {"message": "API french_browser - alive"}

class ShotResponse(BaseModel):
    keyframe_name: str
    start_stamp: int
    end_stamp: int

@app.get("/api/get_shot/{keyframe_name}", response_model=ShotResponse)
async def get_shot(keyframe_name: str):
    """Get a shot by its ID"""
    shot = db.get_shot(keyframe_name)
    if not shot:
        raise HTTPException(status_code=404, detail="Shot not found")
    return shot

@app.get("/api/search/text/")
async def search_text(query: str = Query()):
    """Perform similarity search, given a text query to find similar images"""
    top_k = text_query_keyframes(query, images_embeddings, images_names, 20, model, device)
    return top_k

@app.get("/api/search/similarity/")
async def search_similarity(keyframe_name: str):
    """Perform similarity search, given an image query to find similar images"""
    found, keyframe_embedding = db.get_embedding(keyframe_name)
    if not found:
        raise HTTPException(status_code=404, detail="Shot not found")
    top_k = image_similarity(keyframe_embedding, images_embeddings, images_names, 20)
    return top_k

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )