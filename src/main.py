import argparse
from pathlib import Path
from sim import cargar_desde_archivo, ColaCircular, print_table, Particion, Memoria

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file_path", type=Path, help="Dirección del archivo con los procesos."
    )
    args = parser.parse_args()

    try:
        cola_nuevos = ColaCircular(10)
        cargar_desde_archivo(cola_nuevos, args.file_path)
        print_table(
            "->> Carga de trabajo:",
            cola_nuevos.buffer,
            ["PID", "TAM(KB)", "TA", "TI"],
        )
        memoria_principal = Memoria(
            [Particion(100), Particion(60), Particion(120), Particion(250)]
        )
        memoria_secundaria = []

        clock = 0
        cola_listos = ColaCircular(5)
        CPU = None 

        # Prestar atención que la condición está incompleta por el momento, tendría que controlar la longitud de la cola de listos también.
        while(True):
            while clock != cola_nuevos.peek().get_tiempo_arribo():
                clock += 1
            
            while (cola_listos.largo < 5):
                proceso = cola_nuevos.unshift()
                cola_listos.shift(proceso)



                if (cola_nuevos.peek().get_tiempo_arribo() <= clock):
                    continue
                break
            
            print_table(
                    "->> Carga de trabajo:",
                    cola_listos.buffer,
                    ["PID", "TAM(KB)", "TA", "TI"],
                    )
            # Best-Fit:
            while(True): # TODO: Actualizar con la correcta evaluación de salida
                if (memoria_principal.particion_pequeña.usada == False):
                    if (cola_listos.peek().get_tamaño() <= memoria_principal.particion_pequeña.tamaño):
                        memoria_principal.procesos.shift(cola_listos.unshift())
                        memoria_principal.particion_pequeña.usada = True
                        continue
                    elif (memoria_principal.particion_mediana.usada == False):
                        if (cola_listos.peek().get_tamaño() <= memoria_principal.particion_mediana.tamaño):
                            memoria_principal.procesos.shift(cola_listos.unshift())
                            memoria_principal.particion_mediana.usada = True
                            continue
                        elif (memoria_principal.particion_grande.usada == False):
                            memoria_principal.procesos.shift(cola_listos.unshift())
                            memoria_principal.particion_grande.usada = True
                            continue
                        else: 
                            # TODO: REVISAR ESTO
                            memoria_secundaria.append(cola_listos.unshift())

                break # TODO: Retirar esto cuando se conozca bien la condición de salida
            

            # Round-Robin:
            if(CPU == None):
                quantum = 2
                # Ver si está bien sumarle +1 al clock en este instante
                clock += 1
                proceso = memoria_principal.procesos.peek()
                # TODO: Fijarme que cuando cargo procesos de un archivo, no haya alguno con un tiempo de irrupcion <= 0
                proceso.tiempo_irrupcion -= 1
                if (proceso.tiempo_irrupcion == 0):
                    CPU = None
                    # TODO: Ver como actualizar el estado de la partición correspondiente

                    if (cola_listos.largo == 0 and cola_nuevos.largo == 0):
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
