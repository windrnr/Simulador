import argparse
import reader
from sim import build_process_list, print_table
from pathlib import Path

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "file_path", type=Path, help="Dirección del archivo con los procesos."
            )
    args = parser.parse_args()

    return args

# Responsabilidades de main:
# 1) Encargarse solamente de manejar los errores que vayan subiendo del resto de la ejecución del programa.
# 2) Llamar a los procesos principales del simulador (Que se encuentran en sim.py)

#TODO:
# 1. Abstraer la lectura y construcción de la cola de nuevos en una función.
def main() -> None:
    args = parse_args()

    try:
        r = reader.Reader()
        data = r.read(args.file_path)
        
        new_process_list = build_process_list(data)
        print_table(new_process_list, ["PID", "TAM(KB)", "TA", "TI"])

    except ValueError as e:
        print(f"Error: Extensión incorrecta. {e}")
    except FileNotFoundError as e:
        print(f"Error: {e} El archivo no existe o no es encontrado.")
    except IsADirectoryError as e:
        print(f"Error: El path: {e}")

if __name__ == "__main__":
    main()
