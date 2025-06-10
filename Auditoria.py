class Cliente:
    def __init__(self, cedula, cantidad_productos, monto):
        self.cedula = cedula
        self.cantidad_productos = cantidad_productos
        self.monto = monto
        self.siguiente = None  

primero = None
ultimo = None
clientes_atendidos = 0
pagado_tdd = 0.0
pagado_efectivo = 0.0
total_pagado = 0.0

def mostrar_menu():
    """Muestra el menú y retorna la opción seleccionada."""
    print("\n1. Crear cliente")
    print("2. Atender cliente")
    print("3. Ver cola")
    print("4. Ver reporte")
    print("5. Cerrar caja")
    print("6. Salir")
    while True:
        try:
            opcion = int(input("Seleccione una opción: "))
            return opcion
        except ValueError:
            print("Por favor, ingrese un número válido.")

def crear_cliente():
    """Crea un nuevo cliente y lo añade al final de la cola."""
    global primero, ultimo

    print("\nCrear cliente:")
    cedula = input("Cédula del cliente: ")
    while True:
        try:
            cantidad_productos = int(input("Cantidad de productos: "))
            if cantidad_productos < 0:
                print("La cantidad de productos no puede ser negativa.")
                continue
            break
        except ValueError:
            print("Por favor, ingrese un número entero para la cantidad.")

    while True:
        try:
            monto = float(input("Monto a pagar en $: "))
            if monto < 0:
                print("El monto no puede ser negativo.")
                continue
            break
        except ValueError:
            print("Por favor, ingrese un número para el monto.")

    nuevo_cliente = Cliente(cedula, cantidad_productos, monto)

    if primero is None: 
        primero = ultimo = nuevo_cliente
    else:
        ultimo.siguiente = nuevo_cliente
        ultimo = nuevo_cliente
    print("Cliente agregado a la cola.")

def atender_cliente():
    """Atiende al primer cliente de la cola."""
    global primero, ultimo, clientes_atendidos, pagado_tdd, pagado_efectivo, total_pagado

    if primero is None:
        print("No hay clientes en cola.")
        return

    cliente_atendido = primero
    primero = primero.siguiente
    if primero is None:
        ultimo = None

    while True:
        forma_pago = input(f"Cliente: {cliente_atendido.cedula}, Monto: ${cliente_atendido.monto:.2f}\nForma de pago (1 = Efectivo, 2 = TDD): ").upper()
        if forma_pago == '1':
            pagado_efectivo += cliente_atendido.monto
            break
        elif forma_pago == '2':
            pagado_tdd += cliente_atendido.monto
            break
        else:
            print("Forma de pago no válida. Intente de nuevo.")
            print("--------------------------------")

    clientes_atendidos += 1
    total_pagado += cliente_atendido.monto
    
    print("Cliente atendido correctamente.")


def ver_cola():
    """Muestra los clientes actualmente en la cola."""
    if primero is None:
        print("No hay clientes en cola.")
        return

    print("\nClientes en cola:")
    actual = primero
    contador = 1
    while actual is not None:
        print(f"{contador}. Cédula: {actual.cedula}, Cantidad de productos: {actual.cantidad_productos}, Monto: ${actual.monto:.2f}")
        actual = actual.siguiente
        contador += 1

def ver_reporte():
    """Muestra un reporte de la actividad de la caja."""
    print("\n--- Reporte de Caja ---")
    print(f"Total de clientes atendidos: {clientes_atendidos}")

    clientes_en_cola = 0
    actual = primero
    while actual is not None:
        clientes_en_cola += 1
        actual = actual.siguiente
    print(f"Cantidad de clientes en cola: {clientes_en_cola}")

    print(f"Total facturado - General: ${total_pagado:.2f}")
    print(f"Total facturado - Efectivo: ${pagado_efectivo:.2f}")
    print(f"Total facturado - TDD: ${pagado_tdd:.2f}")
    print("-----------------------")

def cerrar_caja():
    """Elimina todos los clientes de la cola."""
    global primero, ultimo
    primero = None
    ultimo = None
    print("Caja cerrada. Todos los clientes eliminados de la cola.")

def salir_programa():
    """Sale del programa, verificando si hay clientes en cola."""
    global primero
    if primero is not None:
        respuesta = input("Aún hay clientes en cola. ¿Desea salir? (1 = Si / 2 = No): ").upper()
        if respuesta == '2':
            return False 
        elif respuesta == '1':
            cerrar_caja() 
            print("Cerrado correctamente.")
            return True 
        else:
            print("Respuesta no válida.")
            return False 
    else:
        print("Cerrado correctamente.")
        return True 

def main():
    """Función principal que ejecuta el menú y las opciones."""
    while True:
        opcion = mostrar_menu()
        if opcion == 1:
            crear_cliente()
        elif opcion == 2:
            atender_cliente()
        elif opcion == 3:
            ver_cola()
        elif opcion == 4:
            ver_reporte()
        elif opcion == 5:
            cerrar_caja()
        elif opcion == 6:
            if salir_programa():
                break # Rompe el bucle while y termina el programa
        else:
            print("Opción incorrecta. Intente de nuevo.")
        print("--------------------------------")

if __name__ == "__main__":
    main()