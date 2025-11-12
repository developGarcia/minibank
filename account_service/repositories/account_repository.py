# account_service/repositories/account_repository.py
from database import db

class AccountRepository:
    def __init__(self):
        self.db = db
    
    def find_account_by_id(self, account_id):
        """Buscar cuenta por ID"""
        query = "SELECT * FROM cuentas WHERE id = ? AND estado = 'activa'"
        result = self.db.execute_query(query, (account_id,))
        return result[0] if result else None
    
    def find_accounts_by_customer(self, customer_id):
        """Obtener todas las cuentas de un cliente"""
        query = "SELECT * FROM cuentas WHERE cliente_id = ? AND estado = 'activa'"
        return self.db.execute_query(query, (customer_id,))
    
    def update_account_balance(self, account_id, new_balance):
        """Actualizar saldo de cuenta"""
        query = "UPDATE cuentas SET saldo = ? WHERE id = ?"
        result = self.db.execute_query(query, (new_balance, account_id))
        return result is not None
    
    def create_transaction(self, cuenta_id, tipo, monto, descripcion=""):
        """Crear nueva transacción"""
        query = "INSERT INTO transacciones (cuenta_id, tipo, monto, descripcion) VALUES (?, ?, ?, ?)"
        return self.db.execute_query(query, (cuenta_id, tipo, monto, descripcion))
    
    def find_transactions_by_account(self, account_id, limit=10):
        """Obtener transacciones de una cuenta"""
        query = "SELECT * FROM transacciones WHERE cuenta_id = ? ORDER BY fecha DESC LIMIT ?"
        return self.db.execute_query(query, (account_id, limit))
    
    def account_exists(self, account_id):
        """Verificar si cuenta existe"""
        query = "SELECT id FROM cuentas WHERE id = ? AND estado = 'activa'"
        result = self.db.execute_query(query, (account_id,))
        return bool(result)