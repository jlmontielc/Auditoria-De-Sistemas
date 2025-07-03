from cliente import Cliente

def mostrar_menu(caja, cola):
    while True:
        print("\n=== MENÚ ===")
        print("1. Crear cliente")
        print("2. Atender cliente")
        print("3. Ver clientes en cola")
        print("4. Ver reporte de pagos")
        print("5. Cerrar caja")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            cedula = input("Ingrese la cédula del cliente: ")
            cantidad = int(input("Ingrese la cantidad: "))
            monto = float(input("Ingrese el monto en $: "))
            nuevo_cliente = Cliente(cedula=cedula, cantidad=cantidad, monto=monto)
            cola.agregar_cliente(nuevo_cliente)
            print("Cliente agregado a la cola.")
        elif opcion == "2":
            cliente = cola.siguiente_cliente()
            if cliente:
                metodo_pago = input("Ingrese el método de pago: ")
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
            if cola.cola:
                print(f"Cerrando caja. Se eliminarán {len(cola.cola)} clientes de la cola.")
                cola.cola.clear()
            else:
                print("No hay clientes en la cola.")
        elif opcion == "6":
            if cola.cola:
                confirmar = input("Aún hay clientes en la cola. ¿Seguro que desea salir? (s/n): ")
                if confirmar.lower() != "s":
                    continue
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")