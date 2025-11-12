# auth_service/controllers/auth_controller.py
from flask import request, jsonify
from services.auth_service import AuthService

auth_service = AuthService()

def configure_auth_routes(app):
    """Configurar rutas de autenticación"""
    
    @app.route('/auth/login', methods=['POST'])
    def login():
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return jsonify({
                    'success': False,
                    'error': 'Username y password requeridos'
                }), 400
            
            user_data = auth_service.authenticate(username, password)
            
            if user_data:
                token = auth_service.generate_token(user_data)
                return jsonify({
                    'success': True,
                    'token': token,
                    'user': user_data
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Credenciales inválidas'
                }), 401
                
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Error en servidor: {str(e)}'
            }), 500
    
    @app.route('/auth/verify', methods=['POST'])
    def verify_token():
        data = request.get_json()
        token = data.get('token', '')
        
        token_data = auth_service.validate_token(token)
        if token_data:
            return jsonify({'valid': True, 'user_data': token_data['user_data']})
        else:
            return jsonify({'valid': False, 'error': 'Token inválido'})
    
    @app.route('/auth/health', methods=['GET'])
    def health_check():
        return jsonify({
            'service': 'Auth Service - MiniBank',
            'status': 'healthy',
            'database': 'SQLite',
            'active_sessions': len(auth_service.active_tokens)
        })