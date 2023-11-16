from reader import read_data
from rich.console import Console
from rich.table import Table
from rich.columns import Columns


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
        # Tiempo total en que el proceso está en estado Listo
        self.tiempo_espera: int = 0
        self.instante_salida: int = 0
        self.resguardo_tiempo_irrupcion = data[3]
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
        title=title,
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
    Console().print(tabla, "\n")


def mostrar_estadisticas(
    cola_finalizados: list[Proceso],
):
    estadistica_columnas = [
        "PID",
        "T.RESPUESTA",
        "T.ESPERA",
        "T.RETORNO",

    ]

    promedios_columnas = [ 
        "T.RESPUESTA(x̄)",
        "T.ESPERA(x̄)",
        "T.RETORNO(x̄)",
    ]
    

    tabla_estadistica = Table(
        title="Tiempos de cada proceso",
        show_header=True,
        header_style="bold green",
        title_style="bold",
    )
    

    for columna in estadistica_columnas:
        tabla_estadistica.add_column(columna, justify="center")
    for p in cola_finalizados:
        t_respuesta = p.instante_salida - p.tiempo_arribo
        t_retorno = p.resguardo_tiempo_irrupcion + p.tiempo_espera
        t_espera = p.tiempo_espera

        tabla_estadistica.add_row(
            str(p.pid),
            str(t_respuesta),
            str(t_espera),
            str(t_retorno),
        )

    tabla_promedios = Table(
        title="Tiempos promedios",
        show_header=True,
        header_style="bold yellow",
        title_style="bold",
    )

    sum_t_respuesta = 0
    sum_t_retorno   = 0
    sum_t_espera    = 0
    
    for columna in promedios_columnas:
        tabla_promedios.add_column(columna, justify="center")
    for p in cola_finalizados:
        sum_t_respuesta += (p.instante_salida - p.tiempo_arribo)
        # Que vivo que soy si a este punto de la ejecución el tiempo de irrupción de ese proceso es 0.
        sum_t_retorno   += (p.resguardo_tiempo_irrupcion + p.tiempo_espera)
        sum_t_espera    += (p.tiempo_espera)


    tabla_promedios.add_row(
        str(round((sum_t_respuesta  / len(cola_finalizados)), 2)),
        str(round((sum_t_espera     / len(cola_finalizados)), 2)),
        str(round((sum_t_retorno    / len(cola_finalizados)), 2)),
    )

    Console().print(
        Columns(
            [
                tabla_estadistica,
                "\t",
                tabla_promedios
            ]
        )
    )


def mostrar_estado(
    cola_nuevos: list[Proceso],
    cola_listos: list[Proceso],
    cola_finalizados: list[Proceso],
    memoria: Memoria,
    clock: int,
):
    """
    Imprime por pantalla varias tablas con la información de los procesos de cada cola.
    """
    print(f"[!] - En el tiempo de clock: {clock}\n")
    nombres_columnas = ["PID", "TAM(KB)", "TA", "TI", "ESTADO"]
    memoria_columnas = ["DIRECCIÓN", "TAM(KB)", "FRAG(KB)", "PID", "TAM(KB)"]

    title_style = "bold"

    tabla_memoria = Table(
        title="Memoria",
        show_header=True,
        header_style="bold blue",
        title_style=title_style,
    )

    for columna in memoria_columnas:
        tabla_memoria.add_column(columna, justify="center")
    for particion in memoria.particiones:
        if particion and particion.proceso is not None:
            tabla_memoria.add_row(
                str(hex(id(particion))),
                str(particion.tamaño),
                str(particion.frag_interna),
                str(particion.proceso.pid),
                str(particion.proceso.tamaño),
            )

    tabla_nuevos = Table(
        title="Cola de Nuevos",
        show_header=True,
        header_style="bold yellow",
        title_style=title_style,
    )
    for columna in nombres_columnas:
        tabla_nuevos.add_column(columna, justify="center")
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
        header_style="bold cyan",
        title_style=title_style,
    )
    for columna in nombres_columnas:
        tabla_listos.add_column(columna, justify="center")
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
            header_style="bold green",
            title_style=title_style,
        )
        for columna in nombres_columnas:
            tabla_finalizados.add_column(columna, justify="center")
        for p in cola_finalizados:
            tabla_finalizados.add_row(
                str(p.pid),
                str(p.tamaño),
                str(p.tiempo_arribo),
                str(p.tiempo_irrupcion),
                p.estado,
            )

        Console().print (
            Columns([tabla_memoria, "\t", tabla_nuevos, "\t", tabla_listos, "\t", tabla_finalizados])
        )
    else:
        Console().print(
            Columns([tabla_memoria, "\t", tabla_nuevos, "\t", tabla_listos])
        )
