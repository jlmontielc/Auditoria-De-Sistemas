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
    return mysql.connector.connect(**DB_CONFIG)

def crear_tablas():
    conn = obtener_conexion()
    cursor = conn.cursor()
    # Tabla de clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cedula VARCHAR(20) UNIQUE,
            cantidad INT,
            monto FLOAT
        )
    ''')
    # Tabla de pagos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pagos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cedula VARCHAR(20),
            cantidad INT,
            monto FLOAT,
            metodo_pago VARCHAR(20),
            FOREIGN KEY (cedula) REFERENCES clientes(cedula)
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    crear_tablas()
    print("Tablas creadas correctamente.") 