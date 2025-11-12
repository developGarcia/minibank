# api_gateway/app.py
from flask import Flask, request, jsonify
import requests
import datetime

app = Flask(__name__)

# Configuración de servicios
SERVICES = {
    'auth': {
        'base_url': 'http://localhost:6001',
        'prefix': '/auth'
    },
    'accounts': {
        'base_url': 'http://localhost:6002', 
        'prefix': '/accounts'
    }
}

class GatewayManager:
    def route_request(self, service_name, path, method, data=None):
        """Enrutar requests a servicios"""
        if service_name not in SERVICES:
            return {'success': False, 'error': 'Servicio no encontrado'}
        
        service_config = SERVICES[service_name]
        base_url = service_config['base_url']
        prefix = service_config['prefix']
        
        target_url = f"{base_url}{prefix}/{path}"
        
        print(f"🎯 Enrutando {method} a: {target_url}")
        
        try:
            response = requests.request(
                method=method,
                url=target_url,
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print(f"✅ Respuesta: {response.status_code}")
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'status_code': response.status_code,
                    'data': response.json()
                }
            else:
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'error': f'Error {response.status_code} del servicio'
                }
                
        except requests.exceptions.ConnectionError:
            return {'success': False, 'error': 'Servicio no disponible'}
        except Exception as e:
            return {'success': False, 'error': f'Error: {str(e)}'}

gateway_manager = GatewayManager()

@app.route('/api/<service_name>/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gateway_proxy(service_name, subpath):
    """Proxy para todos los servicios"""
    print(f"📥 REQUEST: {request.method} /api/{service_name}/{subpath}")
    
    request_data = request.get_json(silent=True) or {}
    
    resultado = gateway_manager.route_request(
        service_name=service_name,
        path=subpath,
        method=request.method,
        data=request_data
    )
    
    if resultado['success']:
        return jsonify(resultado['data']), resultado['status_code']
    else:
        return jsonify({
            'success': False,
            'error': resultado['error'],
            'gateway': True
        }), resultado.get('status_code', 500)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check del sistema completo"""
    health_status = {}
    
    for service_name, config in SERVICES.items():
        try:
            health_url = f"{config['base_url']}{config['prefix']}/health"
            response = requests.get(health_url, timeout=5)
            health_status[service_name] = {
                'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                'status_code': response.status_code
            }
        except:
            health_status[service_name] = {'status': 'unhealthy', 'status_code': 0}
    
    overall_healthy = all(s['status'] == 'healthy' for s in health_status.values())
    
    return jsonify({
        'overall_status': 'healthy' if overall_healthy else 'degraded',
        'services': health_status,
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/api/info', methods=['GET'])
def system_info():
    return jsonify({
        'system': 'MiniBank API Gateway - C4 Architecture',
        'description': 'Sistema bancario con arquitectura de microservicios',
        'services': {
            'auth': 'http://localhost:6001',
            'accounts': 'http://localhost:6002'
        }
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🚪 API GATEWAY - MINIBANK C4")
    print("=" * 60)
    print("📡 Puerto: 5000")
    print("🔗 Servicios:")
    print("   🔐 Auth:    http://localhost:6001")
    print("   💰 Accounts: http://localhost:6002")
    print("\n📍 Ejemplos:")
    print("   POST /api/auth/login")
    print("   GET  /api/accounts/client/2")
    print("   GET  /api/health")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=6000, debug=True)