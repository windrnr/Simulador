import inquirer
from inquirer import errors
import argparse
from pathlib import Path, PurePath
from sim import ColaCircular, Proceso, run, generar_desde_archivo
import os


def build(file_path):
    cola_nuevos = generar_desde_archivo(file_path, 10)
    run(cola_nuevos)


def clear_screen():
    clear = lambda: os.system("tput reset")
    clear()


def validar(answers, current):
    try:
        if int(current) >= 0:
            return True
    except:
        raise errors.ValidationError(
            "", reason="El valor ingresado no es un número positivo"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file_path",
        type=Path,
        nargs="?",
        default=None,
        help="Dirección del archivo con los procesos (opcional).",
    )
    args = parser.parse_args()

    preguntas = [
        inquirer.List(
            name="opción",
            message="Cómo va a cargar los procesos?",
            choices=["Terminal", "Archivo"],
        ),
    ]

    try:
        if args.file_path is not None:
            build(args.file_path)
        else:
            respuestas = inquirer.prompt(preguntas)
            if respuestas is not None:
                entrada = respuestas["opción"]
                if entrada is not None:
                    if entrada == "Archivo":
                        respuesta = inquirer.prompt(
                            [
                                inquirer.Path(
                                    "path",
                                    message="Ingrese el path hacia el archivo",
                                    path_type=inquirer.Path.FILE,
                                ),
                            ]
                        )
                        if respuesta is not None:
                            file_path = Path(PurePath(respuesta["path"]))
                            build(file_path)
                    else:
                        preguntas = [
                            inquirer.Text(
                                name="pid",
                                message="ID",
                                validate=validar,
                            ),
                            inquirer.Text(
                                name="tiempo_arribo",
                                message="Tiempo de arribo",
                                validate=validar,
                            ),
                            inquirer.Text(
                                name="tiempo_irrupcion",
                                message="Tiempo de irrupción",
                                validate=validar,
                            ),
                            inquirer.Text(
                                name="tamaño",
                                message="Tamaño",
                                validate=validar,
                            ),
                        ]
                        respuesta = inquirer.prompt(
                            [
                                inquirer.Text(
                                    name="numero_procesos",
                                    message="Ingrese el número de procesos que desea cargar",
                                    validate=validar,
                                )
                            ]
                        )
                        if respuesta is not None:
                            numero = int(respuesta["numero_procesos"])
                            cola_nuevos = ColaCircular(10)
                            for i in range(1, numero):
                                print("Progreso:", i, "/10")
                                respuestas = inquirer.prompt(preguntas)
                                if respuestas is not None:
                                    data = []
                                    data.append(int(respuestas["pid"]))
                                    data.append(int(respuestas["tamaño"]))
                                    data.append(int(respuestas["tiempo_arribo"]))
                                    data.append(int(respuestas["tiempo_irrupcion"]))
                                    print(type(respuestas["pid"]))
                                    cola_nuevos.shift(Proceso(data))

                            clear_screen()
                            run(cola_nuevos)

    except ValueError as e:
        print(f"Error: Extensión incorrecta. {e}")
    except FileNotFoundError as e:
        print(f"Error: {e} El archivo no existe o no es encontrado.")
    except IsADirectoryError as e:
        print(f"Error: El path: {e}")


if __name__ == "__main__":
    main()
