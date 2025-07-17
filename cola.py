from collections import deque

class ColaClientes:
    def __init__(self):
        #Inicializa una cola vacía de clientes.
        self.cola = deque()

    def agregar_cliente(self, cliente):
        #Agrega un cliente al final de la cola.
        self.cola.append(cliente)

    def siguiente_cliente(self):
        #Remueve y retorna el siguiente cliente en la cola. Si está vacía, retorna None.
        if self.cola:
            return self.cola.popleft()
        return None

    def ver_siguiente(self):
        #Retorna el siguiente cliente sin removerlo. Si está vacía, retorna None.
        if self.cola:
            return self.cola[0]
        return None

    def tamano(self):
        #Retorna el número de clientes en la cola.
        return len(self.cola)

    def limpiar(self):
        #Limpia toda la cola de clientes.
        self.cola.clear()

    def listar_clientes(self):
        #Retorna una lista de todos los clientes en la cola (en orden).
        return list(self.cola)