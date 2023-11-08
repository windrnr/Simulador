import inquirer
from inquirer import errors
import argparse
from pathlib import Path, PurePath
from sim import Proceso, run, generar_desde_archivo
import os


def build(file_path):
    cola_nuevos = generar_desde_archivo(file_path, 10)
    run(cola_nuevos)


def clear_screen():
    clear = lambda: os.system("tput reset")
    clear()


def validar_proceso(answers, current):
    try:
        if int(current) >= 0:
            return True
    except:
        raise errors.ValidationError(
            "", reason="El valor ingresado no es un número positivo."
        )


def validar_carga(answers, current):
    try:
        if int(current) >= 5 and int(current) <= 10:
            return True
    except:
        raise errors.ValidationError(
            "", reason="El valor ingresado debe estar en el intervalo [5;10] ."
        )


def validar_path(answers, current):
    file_path = Path(PurePath(current))

    if not Path.exists(file_path):
        raise errors.ValidationError(
            "", reason=f"Ha ocurrido un error abriendo '{file_path}', no existe o no ha podido ser encontrado."
        )

    if Path.is_dir(file_path):
        raise errors.ValidationError("", reason=f"'{file_path}' es un directorio.")

    if file_path.suffix != ".csv" and file_path.suffix != ".json":
        raise errors.ValidationError(
            "", reason="El archivo de entrada debe ser '.csv' o '.json'."
        )

    return True


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
                                    validate=validar_path,
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
                                validate=validar_proceso,
                            ),
                            inquirer.Text(
                                name="tiempo_arribo",
                                message="Tiempo de arribo",
                                validate=validar_proceso,
                            ),
                            inquirer.Text(
                                name="tiempo_irrupcion",
                                message="Tiempo de irrupción",
                                validate=validar_proceso,
                            ),
                            inquirer.Text(
                                name="tamaño",
                                message="Tamaño",
                                validate=validar_proceso,
                            ),
                        ]
                        respuesta = inquirer.prompt(
                            [
                                inquirer.Text(
                                    name="numero_procesos",
                                    message="Ingrese el número de procesos que desea cargar (min.5, max.10)",
                                    validate=validar_carga,
                                )
                            ]
                        )
                        if respuesta is not None:
                            numero = int(respuesta["numero_procesos"])
                            cola_nuevos = []
                            for i in range(1, numero + 1):
                                print("Progreso:", i, "/", numero)
                                respuestas = inquirer.prompt(preguntas)
                                if respuestas is not None:
                                    data = []
                                    data.append(int(respuestas["pid"]))
                                    data.append(int(respuestas["tamaño"]))
                                    data.append(int(respuestas["tiempo_arribo"]))
                                    data.append(int(respuestas["tiempo_irrupcion"]))
                                    cola_nuevos.append(Proceso(data))

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
