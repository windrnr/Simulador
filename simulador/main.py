import argparse
from sim import Queue, print_table
from pathlib import Path

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file_path", type=Path, help="Dirección del archivo con los procesos."
    )
    args = parser.parse_args()

    try:
        new_queue = Queue(10)
        new_queue.load_from_file(args.file_path)
        print_table(
            "->> Tabla de cola de nuevos recien cargada:",
            new_queue._data,
            ["PID", "TAM(KB)", "TA", "TI"],
        )

        ready_queue = Queue(5)
        ready_queue.load_from_queue(new_queue)

        # print_table("->> Tabla de cola de nuevos después de cargar la cola de listos:", new_queue._data, ["PID", "TAM(KB)", "TA", "TI"])
        # print_table("->> Tabla de cola de listos:", ready_queue._data, ["PID", "TAM(KB)", "TA", "TI"])

    except ValueError as e:
        print(f"Error: Extensión incorrecta. {e}")
    except FileNotFoundError as e:
        print(f"Error: {e} El archivo no existe o no es encontrado.")
    except IsADirectoryError as e:
        print(f"Error: El path: {e}")


if __name__ == "__main__":
    main()
