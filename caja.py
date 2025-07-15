import mysql.connector
from cliente import Cliente
from conexion import obtener_conexion

class Caja:
    def __init__(self):
        self.conn = obtener_conexion()

    def guardar_o_actualizar_cliente(self, cliente):
        cliente.guardar()

    def procesar_pago(self, cliente, metodo_pago):
        self.guardar_o_actualizar_cliente(cliente)
        # Obtener el id del cliente
        cliente_db = Cliente.obtener_por_cedula(cliente.cedula)
        if not cliente_db:
            print(f"No se encontró el cliente con cédula {cliente.cedula} en la base de datos.")
            return
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO pagos (cliente_id, metodo_pago)
            VALUES (%s, %s)
        ''', (cliente_db.id, metodo_pago))
        self.conn.commit()
        cursor.close()
        print(f"Pago procesado para {cliente.cedula} por {cliente.monto}$ usando {metodo_pago}")

    def generar_reporte(self):
        cursor = self.conn.cursor()
        print("=== REPORTE DE PAGOS ===")
        cursor.execute('''
            SELECT c.cedula, c.cantidad, c.monto, p.metodo_pago, p.fecha
            FROM pagos p
            JOIN clientes c ON p.cliente_id = c.id
            ORDER BY p.id
        ''')
        pagos = cursor.fetchall()
        for pago in pagos:
            print(f"Cédula: {pago[0]}, Cantidad: {pago[1]}, Monto: {pago[2]}, Método: {pago[3]}, Fecha: {pago[4]}")
        print("========================")
        cursor.close()

    def __del__(self):
        if self.conn.is_connected():
            self.conn.close()
