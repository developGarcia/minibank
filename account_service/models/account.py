"""
MODELOS DE DOMINIO - Account Service
Nivel C4: Código (Entidades)
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Account:
    id: int
    numero_cuenta: str
    cliente_id: int
    saldo: float
    tipo: str
    estado: str
    fecha_creacion: str
    
    def tiene_fondos_suficientes(self, monto: float) -> bool:
        return self.saldo >= monto
    
    def puede_recibir_deposito(self, monto: float) -> bool:
        return monto > 0 and self.estado == 'activa'

@dataclass
class Transaction:
    id: int
    cuenta_id: int
    tipo: str  # 'deposito', 'retiro'
    monto: float
    descripcion: str
    fecha: str
    
    def es_deposito(self) -> bool:
        return self.tipo == 'deposito'
    
    def es_retiro(self) -> bool:
        return self.tipo == 'retiro'

@dataclass
class CustomerAccounts:
    cliente_id: int
    cuentas: List[Account]
    saldo_total: float
    
    def calcular_saldo_total(self) -> float:
        return sum(cuenta.saldo for cuenta in self.cuentas)