#!/usr/bin/env python3
import ffmpeg
import os
import sys
from pathlib import Path

def get_video_fps(video_path):
    """Obtient le FPS de la vidéo"""
    try:
        probe = ffmpeg.probe(video_path, select_streams='v:0')
        fps_str = probe['streams'][0]['r_frame_rate']
        if '/' in fps_str:
            num, den = fps_str.split('/')
            fps = float(num) / float(den)
        else:
            fps = float(fps_str)
        return fps
    except Exception as e:
        print(f"Erreur lors de l'obtention du FPS: {e}")
        return 25.0  # FPS par défaut

def frame_to_timestamp(frame, fps):
    """Convertit un numéro de frame en timestamp (secondes)"""
    return frame / fps

def extract_keyframe(video_path, frame_num, fps, output_dir):
    """Extrait une keyframe à partir d'un numéro de frame"""
    timestamp = frame_to_timestamp(frame_num, fps)
    output_path = os.path.join(output_dir, f"keyframe_shot_{frame_num:06d}.jpg")
    
    try:
        (
            ffmpeg
            .input(video_path, ss=timestamp)
            .output(output_path, vframes=1, **{'q:v': 2})
            .overwrite_output()
            .run(quiet=True)
        )
        print(f"Keyframe extraite: {output_path}")
        return True
    except ffmpeg.Error as e:
        print(f"Erreur lors de l'extraction de la keyframe {frame_num}: {e}")
        return False

def extract_video_clip(video_path, start_frame, end_frame, fps, output_dir, shot_index):
    """Extrait un clip vidéo entre deux frames"""
    start_timestamp = frame_to_timestamp(start_frame, fps)
    duration_frames = end_frame - start_frame + 1
    duration_seconds = duration_frames / fps
    
    output_path = os.path.join(output_dir, f"shot_{shot_index:03d}_frames_{start_frame}-{end_frame}.mp4")
    
    try:
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
        print(f"Clip extrait: {output_path}")
        return True
    except ffmpeg.Error as e:
        print(f"Erreur lors de l'extraction du clip {shot_index}: {e}")
        return False

def parse_shots_file(shots_file_path):
    """Parse le fichier contenant les données des shots"""
    shots = []
    try:
        with open(shots_file_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    start_frame, end_frame = map(int, line.split())
                    shots.append((start_frame, end_frame))
                except ValueError:
                    print(f"Ligne {line_num} ignorée (format invalide): {line}")
        
        return shots
    except FileNotFoundError:
        print(f"Fichier non trouvé: {shots_file_path}")
        return []
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier: {e}")
        return []

def get_video_info(video_path):
    """Obtient des informations détaillées sur la vidéo"""
    try:
        probe = ffmpeg.probe(video_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        
        if video_stream:
            width = video_stream.get('width')
            height = video_stream.get('height')
            duration = float(probe['format'].get('duration', 0))
            fps = get_video_fps(video_path)
            total_frames = int(duration * fps)
            
            print(f"Informations vidéo:")
            print(f"  Résolution: {width}x{height}")
            print(f"  Durée: {duration:.2f}s")
            print(f"  FPS: {fps:.2f}")
            print(f"  Frames totales: {total_frames}")
            
            return fps, total_frames
        else:
            print("Aucun flux vidéo trouvé")
            return 25.0, 0
    except Exception as e:
        print(f"Erreur lors de l'analyse de la vidéo: {e}")
        return 25.0, 0

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <video_file> <shots_file>")
        print("Exemple: python script.py video.mp4 shots.txt")
        sys.exit(1)
    
    video_path = sys.argv[1]
    shots_file_path = sys.argv[2]
    
    # Vérification des fichiers d'entrée
    if not os.path.exists(video_path):
        print(f"Fichier vidéo non trouvé: {video_path}")
        sys.exit(1)
    
    if not os.path.exists(shots_file_path):
        print(f"Fichier de shots non trouvé: {shots_file_path}")
        sys.exit(1)
    
    # Création des dossiers de sortie
    base_name = Path(video_path).stem
    keyframes_dir = f"{base_name}_keyframes"
    clips_dir = f"{base_name}_clips"
    
    os.makedirs(keyframes_dir, exist_ok=True)
    os.makedirs(clips_dir, exist_ok=True)
    
    print(f"Analyse de la vidéo: {video_path}")
    
    # Obtenir les informations de la vidéo
    fps, total_frames = get_video_info(video_path)
    
    # Parser le fichier de shots
    shots = parse_shots_file(shots_file_path)
    if not shots:
        print("Aucun shot valide trouvé dans le fichier.")
        sys.exit(1)
    
    print(f"\nNombre de shots trouvés: {len(shots)}")
    
    # Validation des frames
    invalid_shots = []
    for i, (start_frame, end_frame) in enumerate(shots):
        if start_frame < 0 or end_frame >= total_frames or start_frame > end_frame:
            invalid_shots.append(i + 1)
    
    if invalid_shots:
        print(f"⚠️  Shots avec des frames invalides: {invalid_shots}")
        print(f"   (La vidéo contient {total_frames} frames au total)")
    
    # Traitement de chaque shot
    successful_keyframes = 0
    successful_clips = 0
    
    for i, (start_frame, end_frame) in enumerate(shots, 1):
        print(f"\nTraitement du shot {i}/{len(shots)}: frames {start_frame}-{end_frame}")
        
        # Validation de ce shot spécifique
        if start_frame < 0 or end_frame >= total_frames or start_frame > end_frame:
            print(f"  ⚠️  Shot {i} ignoré: frames invalides")
            continue
        
        # Calcul de la frame du milieu (keyframe)
        middle_frame = (start_frame + end_frame) // 2
        
        print(f"  Keyframe: frame {middle_frame}")
        print(f"  Durée: {(end_frame - start_frame + 1) / fps:.2f}s")
        
        # Extraction de la keyframe
        if extract_keyframe(video_path, middle_frame, fps, keyframes_dir):
            successful_keyframes += 1
        
        # Extraction du clip vidéo
        if extract_video_clip(video_path, start_frame, end_frame, fps, clips_dir, i):
            successful_clips += 1
    
    # Résumé final
    print(f"\n=== RÉSUMÉ ===")
    print(f"Shots traités: {len(shots)}")
    print(f"Keyframes extraites avec succès: {successful_keyframes}")
    print(f"Clips extraits avec succès: {successful_clips}")
    print(f"Keyframes sauvegardées dans: {keyframes_dir}/")
    print(f"Clips sauvegardés dans: {clips_dir}/")
    
    if successful_keyframes == len(shots) and successful_clips == len(shots):
        print("✅ Toutes les extractions ont réussi!")
    else:
        print("⚠️  Certaines extractions ont échoué. Vérifiez les messages d'erreur ci-dessus.")
        
    # Statistiques supplémentaires
    if successful_clips > 0:
        total_extracted_duration = sum(
            (end_frame - start_frame + 1) / fps 
            for start_frame, end_frame in shots[:successful_clips]
        )
        print(f"Durée totale extraite: {total_extracted_duration:.2f}s")

if __name__ == "__main__":
    main()