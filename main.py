from caja import Caja
from cola import ColaClientes
from menu import mostrar_menu

if __name__ == "__main__":
    caja = Caja()
    cola = ColaClientes()
    mostrar_menu(caja, cola)
