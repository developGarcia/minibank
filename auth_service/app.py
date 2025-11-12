# auth_service/app.py
from flask import Flask, jsonify
from controllers.auth_controller import configure_auth_routes

app = Flask(__name__)

# Configurar rutas
configure_auth_routes(app)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint no encontrado'}), 404

if __name__ == '__main__':
    print("=" * 60)
    print("🔐 AUTH SERVICE - MINIBANK C4")
    print("=" * 60)
    print("📡 Puerto: 6001")
    print("🗄️  Base de datos: SQLite compartida")
    print("\n📍 Endpoints:")
    print("   POST /auth/login")
    print("   POST /auth/verify") 
    print("   GET  /auth/health")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=6001, debug=True)