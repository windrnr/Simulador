from tabulate import tabulate
from reader import read_data
from rich.console import Console
from rich.table import Table
from rich.columns import Columns
from rich import print


class Memoria:
    def __init__(self, mapa_de_memoria: list):
        self.particiones: list[Particion] = mapa_de_memoria[1:]


class Particion:
    def __init__(self, tamaño: int):
        self.tamaño: int = tamaño
        self.frag_interna: int = 0
        self.proceso: Proceso | None = None


class Proceso:
    def __init__(self, data: list[int]):
        self.pid: int = data[0]
        self.tamaño: int = data[1]
        self.tiempo_arribo: int = data[2]
        self.tiempo_irrupcion: int = data[3]
        self.estado = "Nuevo"
        self.particion: Particion | None = None

    def return_list_of_data(self) -> list:
        data = []
        data.append(self.pid)
        data.append(self.tamaño)
        data.append(self.tiempo_arribo)
        data.append(self.tiempo_irrupcion)
        data.append(self.estado)

        return data


def generar_desde_archivo(fuente, tamaño: int) -> list[Proceso]:
    """
    Se genera la cola a partir de un dictionary con los datos del archivo.
    """
    data = read_data(fuente)
    resultado = []

    for p in data.values():
        proceso = Proceso(p)
        if (
            proceso.tamaño <= 250
            and proceso.tiempo_arribo >= 0
            and proceso.tiempo_irrupcion >= 1
            and len(resultado) < tamaño
        ):
            resultado.append(proceso)
        continue

    resultado = [p for p in resultado if p.tiempo_irrupcion > 0]
    resultado.sort(key=lambda x: x.tiempo_arribo)
    return resultado


def tabla(title: str, data: list[Proceso], headers: list):
    """
    Imprime por pantalla una tabla con los procesos dentro de una lista.
    """
    tabla = Table(
            title = title,
            show_header=True,
            header_style="bold green",
            title_style="bold",
            )
    for columnas in headers:
        tabla.add_column(columnas)
    for p in data:
        tabla.add_row(
            str(p.pid),
            str(p.tamaño),
            str(p.tiempo_arribo),
            str(p.tiempo_irrupcion),
            p.estado,
        )
    Console().print(tabla,"\n")



def mostrar_estado(
    cola_nuevos: list[Proceso],
    cola_listos: list[Proceso],
    cola_finalizados: list[Proceso],
    clock: int,
):
    """
    Imprime por pantalla varias tablas con la información de los procesos de cada cola.
    """
    print(f"[!] - En el tiempo de clock: {clock}\n")
    nombres_columnas = ["PID", "TAM(KB)", "TA", "TI", "ESTADO"]

    header_style = "bold green"
    title_style = "bold"

    tabla_nuevos = Table(
        title="Cola de Nuevos",
        show_header=True,
        header_style=header_style,
        title_style=title_style,
    )
    for columnas in nombres_columnas:
        tabla_nuevos.add_column(columnas)
    for p in cola_nuevos:
        tabla_nuevos.add_row(
            str(p.pid),
            str(p.tamaño),
            str(p.tiempo_arribo),
            str(p.tiempo_irrupcion),
            p.estado,
        )

    tabla_listos = Table(
        title="Cola de Listos",
        show_header=True,
        header_style=header_style,
        title_style=title_style,
    )
    for columnas in nombres_columnas:
        tabla_listos.add_column(columnas)
    for p in cola_listos:
        tabla_listos.add_row(
            str(p.pid),
            str(p.tamaño),
            str(p.tiempo_arribo),
            str(p.tiempo_irrupcion),
            p.estado,
        )

    if len(cola_finalizados) != 0:
        tabla_finalizados = Table(
            title="Procesos Finalizados",
            show_header=True,
            header_style=header_style,
            title_style=title_style,
        )
        for columnas in nombres_columnas:
            tabla_finalizados.add_column(columnas)
        for p in cola_finalizados:
            tabla_finalizados.add_row(
                str(p.pid),
                str(p.tamaño),
                str(p.tiempo_arribo),
                str(p.tiempo_irrupcion),
                p.estado,
            )

        Console().print(Columns([tabla_nuevos, "\t", tabla_listos, "\t", tabla_finalizados]))
    else:
        Console().print(Columns([tabla_nuevos, "\t", tabla_listos]))


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


def run(cola_nuevos: list[Proceso]):
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

        mostrar_estado(cola_nuevos, cola_listos, cola_finalizados, clock)
        input("[!] Ingrese Enter para continuar al siguiente tiempo de clock:\n")
        print(f"[!] - Quantum igual a: {quantum}")

        proceso = cola_listos[0]
        proceso.estado = "Ejecutando"
        clock += 1
        proceso.tiempo_irrupcion -= 1
        CPU_LIBRE = False

        if proceso.tiempo_irrupcion == 0:
            proceso.estado = "Finalizado"

            if proceso.particion is not None:
                proceso.particion.proceso = None

            cola_finalizados.append(proceso)
            cola_listos.pop(0)
            CPU_LIBRE = True

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

        continue

    print("Termino!")
