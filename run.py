import subprocess
import time
import os
import sys

def run_service(path):
    print(f"Iniciando {path}...")
    try:
        # En Windows se usa "python" y en Linux/Mac "python3"
        python_cmd = "python" if os.name == "nt" else "python3"
        subprocess.Popen([python_cmd, "app.py"], cwd=path)
    except FileNotFoundError as e:
        print(f"Error: no se pudo iniciar {path}. {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado al iniciar {path}: {e}")

print("========================================")
print("   INICIANDO SISTEMA MINIBANK C4")
print("========================================")

services = [
    "auth_service",
    "account_service",
    "api_gateway",
    "web_demo"
]

for service in services:
    run_service(service)
    time.sleep(2)  # espera entre servicios

print("========================================")
print("   SISTEMA INICIADO CORRECTAMENTE")
print("========================================")
print("Servicios disponibles:")
print("- Web Demo: http://localhost:6005")
print("- API Gateway: http://localhost:6000")
print("- Auth Service: http://localhost:6001")
print("- Account Service: http://localhost:6002")
print("========================================")

input("Presiona [Enter] para salir...")
