from conexion import obtener_conexion

class Pago:
    def __init__(self, compra_id, metodo_pago, monto, id=None, fecha_pago=None):
        self.id = id
        self.compra_id = compra_id
        self.metodo_pago = metodo_pago
        self.monto = monto
        self.fecha_pago = fecha_pago

    def guardar(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO pagos (compra_id, metodo_pago, monto)
            VALUES (%s, %s, %s)
        ''', (self.compra_id, self.metodo_pago, self.monto))
        conn.commit()
        self.id = cursor.lastrowid
        cursor.close()
        conn.close()

    @staticmethod
    def obtener_por_compra(compra_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('SELECT id, compra_id, metodo_pago, monto, fecha_pago FROM pagos WHERE compra_id = %s', (compra_id,))
        pagos = []
        for row in cursor.fetchall():
            pagos.append(Pago(id=row[0], compra_id=row[1], metodo_pago=row[2], monto=row[3], fecha_pago=row[4]))
        cursor.close()
        conn.close()
        return pagos 