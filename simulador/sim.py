from abc import ABC
from process import Process
from tabulate import tabulate

def print_table(title: str,data: list[Process], headers: list) -> None:
    outer = []
    for process in data:
        outer.append(process.return_list_of_data())

    print(f"{title}\n" + tabulate(outer, headers, tablefmt="fancy_outline", stralign='center'))

class Queue(ABC):
    def __init__(self, capacity: int) -> None:
        self._capacity: int = capacity
        self._lenght: int = 0
        self._data: list[Process] = []


    def get_data(self):
        return self._data

    def get_capacity(self):
        return self._capacity

    def get_length(self):
        return self._lenght

    def set_data(self, data: list[Process]):
        self._data = data

    def add_process(self, process: Process):
        if self._capacity == self._lenght:
            return False

        self._lenght += 1
        self._data.append(process)
        return True

class QueueNew(Queue):
    def build(self, data: dict):
        for p in data.values():
            self.add_process(Process(p))

        self._data = [p for p in self._data if p.get_size() <= 250]
        self._data.sort(reverse = False, key = lambda x: x.get_ta())


class QueueReady(Queue):
    def load_list(self, new_queue: QueueNew):
        loaded_items = []
        for item in new_queue.get_data():
            if self.add_process(item):
                loaded_items.append(item)
            else:
                break
        
        remnant = [item for item in new_queue.get_data() if item not in loaded_items]
        new_queue.set_data(remnant)


