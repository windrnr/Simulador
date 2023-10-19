from abc import ABC
from process import Process
from tabulate import tabulate
from reader import read_data


def print_table(title: str, data: list[Process], headers: list) -> None:
    """
    Imprime por pantalla una tabla con los procesos dentro de una lista.
    """
    outer = []
    for process in data:
        outer.append(process.return_list_of_data())

    print(
        f"{title}\n"
        + tabulate(outer, headers, tablefmt="fancy_outline", stralign="center")
    )


class Queue(ABC):
    def __init__(self, capacity: int) -> None:
        self._capacity: int = capacity
        self._lenght: int = 0
        self._data: list[Process] = []

    def load_from_file(self, file):
        """
        Se carga la lista a partir de un dictionary con los datos del archivo.
        """
        data = read_data(file)

        for p in data.values():
            if self._capacity == self._lenght:
                break

            self._lenght += 1
            self._data.append(Process(p))

        self._data = [p for p in self._data if p.get_tamaño() <= 250]
        self._data.sort(key=lambda x: x.get_tiempo_arribo())

    def load_from_queue(self, source):
        """
        Se carga una lista a partir de otra.
        Los elementos cargados son retirados de la lista original.
        """
        loaded_items = []
        for item in source._data:
            if self._capacity == self._lenght:
                break

            self._lenght += 1
            self._data.append(item)
            loaded_items.append(item)

        source._data = [item for item in source._data if item not in loaded_items]
