from conexion import obtener_conexion

class Cliente:
    def __init__(self, cedula, nombre, email, telefono, id=None, fecha_registro=None):
        self.id = id
        self.cedula = cedula
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.fecha_registro = fecha_registro

    def guardar(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clientes (cedula, nombre, email, telefono)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE nombre=%s, email=%s, telefono=%s
        ''', (self.cedula, self.nombre, self.email, self.telefono, self.nombre, self.email, self.telefono))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def obtener_por_cedula(cedula):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('SELECT id, cedula, nombre, email, telefono, fecha_registro FROM clientes WHERE cedula = %s', (cedula,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return Cliente(id=row[0], cedula=row[1], nombre=row[2], email=row[3], telefono=row[4], fecha_registro=row[5])
        return None