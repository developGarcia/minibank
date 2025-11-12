# auth_service/services/auth_service.py
import hashlib
import time
from repositories.user_repository import UserRepository

class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.active_tokens = {}  # Tokens en memoria
    
    def authenticate(self, username, password):
        """Autenticar usuario"""
        user = self.user_repository.find_by_username(username)
        
        if user and user['password'] == password:
            return {
                'user_id': user['id'],
                'username': user['username'],
                'nombre': user['nombre'],
                'role': user['role']
            }
        return None
    
    def generate_token(self, user_data):
        """Generar token de sesión"""
        token_base = f"{user_data['user_id']}_{user_data['username']}_{time.time()}"
        token = hashlib.md5(token_base.encode()).hexdigest()
        
        self.active_tokens[token] = {
            'user_data': user_data,
            'created_at': time.time()
        }
        
        return token
    
    def validate_token(self, token):
        """Validar token"""
        return self.active_tokens.get(token)
    
    def logout(self, token):
        """Cerrar sesión"""
        if token in self.active_tokens:
            del self.active_tokens[token]
            return True
        return False