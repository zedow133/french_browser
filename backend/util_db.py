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
    
    def insert_shot(self, shot_id: str, source: str, 
                   start_stamp: int, end_stamp: int, 
                   embedding: torch.Tensor) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            embedding_blob = self._serialize_tensor(embedding)
            
            cursor.execute('''INSERT INTO shots (shot_id, source, start_stamp, end_stamp, embedding) VALUES (?, ?, ?, ?, ?)''', (shot_id, source, start_stamp, end_stamp, embedding_blob))
            
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
            return {
                'shot_id': row[0],
                'source': row[1],
                'start_stamp': row[2],
                'end_stamp': row[3],
            }
        return None
    
    def get_embedding(self, shot_id: str) -> Optional[Any]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM shots WHERE shot_id = ?', (shot_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return True, self._deserialize_tensor(row[4])
        return False, None

    def get_all_shots(self) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM shots')
        
        rows = cursor.fetchall()
        conn.close()
        
        shots = []
        for row in rows:
            embedding = self._deserialize_tensor(row[4])
            
            shots.append({
                'shot_id': row[0],
                'source': row[1],
                'start_stamp': row[2],
                'end_stamp': row[3],
                'embedding': embedding
            })
        
        return shots