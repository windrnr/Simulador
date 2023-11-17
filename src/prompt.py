import inquirer, os
from inquirer import errors
from pathlib import Path, PurePath
from sim import Run
from utils import Proceso, generar_desde_archivo


def clear_screen():
    os.system("tput reset")


def validar_positivo(answers, current):
    try:
        if int(current) >= 0:
            return True
    except:
        raise errors.ValidationError(
            "", reason="El valor ingresado no es un número positivo."
        )


def validar_tamaño(answers, current):
    try:
        if int(current) >= 0 and int(current) <= 250:
            return True
    except:
        raise errors.ValidationError(
            "", reason="El tamaño de un proceso no puede ser mayor a 250KB."
        )


def validar_carga(answers, current):
    try:
        if int(current) <= 10:
            return True
    except:
        raise errors.ValidationError(
            "", reason="La cantidad de proceso no debe ser mayor a 10."
        )


def validar_path(answers, current):
    file_path = Path(PurePath(current))

    if not Path.exists(file_path):
        raise errors.ValidationError(
            "",
            reason=f"Ha ocurrido un error abriendo '{file_path}', no existe o no ha podido ser encontrado.",
        )

    if Path.is_dir(file_path):
        raise errors.ValidationError("", reason=f"'{file_path}' es un directorio.")

    if file_path.suffix != ".csv" and file_path.suffix != ".json":
        raise errors.ValidationError(
            "", reason="El archivo de entrada debe ser '.csv' o '.json'."
        )

    return True


def Prompt(FULL_RUN, ININTERRUMPIDO):
    preguntas = [
        inquirer.List(
            name="opción",
            message="Cómo va a cargar los procesos?",
            choices=["Terminal", "Archivo"],
        ),
    ]
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
                    cola_nuevos = generar_desde_archivo(file_path, 10)
                    Run(cola_nuevos, FULL_RUN, ININTERRUMPIDO)
            else:
                preguntas = [
                    inquirer.Text(
                        name="pid",
                        message="ID",
                        validate=validar_positivo,
                    ),
                    inquirer.Text(
                        name="tiempo_arribo",
                        message="Tiempo de arribo",
                        validate=validar_positivo,
                    ),
                    inquirer.Text(
                        name="tiempo_irrupcion",
                        message="Tiempo de irrupción",
                        validate=validar_positivo,
                    ),
                    inquirer.Text(
                        name="tamaño",
                        message="Tamaño",
                        validate=validar_tamaño,
                    ),
                ]
                respuesta = inquirer.prompt(
                    [
                        inquirer.Text(
                            name="numero_procesos",
                            message="Ingrese el número de procesos que desea cargar (max.10)",
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
                    Run(cola_nuevos, FULL_RUN, ININTERRUMPIDO)
