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

def print_table(data: list, headers: list) -> None:
    outer = []
    for process in data:
        outer.append(process.return_list_of_data())
    print(tabulate(outer, headers, tablefmt="grid"))

# La idea es que main se encarge de manejar los errores que van ocurriendo, y llamar a los procesos principales del simulador
# No tendría que haber una implementación en esta función.
def main() -> None:
    args = parse_args()

    try:
        r = reader.Reader()
        data = r.read(args.file_path)
        process_list = build_process_list(data)
        print_table(process_list, ["PDI", "TAM(KB)", "TA", "TI"])
    except ValueError as e:
        print(f"Error: Extensión incorrecta. {e}")
    except FileNotFoundError as e:
        print(f"Error: {e} El archivo no existe o no es encontrado.")
    except IsADirectoryError as e:
        print(f"Error: El path: {e}")

if __name__ == "__main__":
    main()
