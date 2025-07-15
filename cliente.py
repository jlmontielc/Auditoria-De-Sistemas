from conexion import obtener_conexion

class Cliente:
    def __init__(self, cedula, cantidad, monto, id=None):
        self.id = id
        self.cedula = cedula
        self.cantidad = cantidad
        self.monto = monto

    def guardar(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clientes (cedula, cantidad, monto)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE cantidad=%s, monto=%s
        ''', (self.cedula, self.cantidad, self.monto, self.cantidad, self.monto))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def obtener_por_cedula(cedula):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('SELECT id, cedula, cantidad, monto FROM clientes WHERE cedula = %s', (cedula,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return Cliente(id=row[0], cedula=row[1], cantidad=row[2], monto=row[3])
        return None