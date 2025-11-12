# Nivel 2 - Diagrama de Contenedores

## Contenedores Implementados:

1. **API Gateway** (Puerto 5000)
   - Tecnología: Python Flask
   - Responsabilidad: Punto único de entrada, enrutamiento
   - Estado: ✅ IMPLEMENTADO Y FUNCIONAL

2. **Auth Service** (Puerto 5001)
   - Tecnología: Python Flask  
   - Responsabilidad: Autenticación, autorización, tokens
   - Estado: ✅ IMPLEMENTADO Y FUNCIONAL

3. **Account Service** (Puerto 5002)
   - Tecnología: Python Flask
   - Responsabilidad: Gestión de cuentas, transacciones, saldos
   - Estado: ✅ IMPLEMENTADO Y FUNCIONAL
   
   [Cliente]
↓ (HTTP Requests)
[API Gateway:5000]
↓ (HTTP) ↓ (HTTP)
[Auth Service:5001] [Account Service:5002]

## Comunicación:

### **Nivel 3 - Componentes:**
**`documentacion-c4/3-componentes.md`**
```markdown
# Nivel 3 - Diagrama de Componentes

## Auth Service Components:
- **AuthenticationManager**: Lógica de negocio de autenticación
- **Login Endpoint** (`/auth/login`): Recepción de credenciales
- **Token Verification** (`/auth/verify`): Validación de tokens

## Account Service Components:  
- **AccountManager**: Lógica de negocio de cuentas
- **Account Endpoints**: Operaciones CRUD de cuentas
- **Transaction Engine**: Procesamiento de transacciones

## API Gateway Components:
- **GatewayManager**: Orquestación y enrutamiento
- **Health Checker**: Monitoreo de servicios
- **Request Router**: Distribución de requests