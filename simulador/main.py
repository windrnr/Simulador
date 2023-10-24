import argparse
from sim import Queue, print_table
from pathlib import Path


class Memoria:
    def __init__ (self, layout: list):
        self.PP: Particion = layout[1]
        self.PM: Particion = layout[2]
        self.PG: Particion = layout[3]

class Particion:
    def __init__(self, size: int):
        self.size = size
        self.ifrag = 0
        self. used = False

def asign(p: Particion, size: int):
    q, r = divmod(p.size, size)
    p.size -= q * size
    p.ifrag = r
    p.used = True



def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file_path", type=Path, help="Dirección del archivo con los procesos."
    )
    args = parser.parse_args()

    try:
        clock = 0
        cola_nuevos = Queue(10)
        cola_nuevos.load_from_file(args.file_path)
        print_table(
            "->> Carga de trabajo:",
            cola_nuevos._data,
            ["PID", "TAM(KB)", "TA", "TI"],
        )
        cola_listos = Queue(5)

        memoria = Memoria([Particion(100), Particion(60), Particion(120), Particion(250)])
        
        # Prestar atención que la condición está incompleta por el momento, tendría que controlar la longitud de la cola de listos también.
        while (cola_nuevos._lenght !=0):
            while(clock != cola_nuevos._data[0].get_tiempo_arribo()):
                clock += 1

            cola_listos.load_from_queue(cola_nuevos)
            # print_table("->> Tabla de cola de nuevos después de cargar la cola de listos:", new_queue._data, ["PID", "TAM(KB)", "TA", "TI"])
            # print_table("->> Tabla de cola de listos:", ready_queue._data, ["PID", "TAM(KB)", "TA", "TI"])

            # Revisar en el diagrama de flujo la condición "Todos los proceso de CL están en MP o Disco"
            # Nunca van a estar los 5 procesos de la cola en la memoria principal, como máximo 3.
            # Tal vez se refiera a otra cosa pero no queda claro.
            
            # BestFit:
            for process in cola_listos._data:
                size = process.get_tamaño()
                if size <= memoria.PP.size:
                    if memoria.PP.used == False:
                        asign(memoria.PP, size)
                        process._executing = True
                
                elif size <= memoria.PM.size:
                    if memoria.PM.used == False:
                        asign(memoria.PM, size)
                        process._executing = True
                else:
                    if memoria.PG.used == False:
                        asign(memoria.PG, size)
                        process._executing = True
            
            #Round-Robin:
            while (cola_listos._lenght != 0):
                break


            break



    except ValueError as e:
        print(f"Error: Extensión incorrecta. {e}")
    except FileNotFoundError as e:
        print(f"Error: {e} El archivo no existe o no es encontrado.")
    except IsADirectoryError as e:
        print(f"Error: El path: {e}")


if __name__ == "__main__":
    main()
