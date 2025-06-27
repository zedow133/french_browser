import os
import sys
from pathlib import Path
import torch
import tempfile
import pickle
from transnetv2 import TransNetV2

from shot_extraction import get_video_fps, detect_shots_with_transnet, extract_keyframes, extract_video_clip
from analysis_keyframes_clip import init as clip_init
from util_db import ShotsDatabase

def process_single_video(video_path, transnet_model, clip_model, preprocess, device, db, data_dir):
    video_name = Path(video_path).stem
    print(f"NAME: {video_name}")
    print(f"{'='*60}")
    
    # Create video directories
    video_output_dir = os.path.join(data_dir, video_name)
    keyframes_dir = os.path.join(video_output_dir, "keyframes")
    clips_dir = os.path.join(video_output_dir, "clips")
    
    os.makedirs(keyframes_dir, exist_ok=True)
    os.makedirs(clips_dir, exist_ok=True)
    
    # Detect shots using TransnetV2
    shots = detect_shots_with_transnet(video_path, transnet_model)

    # Get video FPS
    fps = get_video_fps(video_path)

    # Process all the shots of the video
    for i, (start_frame, end_frame) in enumerate(shots, 1):
        print(f"    SHOT PROGRESSION {i}/{len(shots)}: frames {start_frame}-{end_frame}")
        
        shot_id = video_name + '_' + str(i)

        # Save video clip of the shot in the clips folder of the video
        clip_filename = f"{shot_id}.mp4"
        clip_path = os.path.join(clips_dir, clip_filename)
        extract_video_clip(video_path, start_frame, end_frame, fps, clip_path)

        # Extract several keyframes of the shot and save them in the keyframes folder of the video
        shot_keyframes_names, shot_keyframes_embeddings = extract_keyframes(video_path, start_frame, end_frame, fps, keyframes_dir, shot_id, 10, device, clip_model, preprocess)

        # Insert given keyframes in the database
        for j in range(len(shot_keyframes_names)):
            db.insert_shot(
                keyframe_name = shot_keyframes_names[j],
                start_stamp = round((start_frame / fps) * 1000),
                end_stamp = round((end_frame / fps) * 1000),
                embedding = shot_keyframes_embeddings[j]
            )

def main():
    # Arguments parsing
    if len(sys.argv) != 2:
        print("Usage: python generate_db.py <video_directory>")
        print("Example: python generate_db.py ./videos")
        sys.exit(1)
    
    # Directories checking
    input_dir = sys.argv[1]
    
    if not os.path.exists(input_dir) or not os.path.isdir(input_dir):
        print(f"Input folder not found: {input_dir}")
        sys.exit(1)
    
    # Video files fetching
    video_files = [str(file_path) for file_path in Path(input_dir).rglob('*')]
    
    if not video_files:
        print(f"No video file found in: {input_dir}")
        sys.exit(1)

    # Database creation
    db_dir = "./db"
    os.makedirs(db_dir, exist_ok=True)

    data_dir = os.path.join(db_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    db = ShotsDatabase(db_dir)

    # Models loading
    transnet_model = TransNetV2()
    device, clip_model, preprocess = clip_init()

    # Videos processing
    for i, video_file in enumerate(video_files, 1):
        print(f"{'='*60}")
        print(f"VIDEO PROGRESSION: {i}/{len(video_files)}")
        process_single_video(video_file, transnet_model, clip_model, preprocess, device, db, data_dir)

    # All keyframes embedding
    all_keyframes_names, all_keyframes_embeddings = db.get_all_embeddings()

    with open(os.path.join(db_dir, 'all_keyframes_names.pkl'), 'wb') as f:
        pickle.dump(all_keyframes_names, f)

    with torch.no_grad():
        all_keyframes_embeddings = torch.cat(all_keyframes_embeddings)
        torch.save(all_keyframes_embeddings, os.path.join(db_dir, 'all_keyframes_embeddings.pt'))

if __name__ == "__main__":
    main()