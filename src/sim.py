from process import Proceso
from tabulate import tabulate
from reader import read_data

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

    def unshift(self):
        if self.largo == 0:
            print("La cola está vacía")
            return

        item = self.buffer[self.head]
        # Revisar en la definición de unshift, cómo liberar la memoria que deja de estar contenida entre head y tail.
        self.head = (self.head + 1) % self.tamaño
        self.largo -= 1
        return item


def cargar_desde_archivo(destino: ColaCircular, fuente):
    """
    Se carga la cola a partir de un dictionary con los datos del archivo.
    """
    data = read_data(fuente)

    for p in data.values():
        proceso = Proceso(p)
        if proceso.get_tamaño() <= 250:
            destino.shift(proceso)
        continue

    destino.buffer.sort(key=lambda x: x.get_tiempo_arribo())


def cargar_desde_cola(destino: ColaCircular, fuente: ColaCircular):
    """
    Se carga una cola a partir de otra.
    Los elementos de source cargados son retirados de la cola original.
    """
    for _ in range(5):
        # Revisar en la definición de unshift, cómo liberar la memoria que dejar de estar contenida entre head y tail.
        proceso = fuente.unshift()
        destino.shift(proceso)
