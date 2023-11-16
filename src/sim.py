from copy import deepcopy
from rich import print
from utils import (
    Proceso,
    Particion,
    Memoria,
    tabla,
    mostrar_estadisticas,
    mostrar_estado,
)


def asignar(proceso: Proceso, particion: Particion):
    proceso.estado = "Listo"
    particion.proceso = proceso
    particion.frag_interna = particion.tamaño - proceso.tamaño
    proceso.particion = particion


def asignacion_a_memoria(
    cola_nuevos: list[Proceso],
    cola_listos: list[Proceso],
    memoria_principal: Memoria,
    clock: int,
):
    while (
        (len(cola_nuevos) > 0)
        and (cola_nuevos[0].tiempo_arribo <= clock)
        and (len(cola_listos) < 5)
    ):
        proceso = cola_nuevos.pop(0)
        for particion in memoria_principal.particiones:
            if particion.proceso is None:
                if proceso.tamaño <= particion.tamaño:
                    asignar(proceso, particion)
                    break

        if proceso.particion is None:
            proceso.estado = "Suspendido"

        cola_listos.append(proceso)


def Run(cola_nuevos: list[Proceso], FULL_RUN):
    memoria_principal = Memoria(
        [Particion(100), Particion(60), Particion(120), Particion(250)]
    )
    clock = 0
    quantum = 2
    cola_listos: list[Proceso] = []
    cola_finalizados: list[Proceso] = []

    CPU_LIBRE = True
    tabla(
        "[ϴ] Carga de trabajo que ingresa al simulador (Cola de Nuevos):",
        cola_nuevos,
        ["PID", "TAM(KB)", "TA", "TI", "ESTADO"],
    )

    while clock != cola_nuevos[0].tiempo_arribo:
        clock += 1

    while True:
        asignacion_a_memoria(cola_nuevos, cola_listos, memoria_principal, clock)

        if CPU_LIBRE:
            quantum = 2

        proceso = cola_listos[0]
        proceso.estado = "Ejecutando"

        if FULL_RUN:
            input("[!] Ingrese Enter para continuar al siguiente tiempo de clock:\n")
            print(f"[!] - Quantum igual a: {quantum}")

            mostrar_estado(
                cola_nuevos, cola_listos, cola_finalizados, memoria_principal, clock
            )

        clock += 1
        proceso.tiempo_irrupcion -= 1

        for p in cola_listos[1:]:
            if p.estado == "Listo":
                p.tiempo_espera += 1

        CPU_LIBRE = False

        if proceso.tiempo_irrupcion == 0:
            proceso.estado = "Finalizado"
            proceso.instante_salida = clock

            if proceso.particion is not None:
                proceso.particion.proceso = None
                proceso.particion = None
            
            # Genero una copia porque estabamos teniendo conflictos con comportamientos indefinidos en ciertas partes.
            proceso = deepcopy(proceso)
            cola_finalizados.append(proceso)
            CPU_LIBRE = True
            # Retiro al proceso de la cola de listos.
            cola_listos.pop(0)

            if not FULL_RUN:
                input("[!] Ingrese Enter para continuar al siguiente estado.")
                print(f"[!] - Quantum igual a: {quantum}")
                print(f"[!] - Finaliza el proceso: {proceso.pid}")
                mostrar_estado(
                    cola_nuevos, cola_listos, cola_finalizados, memoria_principal, clock
                )

                
            if len(cola_listos) == 0 and len(cola_nuevos) == 0:
                break
        else:
            quantum -= 1

            if quantum != 0:
                continue

            if len(cola_listos) != 1:
                proceso.estado = "Listo"
                cola_listos.append(cola_listos.pop(0))
                CPU_LIBRE = True

                

        # Cambio de contexto
        if cola_listos[0].estado == "Suspendido":
            proceso = cola_listos[0]
            min_frag = 999
            min_particion = memoria_principal.particiones[0]

            for particion in memoria_principal.particiones:
                frag_generada = particion.tamaño - proceso.tamaño
                if min_frag >= frag_generada and frag_generada >= 0:
                    min_frag = frag_generada
                    min_particion = particion

            if (p := min_particion.proceso) is not None:
                p.estado = "Suspendido"

            proceso.estado = "Listo"
            min_particion.proceso = proceso
            min_particion.frag_interna = min_particion.tamaño - proceso.tamaño
            
            if not FULL_RUN:
                input("[!] Ingrese Enter para continuar al siguiente estado.")
                print(f"[!] - Quantum igual a: {quantum}")
                print(f"[!] - {proceso.pid} pasa a \'Listo\'")
                mostrar_estado(
                    cola_nuevos, cola_listos, cola_finalizados, memoria_principal, clock
                )

        continue

    print(f"El simulador completó su tarea en {clock} tiempos de clock.")
    mostrar_estadisticas(cola_finalizados)
