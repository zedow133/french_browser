import ffmpeg
import os
import sys
from pathlib import Path
from transnetv2 import TransNetV2

def get_video_fps(video_path):
    probe = ffmpeg.probe(video_path, select_streams='v:0')
    fps_str = probe['streams'][0]['r_frame_rate']
    if '/' in fps_str:
        num, den = fps_str.split('/')
        fps = float(num) / float(den)
    else:
        fps = float(fps_str)
    return fps

def extract_keyframe(video_path, start_frame, end_frame, fps, output_path):
    timestamp = ((start_frame + end_frame) // 2) / fps
    
    (
        ffmpeg
        .input(video_path, ss=timestamp)
        .output(output_path, vframes=1, **{'q:v': 2})
        .overwrite_output()
        .run(quiet=True)
    )

def extract_video_clip(video_path, start_frame, end_frame, fps, output_path):
    start_timestamp = start_frame / fps
    duration_frames = end_frame - start_frame + 1
    duration_seconds = duration_frames / fps
    
    (
        ffmpeg
        .input(video_path, ss=start_timestamp, t=duration_seconds)
        .output(
            output_path,
            vcodec='libx264',
            acodec='aac',
            preset='medium',
            crf=23
        )
        .overwrite_output()
        .run(quiet=True)
    )

def save_timestamps_file(output_path, start_frame, end_frame, fps):
    start_timestamp = round((start_frame / fps) * 1000)
    end_timestamp = round((end_frame / fps) * 1000)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"{start_timestamp}\n")
        f.write(f"{end_timestamp}\n")

def detect_shots_with_transnet(video_path, model):
    video_frames, single_frame_predictions, all_frame_predictions = model.predict_video(video_path)
    return model.predictions_to_scenes(single_frame_predictions).tolist()

def process_single_video(video_path, model, output_base_dir):
    video_name = Path(video_path).stem
    print(f"NAME: {video_name}")
    print(f"{'='*60}")
    
    video_output_dir = os.path.join(output_base_dir, video_name)
    keyframes_dir = os.path.join(video_output_dir, "keyframes")
    clips_dir = os.path.join(video_output_dir, "clips")
    timestamps_dir = os.path.join(video_output_dir, "timestamps")
    
    os.makedirs(keyframes_dir, exist_ok=True)
    os.makedirs(clips_dir, exist_ok=True)
    os.makedirs(timestamps_dir, exist_ok=True)
    
    fps = get_video_fps(video_path)
    
    shots = detect_shots_with_transnet(video_path, model)
    
    for i, (start_frame, end_frame) in enumerate(shots, 1):
        print(f"  SHOT PROGRESSION {i}/{len(shots)}: frames {start_frame}-{end_frame}")
        
        shot_id = video_name + '_' + str(i)

        keyframe_filename = f"{shot_id}.jpg"
        keyframe_path = os.path.join(keyframes_dir, keyframe_filename)
        extract_keyframe(video_path, start_frame, end_frame, fps, keyframe_path)

        clip_filename = f"{shot_id}.mp4"
        clip_path = os.path.join(clips_dir, clip_filename)
        extract_video_clip(video_path, start_frame, end_frame, fps, clip_path)

        timestamps_filename = f"{shot_id}.txt"
        timestamps_path = os.path.join(timestamps_dir, timestamps_filename)
        save_timestamps_file(timestamps_path, start_frame, end_frame, fps)

def main():
    if len(sys.argv) not in [2, 3]:
        print("Usage: python shot_extraction.py <video_directory> [output_directory]")
        print("Example: python shot_extraction.py ./videos ./output")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) == 3 else "./output"
    
    if not os.path.exists(input_dir) or not os.path.isdir(input_dir):
        print(f"Input folder not found: {input_dir}")
        sys.exit(1)
    
    os.makedirs(output_dir, exist_ok=True)
    
    video_files = [str(file_path) for file_path in Path(input_dir).rglob('*')]
    
    if not video_files:
        print(f"No video file found in: {input_dir}")
        sys.exit(1)
    
    try:
        model = TransNetV2()
    except Exception as e:
        print(f"TransNetV2 loading failed: {e}")
        sys.exit(1)
    
    for i, video_file in enumerate(video_files, 1):
        print(f"{'='*60}")
        print(f"VIDEO PROGRESSION: {i}/{len(video_files)}")
        process_single_video(video_file, model, output_dir)

if __name__ == "__main__":
    main()