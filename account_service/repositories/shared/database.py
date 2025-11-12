"""
CONEXIÓN A BASE DE DATOS - MySQL
Recurso compartido para todos los servicios
"""
import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'database': 'minibank_c4',
            'user': 'root',      # Usuario por defecto XAMPP
            'password': '',      # Password por defecto XAMPP (vacío)
            'port': 3306
        }
        self.connection = None
    
    def get_connection(self):
        """Obtener conexión a la base de datos"""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**self.config)
            return self.connection
        except Error as e:
            print(f"❌ Error conectando a MySQL: {e}")
            return None
    
    def execute_query(self, query, params=None):
        """Ejecutar consulta y retornar resultados"""
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, params or ())
                
                if query.strip().upper().startswith('SELECT'):
                    result = cursor.fetchall()
                else:
                    connection.commit()
                    result = cursor.lastrowid
                
                cursor.close()
                return result
            except Error as e:
                print(f"❌ Error ejecutando query: {e}")
                return None
        return None

# Instancia global de base de datos
db = Database()