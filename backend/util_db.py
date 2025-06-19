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
                keyframe_name TEXT PRIMARY KEY,
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
        }
        return pickle.dumps(tensor_data)
    
    def _deserialize_tensor(self, blob_data):
        data = pickle.loads(blob_data)
        tensor = torch.from_numpy(data['data'])
        
        if data['device'] != 'cpu':
            tensor = tensor.to(data['device'])

        return tensor
    
    def insert_shot(self, keyframe_name: str,
                   start_stamp: int, end_stamp: int, 
                   embedding: torch.Tensor) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            embedding_blob = self._serialize_tensor(embedding)
            
            cursor.execute('''INSERT INTO shots (keyframe_name, start_stamp, end_stamp, embedding) VALUES (?, ?, ?, ?)''', (keyframe_name, start_stamp, end_stamp, embedding_blob))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Erreur lors de l'insertion: {e}")
            return False
    
    def get_shot(self, keyframe_name: str) -> Optional[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM shots WHERE keyframe_name = ?', (keyframe_name,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'keyframe_name': row[0],
                'start_stamp': row[1],
                'end_stamp': row[2],
            }
        return None
    
    def get_embedding(self, keyframe_name: str) -> Optional[Any]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM shots WHERE keyframe_name = ?', (keyframe_name,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return True, self._deserialize_tensor(row[3])
        return False, None