from copy import deepcopy
from rich import print
from rich.panel import Panel
from utils import (
    Proceso,
    Particion,
    Memoria,
    tabla_inicio,
    mostrar_estadisticas,
    mostrar_estado,
)


def asignar(proceso: Proceso, particion: Particion):
    proceso.estado = "Listo"

    # Actualizo las referencias tanto de la partición como del proceso   
    particion.proceso = proceso
    particion.frag_interna = particion.tamaño - proceso.tamaño
    proceso.particion = particion


def asignacion_a_memoria(
    cola_nuevos: list[Proceso],
    cola_listos: list[Proceso],
    cola_finalizados: list[Proceso],
    memoria_principal: Memoria,
    clock: int,
    quantum: int,
    FULL_RUN,
    ININTERRUMPIDO,
):
    lista_auxiliar_listos = []
    lista_auxiliar_suspendidos = []
    lista_auxiliar = []
    for p in cola_listos:
        if p.estado == "Suspendido" and p.tiempo_arribo <= clock:
            lista_auxiliar.append(p)
        continue

    for p in lista_auxiliar:
        for particion in memoria_principal.particiones:
            if particion.proceso is None:
                if p.tamaño <= particion.tamaño:
                    asignar(p, particion)
                    lista_auxiliar_suspendidos.append(p)
                    break

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
                    lista_auxiliar_listos.append(proceso)
                    break

        if proceso.particion is None:
            proceso.estado = "Suspendido"

        cola_listos.append(proceso)

    if not FULL_RUN:
        if len(lista_auxiliar_listos) > 0 or len(lista_auxiliar_suspendidos) > 0:
            input(
                "[!] Ingrese Enter para continuar al siguiente estado."
            ) if not ININTERRUMPIDO else None
            print("◎  Información:")
            print(f"  ◉  Tiempo de Clock: {clock}")
            print(f"  ◉  Quantum igual a: {quantum}")
            print(
                f"  ◉  {', '.join(str(p.pid) for p in lista_auxiliar_listos)} pasa de 'Nuevo' a 'Listo'"
            ) if len(lista_auxiliar_listos) > 0 else None
            print(
                f"  ◉  {', '.join(str(p.pid) for p in lista_auxiliar_suspendidos)} pasa de 'Suspendido' a 'Listo'"
            ) if len(lista_auxiliar_suspendidos) > 0 else None

            mostrar_estado(
                cola_nuevos, cola_listos, cola_finalizados, memoria_principal
            )

    lista_auxiliar_listos = []
    lista_auxiliar_suspendidos = []


def Run(cola_nuevos: list[Proceso], FULL_RUN, ININTERRUMPIDO):
    memoria_principal = Memoria(
        [Particion(100), Particion(60), Particion(120), Particion(250)]
    )
    clock = 0
    aux = 0
    quantum = 2
    cola_listos: list[Proceso] = []
    cola_finalizados: list[Proceso] = []
    CPU_LIBRE = True

    tabla_inicio(
        "[ϴ] Carga de trabajo que ingresa al simulador (Cola de Nuevos):",
        cola_nuevos,
        ["PID", "TAM(KB)", "TA", "TI", "ESTADO"],
    )

    while clock != cola_nuevos[0].tiempo_arribo:
        clock += 1

    while True:
        asignacion_a_memoria(
            cola_nuevos,
            cola_listos,
            cola_finalizados,
            memoria_principal,
            clock,
            quantum,
            FULL_RUN,
            ININTERRUMPIDO,
        )

        if CPU_LIBRE:
            quantum = 2

        '''
            Esto debido a que si tengo procesos con tiempos de arribo con una diferencia más grande que quantum,
            la cola de listos estará vacía por un periodo largo e Indexar lista vacía es un error.
        ''' 
        if len(cola_listos) == 0:
            clock += 1
            continue

        proceso = cola_listos[0]
        proceso.estado = "Ejecutando"

        if FULL_RUN:
            input(
                "[!] Ingrese Enter para continuar al siguiente tiempo de clock:\n"
            ) if not ININTERRUMPIDO else None
            print("◎  Información:")
            print(f"  ◉  Tiempo de Clock: {clock}")
            print(f"  ◉  Quantum igual a: {quantum}")
            mostrar_estado(
                cola_nuevos, cola_listos, cola_finalizados, memoria_principal
            )

        if not FULL_RUN:
            if proceso.pid != aux:
                input(
                    "[!] Ingrese Enter para continuar al siguiente estado."
                ) if not ININTERRUMPIDO else None
                print("◎  Información:")
                print(f"  ◉  Tiempo de Clock: {clock}")
                print(f"  ◉  Quantum igual a: {quantum}")
                print(f"  ◉  La CPU pasa a ejecutar: {proceso.pid}")
                mostrar_estado(
                    cola_nuevos, cola_listos, cola_finalizados, memoria_principal
                )

            aux = proceso.pid

        clock += 1
        proceso.tiempo_irrupcion -= 1

        for p in cola_listos[1:]:
            if p.estado == "Listo":
                p.tiempo_espera += 1

        CPU_LIBRE = False

        if proceso.tiempo_irrupcion == 0:
            proceso.estado = "Finalizado"
            proceso.instante_salida = clock

            # Actualizo las referencias tanto de la partición como del proceso   
            if (particion := proceso.particion) is not None:
                particion.proceso = None
                particion = None

            # Genero una copia porque estabamos teniendo conflictos con comportamientos indefinidos en ciertas partes.
            proceso = deepcopy(proceso)
            proceso.tiempo_irrupcion = proceso.resguardo_tiempo_irrupcion
            cola_finalizados.append(proceso)
            CPU_LIBRE = True
            # Retiro al proceso de la cola de listos.
            cola_listos.pop(0)

            if not FULL_RUN:
                input(
                    "[!] Ingrese Enter para continuar al siguiente estado."
                ) if not ININTERRUMPIDO else None
                print("◎  Información:")
                print(f"  ◉  Tiempo de Clock: {clock}")
                print(f"  ◉  Quantum igual a: {quantum}")
                print(f"  ◉  Finaliza el proceso: {proceso.pid}")
                mostrar_estado(
                    cola_nuevos, cola_listos, cola_finalizados, memoria_principal
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
            else:
                quantum = 2

        # Cambio de contexto
        if len(cola_listos) > 0:
            resg_pid = 0
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
                    resg_pid = p.pid

                proceso.estado = "Listo"

                # Actualizo las referencias tanto de la partición como del proceso   
                min_particion.proceso = proceso
                proceso.particion = min_particion

                min_particion.frag_interna = min_particion.tamaño - proceso.tamaño

                if not FULL_RUN:
                    input(
                        "[!] Ingrese Enter para continuar al siguiente estado."
                    ) if not ININTERRUMPIDO else None
                    print("◎  Información:")
                    print(f"  ◉  Tiempo de Clock: {clock}")
                    print(f"  ◉  Quantum igual a: {quantum}")
                    print(f"  ◉  Swap-In: {proceso.pid}") if resg_pid == 0 else print(f"  ◉  Swap-Out: {resg_pid} y Swap-In: {proceso.pid}")
                    mostrar_estado(
                        cola_nuevos, cola_listos, cola_finalizados, memoria_principal
                    )

        continue

    if FULL_RUN:
        input(
            "[!] Ingrese Enter para continuar al siguiente tiempo de clock:\n"
        ) if not ININTERRUMPIDO else None

        print("◎  Información:")
        print(f"  ◉  Tiempo de Clock: {clock}")
        print(f"  ◉  Quantum igual a: {quantum}")
        mostrar_estado(cola_nuevos, cola_listos, cola_finalizados, memoria_principal)

    print(
        Panel.fit(
            f"[bold green] COMPLETADO :heavy_check_mark: [reset] El simulador completó su tarea en [bold green]{clock}[reset] tiempos de clock. \n"
        )
    )
    mostrar_estadisticas(cola_finalizados)
