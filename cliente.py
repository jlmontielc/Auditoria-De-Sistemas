from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    cedula = Column(String(20), unique=True)
    cantidad = Column(Integer)
    monto = Column(Float)

    def __init__(self, cedula, cantidad, monto):
        self.cedula = cedula
        self.cantidad = cantidad
        self.monto = monto