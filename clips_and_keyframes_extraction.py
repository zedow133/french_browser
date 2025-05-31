#!/usr/bin/env python3
import ffmpeg
import os
import sys
import sqlite3
from pathlib import Path
from transnetv2 import TransNetV2

def create_database(db_path):
    """Crée la base de données SQLite avec la table shots"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Création de la table shots
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                keyframe_path TEXT NOT NULL,
                clip_path TEXT NOT NULL,
                start_stamp REAL NOT NULL,
                end_stamp REAL NOT NULL,
                duration REAL NOT NULL,
                shot_index INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"Base de données créée: {db_path}")
        return True
    except Exception as e:
        print(f"Erreur lors de la création de la base de données: {e}")
        return False

def insert_shot_to_database(db_path, source, keyframe_path, clip_path, start_stamp, end_stamp, shot_index):
    """Insère un shot dans la base de données"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        duration = end_stamp - start_stamp
        
        cursor.execute('''
            INSERT INTO shots (source, keyframe_path, clip_path, start_stamp, end_stamp, duration, shot_index)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (source, keyframe_path, clip_path, start_stamp, end_stamp, duration, shot_index))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erreur lors de l'insertion en base: {e}")
        return False

def save_timestamps_file(output_path, shots, fps, video_name):
    """Sauvegarde les timestamps dans un fichier texte"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"Timestamps des shots pour: {video_name}\n")
            f.write(f"FPS: {fps:.2f}\n")
            f.write("="*60 + "\n\n")
            
            for i, (start_frame, end_frame) in enumerate(shots, 1):
                start_timestamp = frame_to_timestamp(start_frame, fps)
                end_timestamp = frame_to_timestamp(end_frame, fps)
                duration = end_timestamp - start_timestamp
                
                f.write(f"Shot {i:03d}:\n")
                f.write(f"  Frames: {start_frame} - {end_frame}\n")
                f.write(f"  Début: {start_timestamp:.3f}s\n")
                f.write(f"  Fin: {end_timestamp:.3f}s\n")
                f.write(f"  Durée: {duration:.3f}s\n")
                f.write(f"  Début (HH:MM:SS): {seconds_to_hms(start_timestamp)}\n")
                f.write(f"  Fin (HH:MM:SS): {seconds_to_hms(end_timestamp)}\n")
                f.write("-" * 40 + "\n")
        
        print(f"Timestamps sauvegardés: {output_path}")
        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des timestamps: {e}")
        return False

def seconds_to_hms(seconds):
    """Convertit les secondes en format HH:MM:SS.mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"

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

def detect_shots_with_transnet(video_path, model):
    """Détecte les plans avec TransNetV2"""
    try:
        print(f"  Détection des plans avec TransNetV2...")
        video_frames, single_frame_predictions, all_frame_predictions = model.predict_video(video_path)
        shots = model.predictions_to_scenes(single_frame_predictions)
        
        # Convertir les shots en format (start_frame, end_frame)
        shot_boundaries = []
        for shot in shots:
            start_frame = int(shot[0])
            end_frame = int(shot[1])
            shot_boundaries.append((start_frame, end_frame))
        
        print(f"  {len(shot_boundaries)} plans détectés")
        return shot_boundaries
    except Exception as e:
        print(f"  Erreur lors de la détection des plans: {e}")
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
            
            print(f"  Informations vidéo:")
            print(f"    Résolution: {width}x{height}")
            print(f"    Durée: {duration:.2f}s")
            print(f"    FPS: {fps:.2f}")
            print(f"    Frames totales: {total_frames}")
            
            return fps, total_frames
        else:
            print("  Aucun flux vidéo trouvé")
            return 25.0, 0
    except Exception as e:
        print(f"  Erreur lors de l'analyse de la vidéo: {e}")
        return 25.0, 0

def process_single_video(video_path, model, output_base_dir, db_path):
    """Traite une seule vidéo"""
    video_name = Path(video_path).stem
    print(f"\n{'='*60}")
    print(f"Traitement de: {video_name}")
    print(f"{'='*60}")
    
    # Création des dossiers de sortie spécifiques à cette vidéo
    video_output_dir = os.path.join(output_base_dir, video_name)
    keyframes_dir = os.path.join(video_output_dir, "keyframes")
    clips_dir = os.path.join(video_output_dir, "clips")
    
    os.makedirs(keyframes_dir, exist_ok=True)
    os.makedirs(clips_dir, exist_ok=True)
    
    # Obtenir les informations de la vidéo
    fps, total_frames = get_video_info(video_path)
    
    if total_frames == 0:
        print(f"  ⚠️  Impossible d'analyser la vidéo {video_name}")
        return 0, 0, 0
    
    # Détection des plans avec TransNetV2
    shots = detect_shots_with_transnet(video_path, model)
    
    if not shots:
        print(f"  ⚠️  Aucun plan détecté pour {video_name}")
        return 0, 0, 0
    
    # Sauvegarde des timestamps
    timestamps_file = os.path.join(video_output_dir, f"{video_name}_timestamps.txt")
    save_timestamps_file(timestamps_file, shots, fps, video_name)
    
    # Validation des frames
    invalid_shots = []
    valid_shots = []
    for i, (start_frame, end_frame) in enumerate(shots):
        if start_frame < 0 or end_frame >= total_frames or start_frame > end_frame:
            invalid_shots.append(i + 1)
        else:
            valid_shots.append((start_frame, end_frame))
    
    if invalid_shots:
        print(f"  ⚠️  Plans avec des frames invalides ignorés: {len(invalid_shots)}")
    
    # Traitement de chaque plan valide
    successful_keyframes = 0
    successful_clips = 0
    
    for i, (start_frame, end_frame) in enumerate(valid_shots, 1):
        print(f"  Plan {i}/{len(valid_shots)}: frames {start_frame}-{end_frame}")
        
        # Calcul de la frame du milieu (keyframe)
        middle_frame = (start_frame + end_frame) // 2
        duration = (end_frame - start_frame + 1) / fps
        
        # Calcul des timestamps
        start_timestamp = frame_to_timestamp(start_frame, fps)
        end_timestamp = frame_to_timestamp(end_frame, fps)
        
        print(f"    Keyframe: frame {middle_frame}, Durée: {duration:.2f}s")
        print(f"    Timestamps: {start_timestamp:.3f}s - {end_timestamp:.3f}s")
        
        # Chemins des fichiers de sortie
        keyframe_filename = f"keyframe_shot_{middle_frame:06d}.jpg"
        clip_filename = f"shot_{i:03d}_frames_{start_frame}-{end_frame}.mp4"
        keyframe_path = os.path.join(keyframes_dir, keyframe_filename)
        clip_path = os.path.join(clips_dir, clip_filename)
        
        # Extraction de la keyframe
        keyframe_success = extract_keyframe(video_path, middle_frame, fps, keyframes_dir)
        if keyframe_success:
            successful_keyframes += 1
        
        # Extraction du clip vidéo
        clip_success = extract_video_clip(video_path, start_frame, end_frame, fps, clips_dir, i)
        if clip_success:
            successful_clips += 1
        
        # Insertion en base de données si les deux extractions ont réussi
        if keyframe_success and clip_success:
            # Utilisation de chemins relatifs pour la base de données
            relative_keyframe_path = os.path.relpath(keyframe_path, output_base_dir)
            relative_clip_path = os.path.relpath(clip_path, output_base_dir)
            
            insert_shot_to_database(
                db_path, 
                video_name, 
                relative_keyframe_path, 
                relative_clip_path, 
                start_timestamp, 
                end_timestamp, 
                i
            )
    
    # Résumé pour cette vidéo
    total_extracted_duration = sum(
        (end_frame - start_frame + 1) / fps 
        for start_frame, end_frame in valid_shots[:successful_clips]
    ) if successful_clips > 0 else 0
    
    print(f"\n  === RÉSUMÉ POUR {video_name} ===")
    print(f"  Plans détectés: {len(shots)}")
    print(f"  Plans valides: {len(valid_shots)}")
    print(f"  Keyframes extraites: {successful_keyframes}")
    print(f"  Clips extraits: {successful_clips}")
    print(f"  Durée totale extraite: {total_extracted_duration:.2f}s")
    print(f"  Timestamps: {timestamps_file}")
    print(f"  Keyframes dans: {keyframes_dir}")
    print(f"  Clips dans: {clips_dir}")
    
    return len(valid_shots), successful_keyframes, successful_clips

def get_video_files(input_dir):
    """Récupère tous les fichiers vidéo dans le dossier"""
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v'}
    video_files = []
    
    for file_path in Path(input_dir).rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in video_extensions:
            video_files.append(str(file_path))
    
    return sorted(video_files)

def main():
    if len(sys.argv) not in [2, 3]:
        print("Usage: python script.py <dossier_videos> [dossier_sortie]")
        print("Exemple: python script.py ./videos ./output")
        print("Si le dossier de sortie n'est pas spécifié, './output' sera utilisé")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) == 3 else "./output"
    
    # Vérification du dossier d'entrée
    if not os.path.exists(input_dir):
        print(f"Dossier d'entrée non trouvé: {input_dir}")
        sys.exit(1)
    
    if not os.path.isdir(input_dir):
        print(f"Le chemin spécifié n'est pas un dossier: {input_dir}")
        sys.exit(1)
    
    # Création du dossier de sortie
    os.makedirs(output_dir, exist_ok=True)
    
    # Création de la base de données
    db_path = os.path.join(output_dir, "shots_database.db")
    if not create_database(db_path):
        print("Impossible de créer la base de données. Arrêt du script.")
        sys.exit(1)
    
    # Recherche des fichiers vidéo
    video_files = get_video_files(input_dir)
    
    if not video_files:
        print(f"Aucun fichier vidéo trouvé dans: {input_dir}")
        print("Extensions supportées: .mp4, .avi, .mov, .mkv, .wmv, .flv, .webm, .m4v")
        sys.exit(1)
    
    print(f"Trouvé {len(video_files)} fichier(s) vidéo:")
    for video_file in video_files:
        print(f"  - {video_file}")
    
    # Initialisation du modèle TransNetV2
    print(f"\nInitialisation du modèle TransNetV2...")
    try:
        model = TransNetV2()
        print("Modèle TransNetV2 chargé avec succès")
    except Exception as e:
        print(f"Erreur lors du chargement du modèle TransNetV2: {e}")
        print("Assurez-vous que transnetv2 est installé: pip install transnetv2")
        sys.exit(1)
    
    # Traitement de chaque vidéo
    total_shots = 0
    total_keyframes = 0
    total_clips = 0
    failed_videos = []
    
    for i, video_file in enumerate(video_files, 1):
        print(f"\n{'#'*80}")
        print(f"PROGRESSION: {i}/{len(video_files)}")
        print(f"{'#'*80}")
        
        try:
            shots, keyframes, clips = process_single_video(video_file, model, output_dir, db_path)
            total_shots += shots
            total_keyframes += keyframes
            total_clips += clips
            
            if keyframes == 0 and clips == 0:
                failed_videos.append(video_file)
                
        except Exception as e:
            print(f"Erreur lors du traitement de {video_file}: {e}")
            failed_videos.append(video_file)
    
    # Résumé final global
    print(f"\n{'='*80}")
    print(f"RÉSUMÉ GLOBAL")
    print(f"{'='*80}")
    print(f"Vidéos traitées: {len(video_files)}")
    print(f"Plans détectés au total: {total_shots}")
    print(f"Keyframes extraites au total: {total_keyframes}")
    print(f"Clips extraits au total: {total_clips}")
    print(f"Base de données: {db_path}")
    print(f"Résultats sauvegardés dans: {output_dir}")
    
    if failed_videos:
        print(f"\n⚠️  Vidéos avec des problèmes ({len(failed_videos)}):")
        for video in failed_videos:
            print(f"  - {video}")
    else:
        print(f"\n✅ Toutes les vidéos ont été traitées avec succès!")

if __name__ == "__main__":
    main()