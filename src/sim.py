from tabulate import tabulate
from reader import read_data


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


# class ColaCircular:
#     def __init__(self, tamaño: int):
#         self.tamaño = tamaño
#         self.largo = 0
#         # Revisar si esto es la mejor idea, lo hice así porque no puedo indexar una lista vacía en python.
#         # Me parece que puede llegar a traer errores cuando querramos sacar datos del rendimiento del simulador.
#         self.buffer = [Proceso([0, 0, 0, 0]) for _ in range(tamaño)]
#         self.tail = self.head = 0

#     def shift(self, item) -> None:
#         if self.largo == self.tamaño:
#             print("La cola está llena")
#             return

#         self.buffer[self.tail] = item
#         self.tail = (self.tail + 1) % self.tamaño
#         self.largo += 1

#     def unshift(self) -> Proceso | None:
#         if self.largo == 0:
#             print("La cola está vacía")
#             return

#         item = self.buffer[self.head]
#         # self.buffer[self.head] = None
#         self.head = (self.head + 1) % self.tamaño
#         self.largo -= 1
#         return item

#     def peek(self):
#         return self.buffer[self.head]


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


def tabla(title: str, data: list[Proceso], headers: list) -> None:
    """
    Imprime por pantalla una tabla con los procesos dentro de una lista.
    """
    outer = []
    for proceso in data:
        outer.append(proceso.return_list_of_data())

    print(
        f"{title}\n"
        + tabulate(outer, headers, tablefmt="fancy_outline", stralign="center")
    )


def mostrar_estado(cola_nuevos: list[Proceso], cola_listos: list[Proceso], clock: int):
    print("[!] - En el tiempo de clock:", clock)
    tabla(
        "->> Carga de trabajo - Cola de Nuevos:",
        cola_nuevos,
        ["PID", "TAM(KB)", "TA", "TI", "ESTADO"],
    )
    tabla(
        "->> Carga de trabajo - Cola de Listos:",
        cola_listos,
        ["PID", "TAM(KB)", "TA", "TI", "ESTADO"],
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
    while (len(cola_nuevos) > 0) and (cola_nuevos[0].tiempo_arribo <= clock):
        # DEBUG
        # print("La cabeza de la cola de nuevos en el tiempo", clock, ":")
        # print(cola_nuevos.peek().return_list_of_data())
        # print("\n")
        # DEBUG

        if len(cola_listos) < 5:
            particiones = memoria_principal.particiones
            index = 0

            # Acá hay un error en la carga, seguramente tenga que ver con que iteramos sobre las particiones en el loop exterior, capaz podemos deshacernos de este loop y quedarnos con el while.
            for _ in memoria_principal.particiones:
                proceso = cola_nuevos.pop(0)
                # Utilizar un índice está causando una mal carga de los elementos, es evidente cuando se realiza una prueba de escritorio corta.
                # Por ejemplo, con índex = 0 entra un proceso de 150 y pregunta si particiones[0] está vacía, como si lo está, entra en particiones[2]
                # Luego con índex = 1 entra un proceso de 120 y pregunta si particiones[1] está vacía, como si lo está, entra en particiones[1]
                # Por último con índex = 2 entra un proceso de 20 y pregunta si particiones[2] está vacía, lo que sería falso, y se marca ese proceso como "Suspendido", a pesar de que podría haber entrado en particiones[0]
                # Podríamos usar el for _ in memoria_principal.particiones y usar una variable particion que usemos para realizar el control de los procesos
                if particiones[index].proceso is None:
                    tamaño = proceso.tamaño
                    if tamaño <= 60:
                        asignar(proceso, particiones[0])
                    elif tamaño <= 120:
                        asignar(proceso, particiones[1])
                    else:
                        asignar(proceso, particiones[2])
                else:
                    proceso.estado = "Suspendido"

                cola_listos.append(proceso)
                index += 1


def run(cola_nuevos: list[Proceso]):
    print("-------------- SIMULADOR -------------- (Fix me!)")
    memoria_principal = Memoria(
        [Particion(100), Particion(60), Particion(120), Particion(250)]
    )
    clock = 0
    quantum = 2
    cola_listos: list[Proceso] = []
    CPU_LIBRE = True
    tabla(
        "[ϴ] Carga de trabajo que ingresa al simulador (Cola de Nuevos):",
        cola_nuevos,
        ["PID", "TAM(KB)", "TA", "TI", "ESTADO"],
    )
    print("")


    while clock != cola_nuevos[0].tiempo_arribo:
        clock += 1

    while True:
        asignacion_a_memoria(cola_nuevos, cola_listos, memoria_principal, clock)
        # mostrar_estado(cola_nuevos, cola_listos)

        # Round-Robin:
        if CPU_LIBRE:
            quantum = 2

        mostrar_estado(cola_nuevos, cola_listos, clock)
        input("[!] Ingrese Enter para continuar al siguiente tiempo de clock:")
        clock += 1

        proceso = cola_listos.pop(0)

        proceso.estado = "Ejecutando"
        proceso.tiempo_irrupcion -= 1
        if proceso.tiempo_irrupcion == 0:
            proceso.estado = "Finalizado"
            # DEBUG
            # print("Finalizado:")
            # print(proceso.return_list_of_data())
            # DEBUG
            if proceso.particion is not None:
                proceso.particion.proceso = None
            CPU_LIBRE = True

            if len(cola_listos) == 0 and len(cola_nuevos) == 0:
                # Salida
                break
        else:
            quantum -= 1
            # mostrar_estado(cola_nuevos, cola_listos)
            # input("Ingrese enter para continuar al siguiente tiempo de clock")
            if quantum != 0:
                continue

            proceso.estado = "Listo"
            cola_listos.append(proceso)
            CPU_LIBRE = True

        if cola_listos[0].estado == "Listo":
            continue

        proceso = cola_listos.pop(0)
        min_frag = 999
        min_particion = memoria_principal.particiones[0]

        for particion in memoria_principal.particiones:
            frag_generada = particion.tamaño - proceso.tamaño
            if min_frag >= frag_generada and frag_generada >= 0:
                min_frag = frag_generada
                min_particion = particion

        if (p := min_particion.proceso) is not None:
            p.estado = "Suspendido"
            cola_listos.append(p)

        proceso.estado = "Listo"
        min_particion.proceso = proceso

        continue

    print("estado final")
    mostrar_estado(cola_nuevos, cola_listos, clock)
