import argparse
from pathlib import Path
from sim import (
    Proceso,
    generar_desde_archivo,
    ColaCircular,
    print_table,
    Particion,
    Memoria,
)


def asignacion_a_memoria(cola_nuevos, cola_listos, memoria_principal, clock):
    while cola_nuevos.peek().tiempo_arribo <= clock:
        if cola_listos.largo < 5:
            particiones = memoria_principal.particiones
            i = 1
            for _ in memoria_principal.particiones:
                proceso = cola_nuevos.unshift()
                if proceso:
                    if not particiones[i].proceso:
                        match proceso.tamaño:
                            case n if n <= 60:
                                proceso.estado = "Listo"
                                particiones[1].proceso = proceso
                                particiones[1].frag_interna = (
                                    particiones[1].tamaño - proceso.tamaño
                                )
                                proceso.particion = particiones[1]
                            case n if n <= 120:
                                proceso.estado = "Listo"
                                particiones[2].proceso = proceso
                                particiones[2].frag_interna = (
                                    particiones[2].tamaño - proceso.tamaño
                                )
                                proceso.particion = particiones[2]
                            case n if n <= 250:
                                proceso.estado = "Listo"
                                particiones[3].proceso = proceso
                                particiones[3].frag_interna = (
                                    particiones[3].tamaño - proceso.tamaño
                                )
                                proceso.particion = particiones[3]
                    else:
                        proceso.estado = "Suspendido"
                        cola_listos.shift(proceso)
                        i += 1


def simulador(cola_nuevos):
    print_table(
        "->> Carga de trabajo:",
        cola_nuevos.buffer,
        ["PID", "TAM(KB)", "TA", "TI"],
    )
    memoria_principal = Memoria(
        [Particion(100), Particion(60), Particion(120), Particion(250)]
    )
    clock = 0
    quantum = 2
    cola_listos = ColaCircular(5)
    CPU_LIBRE = True

    while clock != cola_nuevos.peek().tiempo_arribo:
        clock += 1

    while True:
        asignacion_a_memoria(cola_nuevos, cola_listos, memoria_principal, clock)

        # Round-Robin:
        if CPU_LIBRE:
            quantum = 2

        clock += 1
        proceso = cola_listos.unshift()
        if proceso:
            proceso.estado = "Ejecutando"
            proceso.tiempo_irrupcion -= 1
            if proceso.tiempo_irrupcion == 0:
                proceso.estado = "Finalizado"
                if proceso.particion:
                    proceso.particion.proceso = None
                # Me interesaría cambiarle el estado al proceso cuando se termina?
                # Si no, dejo que el GC elimine la variable.
                CPU_LIBRE = True

                if cola_listos.largo == 0 and cola_nuevos.largo == 0:
                    break
            else:
                quantum -= 1
                if not quantum == 0:
                    continue

                proceso.estado = "Listo"
                cola_listos.shift(proceso)
                CPU_LIBRE = True

        if cola_listos.peek().estado == "Listo":
            continue

        proceso = cola_listos.unshift()
        min_frag = 9000
        min_particion = memoria_principal.particiones[1]
        if proceso:
            for particion in memoria_principal.particiones:
                frag_generada = particion.tamaño - proceso.tamaño
                if min_frag >= frag_generada and frag_generada >= 0:
                    min_frag = frag_generada
                    min_particion = particion

        p = min_particion.proceso
        if p:
            p.estado = "Suspendido"
            cola_listos.shift(p)

        if proceso:
            proceso.estado = "Listo"
            min_particion.proceso = proceso

        continue


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file_path", type=Path, help="Dirección del archivo con los procesos."
    )
    args = parser.parse_args()

    try:
        cola_nuevos = ColaCircular(10)
        generar_desde_archivo(cola_nuevos, args.file_path)
        simulador(cola_nuevos)

    except ValueError as e:
        print(f"Error: Extensión incorrecta. {e}")
    except FileNotFoundError as e:
        print(f"Error: {e} El archivo no existe o no es encontrado.")
    except IsADirectoryError as e:
        print(f"Error: El path: {e}")


if __name__ == "__main__":
    main()
