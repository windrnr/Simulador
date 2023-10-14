import argparse
from reader import read_data
from sim import print_table, QueueNew, QueueReady
from pathlib import Path

# Responsabilidades de main:
# 1) Encargarse solamente de manejar los errores que vayan subiendo del resto de la ejecución del programa.
# 2) Llamar a los procesos principales del simulador (Que se encuentran en sim.py)

#TODO:
# 1. Abstraer toda la implementación del simulador fuera de main.py
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "file_path", type=Path, help="Dirección del archivo con los procesos."
            )
    args = parser.parse_args()

    try:
        data = read_data(args.file_path)

        new_queue = QueueNew(10)
        new_queue.build(data)
        print_table("Tabla de cola de nuevos recien cargada:", new_queue.get_data(), ["PID", "TAM(KB)", "TA", "TI"])

        ready_queue = QueueReady(5)
        ready_queue.load_list(new_queue)

        print_table("Tabla de cola de nuevos después de cargar la cola de listos:", new_queue.get_data(), ["PID", "TAM(KB)", "TA", "TI"])
        print_table("Tabla de cola de listos:", ready_queue.get_data(), ["PID", "TAM(KB)", "TA", "TI"])

    except ValueError as e:
        print(f"Error: Extensión incorrecta. {e}")
    except FileNotFoundError as e:
        print(f"Error: {e} El archivo no existe o no es encontrado.")
    except IsADirectoryError as e:
        print(f"Error: El path: {e}")

if __name__ == "__main__":
    main()
