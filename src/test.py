import argparse
from pathlib import Path
import csv
from tabulate import tabulate

def readCSV(file_path: Path) -> list[str]:
    data = []
    if not Path.exists(file_path):
        raise ValueError(f"A ocurrido un error abriendo '{file_path}'.")

    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            data.append(row)

    return data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=Path, help="Dirección del archivo con los procesos.")
    args = parser.parse_args()

    if not (args.file_path.suffix == '.csv'):
        parser.error("El archivo debe ser de extensión '.csv'.")
    
    headers = ["PDI", "TAM(KB)", "TA", "TI"]
    try:
        data = readCSV(args.file_path)
    except ValueError as e:
        print(f"Error: {e}")
        parser.error("El archivo no existe o no es encontrado.")


    print(tabulate(data, headers, tablefmt="grid"))


if __name__ == "__main__":
    main()



