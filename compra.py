from conexion import obtener_conexion

class Compra:
    def __init__(self, cliente_id, cantidad_productos, total, id=None, fecha_compra=None):
        self.id = id
        self.cliente_id = cliente_id
        self.cantidad_productos = cantidad_productos
        self.total = total
        self.fecha_compra = fecha_compra

    def guardar(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO compra (cliente_id, cantidad_productos, total)
            VALUES (%s, %s, %s)
        ''', (self.cliente_id, self.cantidad_productos, self.total))
        conn.commit()
        self.id = cursor.lastrowid
        cursor.close()
        conn.close()

    @staticmethod
    def obtener_por_cliente(cliente_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('SELECT id, cliente_id, fecha_compra, cantidad_productos, total FROM compra WHERE cliente_id = %s', (cliente_id,))
        compras = []
        for row in cursor.fetchall():
            compras.append(Compra(id=row[0], cliente_id=row[1], fecha_compra=row[2], cantidad_productos=row[3], total=row[4]))
        cursor.close()
        conn.close()
        return compras 