@echo off
echo ========================================
echo    INICIANDO SISTEMA MINIBANK C4
echo ========================================

echo Iniciando Auth Service...
start cmd /k "cd auth_service && python app.py"

timeout /t 2 /nobreak >nul

echo Iniciando Account Service...
start cmd /k "cd account_service && python app.py"

timeout /t 2 /nobreak >nul

echo Iniciando API Gateway...
start cmd /k "cd api_gateway && python app.py"

timeout /t 2 /nobreak >nul

echo Iniciando Web Demo...
start cmd /k "cd web_demo && python app.py"

echo ========================================
echo    SISTEMA INICIADO CORRECTAMENTE
echo ========================================
echo Servicios disponibles:
echo - Web Demo: http://localhost:5005
echo - API Gateway: http://localhost:5000
echo - Auth Service: http://localhost:5001
echo - Account Service: http://localhost:5002
echo ========================================
pause