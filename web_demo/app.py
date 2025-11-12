# web_demo/app.py
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import requests
import json

app = Flask(__name__)
app.secret_key = 'minibank-demo-secret-key-2024'

# Configuración
API_GATEWAY = "http://localhost:6000/api"

class MiniBankClient:
    """Cliente para interactuar con la API"""
    
    def __init__(self):
        self.base_url = API_GATEWAY
    
    def login(self, username, password):
        """Iniciar sesión"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={"username": username, "password": password},
                timeout=5
            )
            return response.json(), response.status_code
        except Exception as e:
            return {"success": False, "error": str(e)}, 500
    
    def get_client_accounts(self, client_id):
        """Obtener cuentas del cliente"""
        try:
            response = requests.get(
                f"{self.base_url}/accounts/client/{client_id}",
                timeout=5
            )
            return response.json(), response.status_code
        except Exception as e:
            return {"success": False, "error": str(e)}, 500
    
    def deposit(self, account_id, amount, description=""):
        """Realizar depósito"""
        try:
            response = requests.post(
                f"{self.base_url}/accounts/{account_id}/deposit",
                json={"monto": amount, "descripcion": description},
                timeout=5
            )
            return response.json(), response.status_code
        except Exception as e:
            return {"success": False, "error": str(e)}, 500
    
    def withdraw(self, account_id, amount, description=""):
        """Realizar retiro"""
        try:
            response = requests.post(
                f"{self.base_url}/accounts/{account_id}/withdraw",
                json={"monto": amount, "descripcion": description},
                timeout=5
            )
            return response.json(), response.status_code
        except Exception as e:
            return {"success": False, "error": str(e)}, 500
    
    def get_transactions(self, account_id):
        """Obtener historial de transacciones"""
        try:
            response = requests.get(
                f"{self.base_url}/accounts/{account_id}/transactions",
                timeout=5
            )
            return response.json(), response.status_code
        except Exception as e:
            return {"success": False, "error": str(e)}, 500
    
    def get_system_health(self):
        """Obtener estado del sistema"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.json(), response.status_code
        except Exception as e:
            return {"success": False, "error": str(e)}, 500

# Cliente global
bank_client = MiniBankClient()

# ==================== RUTAS PRINCIPALES ====================
@app.route('/')
def index():
    """Página principal"""
    try:
        health, status_code = bank_client.get_system_health()
    except Exception as e:
        print("⚠️ Error al obtener estado del sistema:", e)
        health = {}

    # ✅ Asegura que siempre haya las claves que el template necesita
    if not isinstance(health, dict):
        health = {}

    health.setdefault("overall_status", "unknown")
    health.setdefault("services", {})

    # ✅ Renderiza la plantilla con seguridad
    return render_template(
        'index.html',
        health=health,
        user=session.get('user')
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        result, status = bank_client.login(username, password)
        
        if result.get('success'):
            session['user'] = result['user']
            session['token'] = result['token']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', 
                                 error=result.get('error', 'Error desconocido'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """Panel principal del usuario"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    
    # Obtener cuentas del usuario
    accounts_result, status = bank_client.get_client_accounts(user['user_id'])
    
    return render_template('dashboard.html',
                         user=user,
                         accounts=accounts_result.get('cuentas', []) if accounts_result.get('success') else [])

@app.route('/architecture')
def architecture():
    """Página de arquitectura C4"""
    return render_template('architecture.html',
                         user=session.get('user'))

# ==================== APIs PARA AJAX ====================
@app.route('/api/deposit', methods=['POST'])
def api_deposit():
    """API para depósitos (AJAX)"""
    if 'user' not in session:
        return jsonify({"success": False, "error": "No autenticado"}), 401
    
    data = request.get_json()
    account_id = data.get('account_id')
    amount = data.get('amount')
    description = data.get('description', '')
    
    result, status = bank_client.deposit(account_id, amount, description)
    return jsonify(result), status

@app.route('/api/withdraw', methods=['POST'])
def api_withdraw():
    """API para retiros (AJAX)"""
    if 'user' not in session:
        return jsonify({"success": False, "error": "No autenticado"}), 401
    
    data = request.get_json()
    account_id = data.get('account_id')
    amount = data.get('amount')
    description = data.get('description', '')
    
    result, status = bank_client.withdraw(account_id, amount, description)
    return jsonify(result), status

@app.route('/api/transactions/<int:account_id>')
def api_transactions(account_id):
    """API para transacciones (AJAX)"""
    if 'user' not in session:
        return jsonify({"success": False, "error": "No autenticado"}), 401
    
    result, status = bank_client.get_transactions(account_id)
    return jsonify(result), status

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🌐 WEB DEMO - MINIBANK C4")
    print("="*70)
    print("📡 Web Demo: http://localhost:6005")
    print("🔗 API Gateway: http://localhost:6000")
    print("\n👤 USUARIOS DE PRUEBA:")
    print("   josej / universidad123")
    print("   admin / admin123")
    print("   cliente / cliente123")
    print("\n🎯 CARACTERÍSTICAS:")
    print("   ✅ Login y autenticación")
    print("   ✅ Consulta de cuentas y saldos")
    print("   ✅ Depósitos y retiros en tiempo real")
    print("   ✅ Visualización de arquitectura C4")
    print("   ✅ Estado del sistema en tiempo real")
    print("="*70)
    
    app.run(host='0.0.0.0', port=6005, debug=True)