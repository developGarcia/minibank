# Nivel 4 - Diagrama de Código

## Estructuras de Datos Principales:

### Auth Service:
```python
usuarios = {
    'username': {
        'password': '...', 
        'user_id': '...',
        'role': '...'
    }
}
tokens_generados = {}  # Almacenamiento de sesiones