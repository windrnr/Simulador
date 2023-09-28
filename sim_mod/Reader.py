from pathlib import Path
import csv

def csv_reader(file_path: Path) -> list[list[str]]:
    data = []

    if not Path.exists(file_path):
        raise ValueError(f"A ocurrido un error abriendo '{file_path}'.")

    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            data.append(row)

    return data


def csv_reader_dict(file_path:Path) -> dict: 
    key = 1
    map = {}

    if not Path.exists(file_path):
        raise ValueError(f"A ocurrido un error abriendo '{file_path}'.")

    with open(file_path, newline='') as process_file:
        reader = csv.reader(process_file, delimiter=',')
        for row in reader:
            map[key] = row
            key += 1
    
    return map 
