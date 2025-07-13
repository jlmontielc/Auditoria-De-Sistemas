from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from cliente import Cliente

Base = declarative_base()

class Caja:
    def __init__(self):
        self.pagos = []

    def procesar_pago(self, cliente, metodo_pago):
        # Guarda la información del pago realizado
        self.pagos.append({
            "cedula": cliente.cedula,
            "cantidad": cliente.cantidad,
            "monto": cliente.monto,
            "metodo_pago": metodo_pago
        })
        print(f"Pago procesado para {cliente.cedula} por {cliente.monto}$ usando {metodo_pago}")

    def generar_reporte(self):
        print("=== REPORTE DE PAGOS ===")
        for pago in self.pagos:
            print(f"Cédula: {pago['cedula']}, Cantidad: {pago['cantidad']}, Monto: {pago['monto']}, Método: {pago['metodo_pago']}")
        print("========================")
