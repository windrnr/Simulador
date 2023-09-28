import argparse
from tabulate import tabulate
from pathlib import Path
import reader
from process import Process

# A estas funciones probablemente las moveremos a un módulo que se encarge de la ejecución del simulador. Por el momento está acá.
def build_process_list(data: dict) -> list[Process]:
    process_list = []
    for p in data.values():
        item = Process(p)
        process_list.append(item)
    
    return process_list

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "file_path", type=Path, help="Dirección del archivo con los procesos."
            )
    args = parser.parse_args()

    return args

def print_table(process_list: list[Process]) -> None:
    outer = []
    for process in process_list:
        outer.append(process.return_list_of_data())
    headers = ["PDI", "TAM(KB)", "TA", "TI"]
    print(tabulate(outer, headers, tablefmt="grid"))

# La idea es que main se encarge de manejar los errores que van ocurriendo, y llamar a los procesos principales del simulador
# No tendría que haber una implementación en esta función.
def main() -> None:
    args = parse_args()

    try:
        r = reader.Reader()
        data = r.read(args.file_path)
        process_list = build_process_list(data)
        print_table(process_list)

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
