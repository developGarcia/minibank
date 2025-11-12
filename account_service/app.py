# account_service/app.py
from flask import Flask, jsonify
from controllers.account_controller import configure_account_routes

app = Flask(__name__)

# Configurar rutas
configure_account_routes(app)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("💰 ACCOUNT SERVICE - MINIBANK C4")
    print("=" * 60)
    print("📡 Puerto: 6002")
    print("🗄️  Base de datos: SQLite (minibank.db)")
    print("\n📍 Endpoints:")
    print("   GET  /accounts/<id>")
    print("   GET  /accounts/client/<cliente_id>") 
    print("   POST /accounts/<id>/deposit")
    print("   POST /accounts/<id>/withdraw")
    print("   GET  /accounts/<id>/transactions")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=6002, debug=True)