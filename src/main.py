import argparse
from sim import print_table, cargar_desde_cola, cargar_desde_archivo, ColaCircular
from pathlib import Path


class Memoria:
    def __init__(self, layout: list):
        self.particion_pequeña: Particion = layout[1]
        self.particion_mediana: Particion = layout[2]
        self.particion_grande: Particion = layout[3]


class Particion:
    def __init__(self, size: int):
        self.tamaño = size
        self.frag_interna = 0
        self.usada = False


def asign(p: Particion, size: int):
    q, r = divmod(p.tamaño, size)
    p.tamaño -= q * size
    p.frag_interna = r
    p.usada = True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file_path", type=Path, help="Dirección del archivo con los procesos."
    )
    args = parser.parse_args()

    try:
        clock = 0
        cola_nuevos = ColaCircular(10)
        cargar_desde_archivo(cola_nuevos, args.file_path)
        print_table(
            "->> Carga de trabajo:",
            cola_nuevos.buffer,
            ["PID", "TAM(KB)", "TA", "TI"],
        )
        cola_listos = ColaCircular(5)
        # Esta funcion seguramente va a convenir que la volvamos a definir para que cargue solamente un proceso a la vez en vez de 5 cada vez.
        # No lo hice ahora porque quiero ver si hace falta.
        cargar_desde_cola(cola_listos, cola_nuevos)
        print_table(
            "->> Tabla de cola de nuevos después de cargar la cola de listos:",
            cola_nuevos.buffer,
            ["PID", "TAM(KB)", "TA", "TI"],
        )
        print_table(
            "->> Tabla de cola de listos:",
            cola_listos.buffer,
            ["PID", "TAM(KB)", "TA", "TI"],
        )
        memoria = Memoria(
            [Particion(100), Particion(60), Particion(120), Particion(250)]
        )

        # Prestar atención que la condición está incompleta por el momento, tendría que controlar la longitud de la cola de listos también.
        # while (cola_nuevos.largo !=0):
        #    while(clock != cola_nuevos.data[0].get_tiempo_arribo()):
        #        clock += 1

        #    cola_listos.cargar_desde_lista(cola_nuevos)
        #    # print_table("->> Tabla de cola de nuevos después de cargar la cola de listos:", new_queue._data, ["PID", "TAM(KB)", "TA", "TI"])
        #    # print_table("->> Tabla de cola de listos:", ready_queue._data, ["PID", "TAM(KB)", "TA", "TI"])

        #    # Revisar en el diagrama de flujo la condición "Todos los proceso de CL están en MP o Disco"
        #    # Nunca van a estar los 5 procesos de la cola en la memoria principal, como máximo 3.
        #    # Tal vez se refiera a otra cosa pero no queda claro.

        #    # BestFit:
        #    for process in cola_listos.data:
        #        size = process.get_tamaño()
        #        if size <= memoria.particion_pequeña.tamaño:
        #            if memoria.particion_pequeña.usada == False:
        #                asign(memoria.particion_pequeña, size)
        #                process._executing = True
        #        elif size <= memoria.particion_mediana.tamaño:
        #            if memoria.particion_mediana.usada == False:
        #                asign(memoria.particion_mediana, size)
        #                process._executing = True
        #        else:
        #            if memoria.particion_grande.usada == False:
        #                asign(memoria.particion_grande, size)
        #                process._executing = True

        #    #Round-Robin:
        #    while (cola_listos.largo != 0):
        #        break

        #    break

    except ValueError as e:
        print(f"Error: Extensión incorrecta. {e}")
    except FileNotFoundError as e:
        print(f"Error: {e} El archivo no existe o no es encontrado.")
    except IsADirectoryError as e:
        print(f"Error: El path: {e}")


if __name__ == "__main__":
    main()
