import mysql.connector
from cliente import Cliente
from conexion import obtener_cursor, cerrar_conexion

class Caja:
    def guardar_o_actualizar_cliente(self, cliente):
        cliente.guardar()

    def procesar_pago(self, compra_id, metodo_pago, monto):
        #Registra un pago para una compra existente.
        conn, cursor = obtener_cursor()
        try:
            cursor.execute('''
                INSERT INTO pagos (compra_id, metodo_pago, monto)
                VALUES (%s, %s, %s)
            ''', (compra_id, metodo_pago, monto))
            conn.commit()
            print(f"Pago procesado para la compra {compra_id} por {monto}$ usando {metodo_pago}")
        finally:
            cerrar_conexion(conn, cursor)

    def generar_reporte(self):
        #Muestra un reporte de todos los pagos realizados, con datos de cliente y compra.
        conn, cursor = obtener_cursor()
        try:
            print("=== REPORTE DE PAGOS ===")
            cursor.execute('''
                SELECT c.cedula, c.nombre, co.id, co.total, p.metodo_pago, p.monto, p.fecha_pago
                FROM pagos p
                JOIN compra co ON p.compra_id = co.id
                JOIN clientes c ON co.cliente_id = c.id
                ORDER BY p.id
            ''')
            pagos = cursor.fetchall()
            for pago in pagos:
                print(f"Cédula: {pago[0]}, Nombre: {pago[1]}, Compra ID: {pago[2]}, Total compra: {pago[3]}, Monto pagado: {pago[5]}, Método: {pago[4]}, Fecha: {pago[6]}")
            print("========================")
        finally:
            cerrar_conexion(conn, cursor)
