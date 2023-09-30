from pathlib import Path
import csv
import json

class Reader:
    def __init__(self):
        pass
    
    def read(self, file_path: Path) -> dict:
        if not Path.exists(file_path):
            raise FileNotFoundError(f"Ha ocurrido un error abriendo '{file_path}'.") 

        if Path.is_dir(file_path):
            raise IsADirectoryError(f"'{file_path}' es un directorio.")

        match file_path.suffix:
            case '.csv':
                data = self._csv_reader(file_path)
            case '.json':
                data = self._json_reader(file_path)
            case _:
                raise ValueError(f"El archivo de entrada debe ser '.csv' o '.json'.")

        return data
        

    def _json_reader(self, file_path: Path) -> dict:
        key = 1
        data = {}

        with open(file_path, "r") as json_file:
            json_data = json.load(json_file)
            if isinstance(json_data, list):
                for item in json_data:
                    l = list(item.values())
                    data[key] = l
                    key += 1

        return data


    def _csv_reader(self, file_path:Path) -> dict: 
        key = 1
        data = {}

        with open(file_path, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                row = [eval(i) for i in row]
                data[key] = row
                key += 1

        return data