from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MiniBank Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .success { color: green; }
            .error { color: red; }
        </style>
    </head>
    <body>
        <h1>🚀 MiniBank Web Demo - FUNCIONANDO</h1>
        <p class="success">¡Si ves esta página, la aplicación web está funcionando!</p>
        
        <h2>Servicios Backend:</h2>
        <ul>
            <li><a href="http://localhost:5000/api/health" target="_blank">API Gateway Health</a></li>
            <li><a href="http://localhost:5001/auth/health" target="_blank">Auth Service Health</a></li>
            <li><a href="http://localhost:5002/accounts/health" target="_blank">Account Service Health</a></li>
        </ul>
        
        <h2>Probar Login:</h2>
        <form action="http://localhost:5000/api/auth/login" method="POST" target="_blank">
            <input type="hidden" name="username" value="josej">
            <input type="hidden" name="password" value="universidad123">
            <button type="submit">Probar Login (josej/universidad123)</button>
        </form>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 SERVIDOR WEB DE PRUEBA - MINIBANK")
    print("=" * 60)
    print("📡 URL: http://localhost:8080")
    print("⏰ Iniciando servidor...")
    
    try:
        app.run(host='0.0.0.0', port=8080, debug=True)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("💡 Posibles soluciones:")
        print("   - El puerto 5005 puede estar en uso")
        print("   - Intenta con otro puerto: python simple_test.py --port 8080")