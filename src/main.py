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


                #TODO: ESTO DEBERÍA SER UN WHILE?
                if (cola_nuevos.peek().get_tiempo_arribo() <= clock):
                    continue
                break
            

            # Primera carga:
            cola_ejecucion = []
            while(True): # TODO: Actualizar con la correcta evaluación de salida
                if (memoria_principal.particion_pequeña.usada == False):
                    if (cola_listos.peek().get_tamaño() <= memoria_principal.particion_pequeña.tamaño):
                        particion = memoria_principal.particion_pequeña
                        particion.usada = True
                        proceso = cola_listos.unshift()
                        if (proceso):
                            proceso.cargado = True

                        cola_ejecucion.append((proceso, particion))

                        continue
                    elif (memoria_principal.particion_mediana.usada == False):
                        if (cola_listos.peek().get_tamaño() <= memoria_principal.particion_mediana.tamaño):
                            particion = memoria_principal.particion_mediana
                            particion.usada = True
                            proceso = cola_listos.unshift()

                            cola_ejecucion.append((proceso, particion))
                            continue
                        elif (memoria_principal.particion_grande.usada == False):
                            particion = memoria_principal.particion_grande
                            particion.usada = True
                            proceso = cola_listos.unshift()

                            cola_ejecucion.append((proceso, particion))
                            continue
                        else: 
                            # TODO: REVISAR ESTO
                            memoria_secundaria.append(cola_listos.unshift())

                break # TODO: <-Retirar esto cuando se conozca bien la condición de salida
            

            # Round-Robin:
            if(CPU == None):
                quantum = 2
                proceso, particion = cola_ejecucion.pop()
                
                clock += 1
                proceso.tiempo_irrupcion -= 1
                # TODO: Fijarme que cuando cargo procesos de un archivo, no haya alguno con un tiempo de irrupcion <= 0
                if (proceso.tiempo_irrupcion == 0):
                    CPU = None
                    particion.usada = False
                    if (cola_listos.largo == 0 and cola_nuevos.largo == 0):
                        break 
                else:
                    quantum -= 1
                    if (quantum == 0):
                        cola_listos.shift(proceso)
                        particion.usada = False
                        CPU = None
                    else:
                        print("TODO")
                
                proceso_n = cola_listos.unshift()
                if (proceso_n):
                    if(not proceso_n.cargado):
                        # Best-Fit
                        print("TODO")

                        min = particion, particion.tamaño - proceso_n.tamaño 
                        for particion in memoria_principal.particiones:
                            frag_in = particion.tamaño - proceso_n.tamaño
                            if(min[1] > frag_in and frag_in >= 0):
                                min = particion, frag_in 

                        if(min[0].usada):
                            proceso.cargado = False
                        else:
                            proceso_n.cargado = True
                            min[0].usada = True
                        # Una mejor solución podría ser que particion conozca al proceso que alberga en un instante.








                    

            break

    except ValueError as e:
        print(f"Error: Extensión incorrecta. {e}")
    except FileNotFoundError as e:
        print(f"Error: {e} El archivo no existe o no es encontrado.")
    except IsADirectoryError as e:
        print(f"Error: El path: {e}")


if __name__ == "__main__":
    main()
