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


def tabla(title: str, data: list[Proceso], headers: list):
    # """
    # Imprime por pantalla una tabla con los procesos dentro de una lista.
    # """
    # outer = []
    # for proceso in data:
    #     outer.append(proceso.return_list_of_data())

    # return tabulate(outer, headers, tablefmt="fancy_outline", stralign="center")
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


def mostrar_estado(cola_nuevos: list[Proceso], cola_listos: list[Proceso], cola_finalizados: list[Proceso], clock: int):
    # print("[!] - En el tiempo de clock:", clock)

    # tabla_nuevos = tabla(
    #     cola_nuevos,
    #     ["PID", "TAM(KB)", "TA", "TI", "ESTADO"],
    # )
    # tabla_listos = tabla(
    #     cola_listos,
    #     ["PID", "TAM(KB)", "TA", "TI", "ESTADO"],
    # )

    # max_filas = max(len(tabla_nuevos), len(tabla_listos))

    # tabla_nuevos += [["", ""]] * (max_filas- len(tabla_nuevos))
    # tabla_listos += [["", ""]] * (max_filas- len(tabla_listos))
    
    # tabla_nuevos_lineas = tabla_nuevos.split('\n')
    # tabla_listos_linea = tabla_listos.split('\n')

    # for linea1, linea2 in zip(tabla_nuevos_lineas, tabla_listos_linea):
    #     print(f"{linea1}\t{linea2}")
    print("[!] - En el tiempo de clock:", clock)
    tabla(
        "->> Carga de trabajo - Cola de Nuevos:",
        cola_nuevos,
        ["PID", "TAM(KB)", "TA", "TI", "ESTADO"],
    )
    print("----------------------------------------------------------------------")
    tabla(
        "->> Carga de trabajo - Cola de Listos:",
        cola_listos,
        ["PID", "TAM(KB)", "TA", "TI", "ESTADO"],
    )
    print("----------------------------------------------------------------------")
    tabla(
            "->> Procesos Finalizados:",
        cola_finalizados,
        ["PID", "TAM(KB)", "TA", "TI", "ESTADO"],
    )
    print("----------------------------------------------------------------------")


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
    while (len(cola_nuevos) > 0) and (cola_nuevos[0].tiempo_arribo <= clock) and (len(cola_listos) < 5):
            proceso = cola_nuevos.pop(0)
            for particion in memoria_principal.particiones:
                if particion.proceso is None:
                    if proceso.tamaño <= particion.tamaño:
                        asignar(proceso, particion)
                        break
                    
            if proceso.particion is None:
                proceso.estado = "Suspendido"
                # cola_suspendidos.append(proceso)
            # else:
            cola_listos.append(proceso)

def run(cola_nuevos: list[Proceso]):
    print("-------------- SIMULADOR -------------- (Fix me!)")
    memoria_principal = Memoria(
        [Particion(100), Particion(60), Particion(120), Particion(250)]
    )
    clock = 0
    quantum = 2
    cola_listos: list[Proceso] = []
    # cola_suspendidos: list[Proceso] = []
    cola_finalizados: list[Proceso] = []
    
    CPU_LIBRE = True
    tabla(
        "[ϴ] Carga de trabajo que ingresa al simulador (Cola de Nuevos):",
        cola_nuevos,
        ["PID", "TAM(KB)", "TA", "TI", "ESTADO"],
    )
    print("\n")


    while clock != cola_nuevos[0].tiempo_arribo:
        clock += 1

    while True:
        asignacion_a_memoria(cola_nuevos, cola_listos, memoria_principal, clock)

        # Round-Robin:
        if CPU_LIBRE:
            quantum = 2

        mostrar_estado(cola_nuevos, cola_listos, cola_finalizados, clock)
        input("[!] Ingrese Enter para continuar al siguiente tiempo de clock:")
        print(f"ACA! --->> {quantum}")
        
        # Acá! puede haber un error cuando queres ingresar a un índice dentro de una cola vacía
        proceso = cola_listos[0]
        proceso.estado = "Ejecutando"
        clock += 1
        proceso.tiempo_irrupcion -= 1
        CPU_LIBRE = False

        # mostrar_estado(cola_nuevos, cola_listos, clock)
        # input("[!] Ingrese Enter para continuar al siguiente tiempo de clock:")
        # print(f"ACA! --->> {quantum}")


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
                # cola_listos.append(proceso)
                CPU_LIBRE = True

        # mostrar_estado(cola_nuevos, cola_listos, clock)
        # input("[!] Ingrese Enter para continuar al siguiente tiempo de clock:")
        # print(f"ACA! --->> {quantum}")

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
                # cola_listos.append(p)

            proceso.estado = "Listo"
            min_particion.proceso = proceso


        continue

    print("Termino!")
