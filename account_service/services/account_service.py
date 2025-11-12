# account_service/services/account_service.py
from repositories.account_repository import AccountRepository

class AccountService:
    def __init__(self):
        self.repository = AccountRepository()
    
    def get_account(self, account_id):
        """Obtener información de una cuenta"""
        account = self.repository.find_account_by_id(account_id)
        if account:
            return {
                'success': True,
                'cuenta': account
            }
        return {
            'success': False,
            'error': 'Cuenta no encontrada'
        }
    
    def get_customer_accounts(self, customer_id):
        """Obtener todas las cuentas de un cliente"""
        accounts = self.repository.find_accounts_by_customer(customer_id)
        return {
            'success': True,
            'cliente_id': customer_id,
            'cuentas': accounts,
            'total_cuentas': len(accounts)
        }
    
    def deposit(self, account_id, amount, description=""):
        """Realizar depósito"""
        if amount <= 0:
            return {'success': False, 'error': 'Monto debe ser mayor a 0'}
        
        account = self.repository.find_account_by_id(account_id)
        if not account:
            return {'success': False, 'error': 'Cuenta no encontrada'}
        
        nuevo_saldo = account['saldo'] + amount
        
        if self.repository.update_account_balance(account_id, nuevo_saldo):
            transaction_id = self.repository.create_transaction(
                account_id, 'deposito', amount, description
            )
            return {
                'success': True,
                'transaccion_id': transaction_id,
                'saldo_anterior': account['saldo'],
                'saldo_nuevo': nuevo_saldo,
                'monto': amount
            }
        
        return {'success': False, 'error': 'Error en transacción'}
    
    def withdraw(self, account_id, amount, description=""):
        """Realizar retiro"""
        if amount <= 0:
            return {'success': False, 'error': 'Monto debe ser mayor a 0'}
        
        account = self.repository.find_account_by_id(account_id)
        if not account:
            return {'success': False, 'error': 'Cuenta no encontrada'}
        
        if account['saldo'] < amount:
            return {'success': False, 'error': 'Fondos insuficientes'}
        
        nuevo_saldo = account['saldo'] - amount
        
        if self.repository.update_account_balance(account_id, nuevo_saldo):
            transaction_id = self.repository.create_transaction(
                account_id, 'retiro', amount, description
            )
            return {
                'success': True,
                'transaccion_id': transaction_id,
                'saldo_anterior': account['saldo'],
                'saldo_nuevo': nuevo_saldo,
                'monto': amount
            }
        
        return {'success': False, 'error': 'Error en transacción'}
    
    def get_account_transactions(self, account_id, limit=10):
        """Obtener historial de transacciones"""
        if not self.repository.account_exists(account_id):
            return {'success': False, 'error': 'Cuenta no encontrada'}
        
        transactions = self.repository.find_transactions_by_account(account_id, limit)
        return {
            'success': True,
            'cuenta_id': account_id,
            'transacciones': transactions,
            'total': len(transactions)
        }