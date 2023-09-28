import argparse
from pathlib import Path
import csv
from tabulate import tabulate


def read_csv(file_path: Path) -> list[str]:
    data = []
    if not Path.exists(file_path):
        raise ValueError(f"A ocurrido un error abriendo '{file_path}'.")

    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            data.append(row)

    return data


# Revisar esto, no funciona correctamente porque todavía no conozco cómo funcionan los dictionarys, más precisamente como añadir nuevas entradas a uno.
def read_csv_dictionary(file_path: Path) -> dict[str, int]:
    data = {}
    
    if not Path.exists(file_path):
        raise ValueError(f"A ocurrido un error abriendo '{file_path}'.")
    with open(file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.update(row)

    return data

def print_table(data:list[str]) -> None:
    headers = ["PDI", "TAM(KB)", "TA", "TI"]
    print(tabulate(data, headers, tablefmt="grid"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file_path", type=Path, help="Dirección del archivo con los procesos."
    )
    args = parser.parse_args()

    if not (args.file_path.suffix == ".csv"):
        parser.error("El archivo debe ser de extensión '.csv'.")

    try:
        data = read_csv(args.file_path)
        print_table(data)
    except ValueError as e:
        print(f"Error: {e}")
        parser.error("El archivo no existe o no es encontrado.")
if __name__ == "__main__":
    main()
