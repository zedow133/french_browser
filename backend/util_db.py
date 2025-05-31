import sqlite3
import json
import pickle
import torch
from typing import List, Optional, Dict, Any

class ShotsDatabase:
    def __init__(self, db_dir: str):
        self.db_path = db_dir + '/shots_database.db'
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shots (
                shot_id TEXT PRIMARY KEY,
                source TEXT NOT NULL,
                keyframe_path TEXT NOT NULL,
                clip_path TEXT NOT NULL,
                start_stamp INTEGER NOT NULL,
                end_stamp INTEGER NOT NULL,
                embedding BLOB NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()

    def _serialize_tensor(self, tensor):
        tensor_data = {
            'data': tensor.cpu().detach().numpy(),
            'device': str(tensor.device),
            'requires_grad': tensor.requires_grad
        }
        return pickle.dumps(tensor_data)
    
    def _deserialize_tensor(self, blob_data):
        data = pickle.loads(blob_data)
        tensor = torch.from_numpy(data['data'])
        
        if data['device'] != 'cpu':
            tensor = tensor.to(data['device'])
        
        if data['requires_grad']:
            tensor.requires_grad_(True)
            
        return tensor
    
    def insert_shot(self, shot_id: str, source: str, keyframe_path: str, 
                   clip_path: str, start_stamp: int, end_stamp: int, 
                   embedding: torch.Tensor) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Sérialiser le tensor
            embedding_blob = self._serialize_tensor(embedding)
            
            cursor.execute('''
                INSERT INTO shots (shot_id, source, keyframe_path, clip_path, 
                                 start_stamp, end_stamp, embedding)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (shot_id, source, keyframe_path, clip_path, start_stamp, end_stamp, embedding_blob))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Erreur lors de l'insertion: {e}")
            return False
    
    def get_shot(self, shot_id: str) -> Optional[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM shots WHERE shot_id = ?', (shot_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            embedding = self._deserialize_tensor(row[6])
            
            return {
                'shot_id': row[0],
                'source': row[1],
                'keyframe_path': row[2],
                'clip_path': row[3],
                'start_stamp': row[4],
                'end_stamp': row[5],
                'embedding': embedding
            }
        return None
    
    def get_all_shots(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if limit:
            cursor.execute('SELECT * FROM shots LIMIT ?', (limit,))
        else:
            cursor.execute('SELECT * FROM shots')
        
        rows = cursor.fetchall()
        conn.close()
        
        shots = []
        for row in rows:
            embedding = self._deserialize_tensor(row[6])
            
            shots.append({
                'shot_id': row[0],
                'source': row[1],
                'keyframe_path': row[2],
                'clip_path': row[3],
                'start_stamp': row[4],
                'end_stamp': row[5],
                'embedding': embedding
            })
        
        return shots
    
    def search_by_source(self, source: str) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM shots WHERE source LIKE ?', (f'%{source}%',))
        rows = cursor.fetchall()
        conn.close()
        
        shots = []
        for row in rows:
            shots.append({
                'shot_id': row[0],
                'source': row[1],
                'keyframe_path': row[2],
                'clip_path': row[3],
                'start_stamp': row[4],
                'end_stamp': row[5],
                'embedding': json.loads(row[6])
            })
        
        return shots