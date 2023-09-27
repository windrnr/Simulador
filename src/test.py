import argparse
from pathlib import Path
import csv
from tabulate import tabulate

def readCSV(file_path):
    data = []
    if not Path.exists(file_path):
        raise ValueError(f"A ocurrido un error abriendo '{file_path}'.")

    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            data.append(row)

    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=Path, help="La dirección al archivo .csv.")
    args = parser.parse_args()
    
    headers = ["PDI", "TAM(KB)", "TA", "TI"]
    try:
        data = readCSV(args.file_path)
    except ValueError as e:
        print(f"Error: {e}")
        parser.error("El archivo no existe o no es encontrado.")


    print(tabulate(data, headers, tablefmt="grid"))


if __name__ == "__main__":
    main()



