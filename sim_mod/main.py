import argparse
from tabulate import tabulate
from pathlib import Path
import reader
from process import Process

# Esto probablemente lo moveremos a un módulo que se encarge de la ejecución del simulador. Por el momento está acá
def build_process_list(data: list[list[str]]) -> list[Process]:
    process_list = []
    for p in data:
        item = Process(p)
        process_list.append(item)
    
    return process_list


# Esto también tendría que moverse a otro módulo.
def print_table(data:list[list[str]]) -> None:
    headers = ["PDI", "TAM(KB)", "TA", "TI"]
    print(tabulate(data, headers, tablefmt="grid"))

## TODO:
## tabulate trata a los elementos de un dictionary como columnas en vez de filas, así que hay que buscar otra manera. No es importante ahora mismo
def print_table_dict(data:dict[str, str]) -> None:
    print(tabulate(data, headers="firstrow", tablefmt="grid"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "file_path", type=Path, help="Dirección del archivo con los procesos."
            )
    args = parser.parse_args()

    return args


# La idea es que main se encarge de manejar los errores que van ocurriendo, y llamar a los procesos principales del simulador, no tendría que haber una implementación en esta función .
# Hay varias cosas que no deberían estár, pero por el momento las dejo acá porque no tenemos tanto desarrollado.
def main() -> None:
    args = parse_args()

    try:
        r = reader.Reader()
        data = r.read(args.file_path)
        print("La información en la tabla:")
        print_table(data)
        process_list = build_process_list(data)
        # Esto siguiente, repito, es una demostración de que los valores efectivamente se cargaron en la clase. No tiene otro uso.
        print("La información en la clase:\n =======================")
        for process in process_list:
            process.print_own_data()
            print("=======================")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
