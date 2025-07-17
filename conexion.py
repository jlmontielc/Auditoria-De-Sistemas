import mysql.connector

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'mi_usuario',
    'password': 'auditoriaJorge1234',
    'database': 'dbAuditoria'
}

def obtener_conexion():
    #Retorna una conexión a la base de datos.
    return mysql.connector.connect(**DB_CONFIG)

def obtener_cursor():
    #Retorna una tupla (conn, cursor) para usar en bloques try/finally.
    conn = obtener_conexion()
    cursor = conn.cursor()
    return conn, cursor

def cerrar_conexion(conn, cursor=None):
    #Cierra el cursor y la conexión si están abiertos.
    if cursor:
        try:
            cursor.close()
        except Exception:
            pass
    if conn:
        try:
            conn.close()
        except Exception:
            pass

def crear_tablas():
    #Crea las tablas necesarias si no existen.
    conn, cursor = obtener_cursor()
    # Tabla de clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cedula VARCHAR(20) UNIQUE NOT NULL,
            nombre VARCHAR(100),
            email VARCHAR(100),
            telefono VARCHAR(20),
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Tabla de compras
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS compra (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cliente_id INT NOT NULL,
            fecha_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            cantidad_productos INT NOT NULL,
            total DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    ''')
    # Tabla de pagos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pagos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            compra_id INT NOT NULL,
            metodo_pago VARCHAR(100) NOT NULL,
            monto DECIMAL(10,2) NOT NULL,
            fecha_pago TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (compra_id) REFERENCES compra(id)
        )
    ''')
    conn.commit()
    cerrar_conexion(conn, cursor)

if __name__ == "__main__":
    crear_tablas()
    print("Tablas creadas correctamente.") 