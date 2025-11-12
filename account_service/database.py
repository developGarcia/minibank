# account_service/database.py
import sqlite3
import os

class Database:
    def __init__(self, db_path="minibank.db"):
        self.db_path = db_path
        self._create_tables()
    
    def get_connection(self):
        """Conectar a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Para acceder a columnas por nombre
        return conn
    
    def _create_tables(self):
        """Crear las tablas si no existen"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                nombre TEXT NOT NULL,
                role TEXT DEFAULT 'customer'
            )
        ''')
        
        # Tabla de cuentas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cuentas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_cuenta TEXT UNIQUE NOT NULL,
                cliente_id INTEGER NOT NULL,
                saldo REAL DEFAULT 0.00,
                tipo TEXT DEFAULT 'ahorros',
                estado TEXT DEFAULT 'activa'
            )
        ''')
        
        # Tabla de transacciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transacciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cuenta_id INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                monto REAL NOT NULL,
                descripcion TEXT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insertar datos de ejemplo
        self._insert_sample_data(cursor)
        
        conn.commit()
        conn.close()
        print("✅ Base de datos SQLite creada")
    
    def _insert_sample_data(self, cursor):
        """Poblar la base de datos con datos de ejemplo"""
        # Insertar usuarios
        cursor.execute("SELECT COUNT(*) as count FROM usuarios")
        if cursor.fetchone()['count'] == 0:
            # Usuarios de prueba
            usuarios = [
                ('admin', 'admin123', 'Administrador', 'admin'),
                ('josej', 'universidad123', 'José Estudiante', 'customer'),
                ('cliente', 'cliente123', 'Cliente Ejemplo', 'customer')
            ]
            
            for usuario in usuarios:
                cursor.execute(
                    "INSERT OR IGNORE INTO usuarios (username, password, nombre, role) VALUES (?, ?, ?, ?)",
                    usuario
                )
            
            # Cuentas de prueba
            cuentas = [
                ('MB001', 1, 1500.00, 'corriente'),
                ('MB002', 2, 1200.00, 'ahorros'), 
                ('MB003', 3, 800.00, 'corriente')
            ]
            
            for cuenta in cuentas:
                cursor.execute(
                    "INSERT OR IGNORE INTO cuentas (numero_cuenta, cliente_id, saldo, tipo) VALUES (?, ?, ?, ?)",
                    cuenta
                )
            
            # Transacciones de prueba
            transacciones = [
                (2, 'deposito', 1000.00, 'Depósito inicial'),
                (2, 'deposito', 200.00, 'Depósito de nómina')
            ]
            
            for trans in transacciones:
                cursor.execute(
                    "INSERT INTO transacciones (cuenta_id, tipo, monto, descripcion) VALUES (?, ?, ?, ?)",
                    trans
                )
            
            print("✅ Datos de ejemplo insertados")
    
    def execute_query(self, query, params=None):
        """Ejecutar cualquier consulta SQL"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(query, params or ())
            
            if query.strip().upper().startswith('SELECT'):
                result = [dict(row) for row in cursor.fetchall()]
            else:
                conn.commit()
                result = cursor.lastrowid
            
            conn.close()
            return result
        except Exception as e:
            print(f"❌ Error en SQL: {e}")
            return None

# Crear instancia global de la base de datos
db = Database()