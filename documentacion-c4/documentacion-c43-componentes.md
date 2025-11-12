# Nivel 3 - Diagrama de Componentes

## Servicio de Autenticación:
### Componentes Identificados:

1. **AuthenticationManager** (Componente de Negocio)
   - Responsabilidad: Lógica de autenticación
   - Métodos: verificar_usuario(), generar_token(), validar_token()

2. **Login Endpoint** (Componente Web) 
   - Responsabilidad: Recibir requests de login
   - Ruta: POST /auth/login

## Servicio de Cuentas:
### Componentes Identificados:

1. **AccountManager** (Componente de Negocio)
   - Responsabilidad: Lógica de cuentas y transacciones
   - Métodos: obtener_cuenta(), realizar_deposito(), realizar_retiro()

2. **Account Endpoints** (Componente Web)
   - Responsabilidad: Exponer operaciones bancarias via API
   - Rutas: GET /accounts/<id>, POST /accounts/<id>/deposit, etc.

## Flujo de Operaciones Bancarias:
[Cliente] → [Account Endpoints] → [AccountManager] → [Base de datos cuentas]