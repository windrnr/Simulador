from pathlib import Path
import json
import csv


def read_data(file_path: Path) -> dict:
    """
    Devuelve un dictionary con el contenido del archivo.
    """
    if file_path.suffix == ".csv":
        data = csv_reader(file_path)
    else:
        data = json_reader(file_path)

    return data


def json_reader(file_path: Path) -> dict:
    key = 1
    data = {}

    with open(file_path, "r") as json_file:
        json_data = json.load(json_file)
        if isinstance(json_data, list):
            for item in json_data:
                row = list(item.values())
                data[key] = row
                key += 1

    return data


def csv_reader(file_path: Path) -> dict:
    key = 1
    data = {}

    with open(file_path, newline="") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            row = [eval(i) for i in row]
            data[key] = row
            key += 1

    return data
