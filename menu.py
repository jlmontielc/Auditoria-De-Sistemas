from cliente import Cliente

def mostrar_menu(caja, cola):
    while True:
        print("\n=== MENÚ ===")
        print("1. Crear cliente")
        print("2. Atender cliente")
        print("3. Ver clientes en cola")
        print("4. Ver reporte de pagos")
        print("5. Ver todos los clientes registrados")
        print("6. Cerrar caja")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            cedula = input("Ingrese la cédula del cliente: ")
            cantidad = int(input("Ingrese la cantidad: "))
            monto = float(input("Ingrese el monto en $: "))
            nuevo_cliente = Cliente(cedula=cedula, cantidad=cantidad, monto=monto)
            nuevo_cliente.guardar()  # Guardar en la base de datos
            cola.agregar_cliente(nuevo_cliente)
            print("Cliente agregado a la cola y guardado en la base de datos.")
        elif opcion == "2":
            cliente = cola.siguiente_cliente()
            if cliente:
                while True:
                    print("\nMétodos de pago disponibles:")
                    print("1. Efectivo")
                    print("2. Tarjeta")
                    print("3. Pago movil")
                    metodo_pago = input("Seleccione el método de pago (1, 2, 3): ")
                    
                    if metodo_pago == "1":
                        metodo_pago = "Efectivo"
                        break
                    elif metodo_pago == "2":
                        metodo_pago = "Tarjeta"
                        break
                    elif metodo_pago == "3":
                        metodo_pago = "Pago movil"
                        break
                    else:
                        print("Opción no válida. Por favor seleccione 1 para Efectivo, 2 para Tarjeta o 3 para Pago movil.")
                caja.procesar_pago(cliente, metodo_pago=metodo_pago)
            else:
                print("No hay clientes en la cola.")
        elif opcion == "3":
            if cola.cola:
                print("Clientes en cola:")
                for idx, cliente in enumerate(cola.cola, 1):
                    print(f"{idx}. Cédula: {cliente.cedula}, Cantidad: {cliente.cantidad}, Monto: {cliente.monto}")
            else:
                print("No hay clientes en la cola.")
        elif opcion == "4":
            caja.generar_reporte()
        elif opcion == "5":
            # Mostrar todos los clientes registrados en la base de datos
            from conexion import obtener_conexion
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute('SELECT cedula, cantidad, monto FROM clientes')
            clientes = cursor.fetchall()
            print("=== CLIENTES REGISTRADOS ===")
            for idx, cliente in enumerate(clientes, 1):
                print(f"{idx}. Cédula: {cliente[0]}, Cantidad: {cliente[1]}, Monto: {cliente[2]}")
            if not clientes:
                print("No hay clientes registrados en la base de datos.")
            print("============================")
            cursor.close()
            conn.close()
        elif opcion == "6":
            if cola.cola:
                print(f"Cerrando caja. Se eliminarán {len(cola.cola)} clientes de la cola.")
                cola.cola.clear()
            else:
                print("No hay clientes en la cola.")
        elif opcion == "7":
            if cola.cola:
                confirmar = input("Aún hay clientes en la cola. ¿Seguro que desea salir? (s/n): ")
                if confirmar.lower() != "s":
                    continue
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")