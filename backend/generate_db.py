import os
import sys
from pathlib import Path
import torch
import pickle
from transnetv2 import TransNetV2

from shot_extraction import get_video_fps, detect_shots_with_transnet, extract_keyframe, extract_video_clip
from analysis_keyframes_clip import init as clip_init, single_embedding, all_embeddings
from util_db import ShotsDatabase

def process_single_video(video_path, transnet_model, clip_model, preprocess, device, db, data_dir):
    video_name = Path(video_path).stem
    print(f"NAME: {video_name}")
    print(f"{'='*60}")
    
    video_output_dir = os.path.join(data_dir, video_name)
    keyframes_dir = os.path.join(video_output_dir, "keyframes")
    clips_dir = os.path.join(video_output_dir, "clips")
    timestamps_dir = os.path.join(video_output_dir, "timestamps")
    
    os.makedirs(keyframes_dir, exist_ok=True)
    os.makedirs(clips_dir, exist_ok=True)
    os.makedirs(timestamps_dir, exist_ok=True)
    
    fps = get_video_fps(video_path)
    
    shots = detect_shots_with_transnet(video_path, transnet_model)
    
    for i, (start_frame, end_frame) in enumerate(shots, 1):
        print(f"    SHOT PROGRESSION {i}/{len(shots)}: frames {start_frame}-{end_frame}")
        
        shot_id = video_name + '_' + str(i)

        keyframe_filename = f"{shot_id}.jpg"
        keyframe_path = os.path.join(keyframes_dir, keyframe_filename)
        extract_keyframe(video_path, start_frame, end_frame, fps, keyframe_path)

        clip_filename = f"{shot_id}.mp4"
        clip_path = os.path.join(clips_dir, clip_filename)
        extract_video_clip(video_path, start_frame, end_frame, fps, clip_path)

        image_embedding = single_embedding(keyframe_path, preprocess, device, clip_model)

        db.insert_shot(
            shot_id = shot_id,
            source = video_name,
            start_stamp = round((start_frame / fps) * 1000),
            end_stamp = round((end_frame / fps) * 1000),
            embedding = image_embedding
        )

def main():
    #Arguments parsing
    if len(sys.argv) not in [2, 3]:
        print("Usage: python generate_db.py <video_directory> [db_directory}")
        print("Example: python generate_db.py ./videos ./db")
        sys.exit(1)
    
    #Directories checking
    input_dir = sys.argv[1]
    db_dir = sys.argv[2] if len(sys.argv) == 3 else "./db"
    
    if not os.path.exists(input_dir) or not os.path.isdir(input_dir):
        print(f"Input folder not found: {input_dir}")
        sys.exit(1)
    
    #Video files fetching
    video_files = [str(file_path) for file_path in Path(input_dir).rglob('*')]
    
    if not video_files:
        print(f"No video file found in: {input_dir}")
        sys.exit(1)

    #Folders creation
    os.makedirs(db_dir, exist_ok=True)

    data_dir = os.path.join(db_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    #Database creation
    db = ShotsDatabase(db_dir)

    # Models loading
    try:
        transnet_model = TransNetV2()
    except Exception as e:
        print(f"TransNetV2 loading failed: {e}")
        sys.exit(1)

    device, clip_model, preprocess = clip_init()
    
    #Videos processing
    for i, video_file in enumerate(video_files, 1):
        print(f"{'='*60}")
        print(f"VIDEO PROGRESSION: {i}/{len(video_files)}")
        process_single_video(video_file, transnet_model, clip_model, preprocess, device, db, data_dir)

    #All keyframes embedding
    keyframes_paths = []
    keyframes_names = []

    for source_name in os.listdir(data_dir):
        source_dir = os.path.join(data_dir, source_name)
        keyframe_dir = os.path.join(source_dir, 'keyframes')
        for keyframe_name in os.listdir(keyframe_dir):
            keyframes_names.append(keyframe_name[:-4])
            keyframe_path = os.path.join(keyframe_dir, keyframe_name)
            keyframes_paths.append(keyframe_path)
    
    all_keyframes_embeddings = all_embeddings(keyframes_paths, preprocess, device, clip_model)

    torch.save(all_keyframes_embeddings, os.path.join(db_dir, 'all_keyframes_embeddings.pt'))

    with open(os.path.join(db_dir, 'all_keyframes_names.pkl'), 'wb') as f:
        pickle.dump(keyframes_names, f)

if __name__ == "__main__":
    main()