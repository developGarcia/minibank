# account_service/controllers/account_controller.py
from flask import request, jsonify
from services.account_service import AccountService

account_service = AccountService()

def configure_account_routes(app):
    """Configurar todas las rutas del servicio"""
    
    @app.route('/accounts/<int:account_id>', methods=['GET'])
    def get_account(account_id):
        result = account_service.get_account(account_id)
        status_code = 200 if result['success'] else 404
        return jsonify(result), status_code
    
    @app.route('/accounts/client/<int:customer_id>', methods=['GET'])
    def get_client_accounts(customer_id):
        result = account_service.get_customer_accounts(customer_id)
        return jsonify(result)
    
    @app.route('/accounts/<int:account_id>/deposit', methods=['POST'])
    def deposit(account_id):
        data = request.get_json()
        amount = data.get('monto', 0)
        description = data.get('descripcion', '')
        
        result = account_service.deposit(account_id, amount, description)
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
    
    @app.route('/accounts/<int:account_id>/withdraw', methods=['POST'])
    def withdraw(account_id):
        data = request.get_json()
        amount = data.get('monto', 0)
        description = data.get('descripcion', '')
        
        result = account_service.withdraw(account_id, amount, description)
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
    
    @app.route('/accounts/<int:account_id>/transactions', methods=['GET'])
    def get_transactions(account_id):
        limit = request.args.get('limit', 10, type=int)
        result = account_service.get_account_transactions(account_id, limit)
        status_code = 200 if result['success'] else 404
        return jsonify(result), status_code
    
    @app.route('/accounts/health', methods=['GET'])
    def health_check():
        return jsonify({
            'service': 'Account Service - MiniBank',
            'status': 'healthy',
            'database': 'SQLite'
        })