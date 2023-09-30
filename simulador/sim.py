from process import Process
from tabulate import tabulate

def build_process_list(data: dict) -> list[Process]:
    process_list = []

    for p in data.values():
        item = Process(p)
        process_list.append(item)

    process_list = [p for p in process_list if p.get_size() <= 250]
    process_list.sort(reverse = False, key = lambda x: x.get_ta())

    return process_list

def print_table(data: list[Process], headers: list) -> None:
    outer = []
    for process in data:
        outer.append(process.return_list_of_data())
    print(tabulate(outer, headers, tablefmt="fancy_outline", stralign='center'))



