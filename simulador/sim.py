from abc import ABC
from process import Process
from tabulate import tabulate
from reader import read_data


def print_table(title: str, data: list[Process], headers: list) -> None:
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

    def add_process(self, process: Process):
        if self._capacity == self._lenght:
            return False

        self._lenght += 1
        self._data.append(process)

    def load_from_file(self, file):
        data = read_data(file)

        for p in data.values():
            if self._capacity == self._lenght:
                break 

            self._lenght += 1
            self._data.append(Process(p))

        self._data = [p for p in self._data if p.get_size() <= 250]
        self._data.sort(key=lambda x: x.get_ta())

    def load_from_queue(self, source):
        loaded_items = []
        for item in source._data:
            if self._capacity == self._lenght:
                break

            self._lenght += 1
            self._data.append(item)
            loaded_items.append(item)

        source._data = [item for item in source._data if item not in loaded_items]
