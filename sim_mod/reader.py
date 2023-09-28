from pathlib import Path
import csv

class Reader:
    def __init__(self):
        pass
    
    def read(self, file_path: Path) -> list[list[str]]:
        suffix = file_path.suffix
        if not Path.exists(file_path):
            raise ValueError(f"A ocurrido un error abriendo '{file_path}'. El archivo no existe o no es encontrado")

        if not ((suffix == ".csv") or (suffix == ".json")):
            raise ValueError(f"El archivo de entrada debe ser de extensión '.csv' o '.json'.")
        
        data = [[]]
        if suffix == ".csv":
            data = self.csv_reader(file_path)
            pass
        
        if suffix == ".json":
            pass

        return data
        

    def csv_reader(self, file_path: Path) -> list[list[str]]:
        data = []
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:
                data.append(row)

        return data


    def csv_reader_dict(self, file_path:Path) -> dict: 
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



