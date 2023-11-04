from tabulate import tabulate
from reader import read_data

class Memoria:
    def __init__(self, layout: list):
        self.particiones: list[Particion] = layout[1:]

class Particion:
    def __init__(self, tamaño: int):
        self.tamaño: int = tamaño
        self.frag_interna: int = 0
        self.proceso: Proceso | None = None


class Proceso:
    def __init__(self, data: list[int]):
        self.pid:int = data[0]
        self.tamaño:int  = data[1]
        self.tiempo_arribo: int = data[2]
        self.tiempo_irrupcion: int = data[3]
        self.estado = "Nuevo"
        self.particion: Particion | None = None

    def return_list_of_data(self) -> list:
        data = []
        data.append(self.pid)
        data.append(self.tamaño)
        data.append(self.tiempo_arribo)
        data.append(self.tiempo_irrupcion)

        return data


class ColaCircular:
    def __init__(self, tamaño: int):
        self.tamaño = tamaño
        self.largo = 0
        # Revisar si esto es la mejor idea, lo hice así porque no puedo indexar una lista vacía en python.
        # Me parece que puede llegar a traer errores cuando querramos sacar datos del rendimiento del simulador.
        self.buffer = [Proceso([0, 0, 0, 0])] * tamaño
        self.tail = self.head = 0

    def shift(self, item) -> None:
        if self.largo == self.tamaño:
            print("La cola está llena")
            return

        self.buffer[self.tail] = item
        self.tail = (self.tail + 1) % self.tamaño
        self.largo += 1

    def unshift(self) -> Proceso | None:
        if self.largo == 0:
            print("La cola está vacía")
            return

        item = self.buffer[self.head]
        # Revisar en la definición de unshift, cómo liberar la memoria que deja de estar contenida entre head y tail.
        self.head = (self.head + 1) % self.tamaño
        self.largo -= 1
        return item

    def peek(self):
        return self.buffer[self.head]


def cargar_desde_archivo(destino: ColaCircular, fuente):
    """
    Se carga la cola a partir de un dictionary con los datos del archivo.
    """
    data = read_data(fuente)

    for p in data.values():
        proceso = Proceso(p)
        if proceso.tamaño <= 250:
            destino.shift(proceso)
        continue

    destino.buffer.sort(key=lambda x: x.tiempo_arribo)


# Puede ser que lo borramos
def cargar_desde_cola(destino: ColaCircular, fuente: ColaCircular):
    """
    Se carga una cola a partir de otra.
    Los elementos de source cargados son retirados de la cola original.
    """
    for _ in range(5):
        # Revisar en la definición de unshift, cómo liberar la memoria que dejar de estar contenida entre head y tail.
        proceso = fuente.unshift()
        destino.shift(proceso)


def print_table(title: str, data: list[Proceso], headers: list) -> None:
    """
    Imprime por pantalla una tabla con los procesos dentro de una lista.
    """
    outer = []
    for proceso in data:
        outer.append(proceso.return_list_of_data())

    print(
        f"{title}\n"
        + tabulate(outer, headers, tablefmt="fancy_outline", stralign="center")
    )
