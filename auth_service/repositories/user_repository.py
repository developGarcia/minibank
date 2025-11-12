# auth_service/repositories/user_repository.py
from database import db

class UserRepository:
    def __init__(self):
        self.db = db
    
    def find_by_username(self, username):
        """Buscar usuario por nombre de usuario"""
        query = "SELECT * FROM usuarios WHERE username = ?"
        result = self.db.execute_query(query, (username,))
        return result[0] if result else None
    
    def find_by_id(self, user_id):
        """Buscar usuario por ID"""
        query = "SELECT * FROM usuarios WHERE id = ?"
        result = self.db.execute_query(query, (user_id,))
        return result[0] if result else None
    
    def create_user(self, username, password, nombre, role="customer"):
        """Crear nuevo usuario"""
        query = "INSERT INTO usuarios (username, password, nombre, role) VALUES (?, ?, ?, ?)"
        return self.db.execute_query(query, (username, password, nombre, role))