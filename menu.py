from cliente import Cliente
from compra import Compra
from pagos import Pago
from caja import Caja
from cola import ColaClientes
import re
import os

class Utilidades:
    @staticmethod
    def limpiar_pantalla():
        os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    caja = Caja()
    cola = ColaClientes()
    while True:
        Utilidades.limpiar_pantalla()
        print("\n=== MENÚ ===")
        print(f"Clientes en cola: {cola.tamano()}")
        print("1. Registrar cliente")
        print("2. Registrar compra y pago")
        print("3. Ver clientes en cola")
        print("4. Ver clientes registrados")
        print("5. Ver compras de un cliente")
        print("6. Ver pagos de una compra")
        print("7. Reportes totales")
        print("8. Exportar transacciones a TXT")
        print("9. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Validación de cédula
            while True:
                cedula = input("Cédula: ")
                if re.match(r'^(?:(?:[1-9][0-9]{0,7})|100000000)$', cedula):
                    break
                else:
                    print("Cédula inválida.")
            nombre = input("Nombre: ")
            # Validación de email
            while True:
                email = input("Email: ")
                if re.match(r'^[^@]+@[^@]+\.[a-zA-Z]{2,}$', email):
                    break
                else:
                    print("Correo electrónico inválido. Ingrese un correo válido.")
            telefono = input("Teléfono: ")
            cliente = Cliente(cedula=cedula, nombre=nombre, email=email, telefono=telefono)
            cliente.guardar()
            cola.agregar_cliente(cliente)
            print("Cliente registrado correctamente.")
            input("Presione Enter para continuar...")
        elif opcion == "2":
            cliente = cola.siguiente_cliente()
            if not cliente:
                print("Cliente no encontrado.")
                input("Presione Enter para continuar...")
                continue
            # Verificar si el cliente tiene una compra sin pagar
            from conexion import obtener_conexion
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.id FROM compra c
                LEFT JOIN pagos p ON c.id = p.compra_id
                WHERE c.cliente_id = %s
                GROUP BY c.id
                HAVING COUNT(p.id) = 0
            ''', (cliente.id,))
            compra_sin_pagar = cursor.fetchone()
            cursor.close()
            conn.close()
            if compra_sin_pagar:
                print("Este cliente ya tiene una compra sin pagar. No puede registrar otra compra hasta que pague la anterior.")
                input("Presione Enter para continuar...")
                continue
            cantidad = int(input(f"Cantidad de productos para {cliente.nombre}: "))
            total = float(input(f"Total de la compra para {cliente.nombre}: $"))
            compra = Compra(cliente_id=cliente.id, cantidad_productos=cantidad, total=total)
            compra.guardar()
            print(f"Compra registrada correctamente para {cliente.nombre}.")
            # Registrar el pago inmediatamente usando Caja
            print(f"El monto a pagar por la compra {compra.id} es: ${total}")
            while True:
                print("Métodos de pago disponibles:")
                print("1. Efectivo")
                print("2. Tarjeta")
                print("3. Pago movil")
                metodo = input("Seleccione el método de pago (1, 2, 3): ")
                if metodo == "1":
                    metodo_pago = "efectivo"
                    break
                elif metodo == "2":
                    metodo_pago = "tarjeta"
                    break
                elif metodo == "3":
                    metodo_pago = "pago movil"
                    break
                else:
                    print("Opción no válida. Vuelva a elegir 1, 2 o 3.")
            caja.procesar_pago(compra.id, metodo_pago, total)
            print("Pago registrado correctamente.")
            input("Presione Enter para continuar...")
        elif opcion == "3":
            print("=== CLIENTES EN COLA ===")
            for idx, cliente in enumerate(cola.listar_clientes(), 1):
                print(f"{idx}. Cédula: {cliente.cedula}, Nombre: {cliente.nombre}, Email: {cliente.email}, Teléfono: {cliente.telefono}")
            if cola.tamano() == 0:
                print("No hay clientes en la cola.")
            print("=========================")
            input("Presione Enter para continuar...")
        elif opcion == "4":
            from conexion import obtener_conexion
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute('SELECT cedula, nombre, email, telefono, fecha_registro FROM clientes')
            clientes = cursor.fetchall()
            print("=== CLIENTES REGISTRADOS ===")
            for c in clientes:
                print(f"Cédula: {c[0]}, Nombre: {c[1]}, Email: {c[2]}, Teléfono: {c[3]}, Fecha registro: {c[4]}")
            if not clientes:
                print("No hay clientes registrados.")
            print("============================")
            cursor.close()
            conn.close()
            input("Presione Enter para continuar...")
        elif opcion == "5":
            cedula = input("Cédula del cliente: ")
            cliente = Cliente.obtener_por_cedula(cedula)
            if not cliente:
                print("Cliente no encontrado.")
                input("Presione Enter para continuar...")
                continue
            compras = Compra.obtener_por_cliente(cliente.id)
            print(f"=== COMPRAS DE {cliente.nombre} ===")
            for compra in compras:
                print(f"ID: {compra.id}, Fecha: {compra.fecha_compra}, Cantidad productos: {compra.cantidad_productos}, Total: {compra.total}")
            if not compras:
                print("No hay compras registradas para este cliente.")
            print("============================")
            input("Presione Enter para continuar...")
        elif opcion == "6":
            compra_id = int(input("ID de la compra: "))
            pagos = Pago.obtener_por_compra(compra_id)
            print(f"=== PAGOS DE LA COMPRA {compra_id} ===")
            for pago in pagos:
                print(f"ID: {pago.id}, Método: {pago.metodo_pago}, Monto: {pago.monto}, Fecha: {pago.fecha_pago}")
            if not pagos:
                print("No hay pagos registrados para esta compra.")
            print("============================")
            input("Presione Enter para continuar...")
        elif opcion == "7":
            caja.generar_reporte()
            input("Presione Enter para continuar...")
        elif opcion == "8":
            from conexion import obtener_conexion
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.id, p.compra_id, p.metodo_pago, p.monto, p.fecha_pago, c.cedula, c.nombre, c.email
                FROM pagos p
                JOIN compra co ON p.compra_id = co.id
                JOIN clientes c ON co.cliente_id = c.id
                ORDER BY p.id
            ''')
            pagos = cursor.fetchall()
            cursor.close()
            conn.close()
            with open('transacciones.txt', 'w', encoding='utf-8') as f:
                f.write('ID Pago | ID Compra | Método de Pago | Monto | Fecha de Pago | Cédula | Nombre | Email\n')
                f.write('-'*90 + '\n')
                for pago in pagos:
                    f.write(f'{pago[0]} | {pago[1]} | {pago[2]} | ${pago[3]} | {pago[4]} | {pago[5]} | {pago[6]} | {pago[7]}\n')
            print('Transacciones exportadas a transacciones.txt')
            input("Presione Enter para continuar...")
        elif opcion == "9":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")