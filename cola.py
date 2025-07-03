from collections import deque

class ColaClientes:
    def __init__(self):
        self.cola = deque()

    def agregar_cliente(self, cliente):
        self.cola.append(cliente)

    def siguiente_cliente(self):
        if self.cola:
            return self.cola.popleft()
        return None