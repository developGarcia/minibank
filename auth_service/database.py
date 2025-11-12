# auth_service/database.py
import sqlite3
import os

class Database:
    def __init__(self, db_path="../account_service/minibank.db"):
        # Usamos la misma base de datos que account_service
        self.db_path = db_path
    
    def get_connection(self):
        """Conectar a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def execute_query(self, query, params=None):
        """Ejecutar consulta SQL"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(query, params or ())
            
            if query.strip().upper().startswith('SELECT'):
                result = [dict(row) for row in cursor.fetchall()]
            else:
                conn.commit()
                result = cursor.lastrowid
            
            conn.close()
            return result
        except Exception as e:
            print(f"❌ Error en SQL: {e}")
            return None

# Instancia global
db = Database()