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
        clock = 0
        cola_listos = ColaCircular(5)
        CPU = None 

        # Prestar atención que la condición está incompleta por el momento, tendría que controlar la longitud de la cola de listos también.
        while clock != cola_nuevos.peek().tiempo_arribo:
            clock += 1

        while(True):
            while (cola_nuevos.peek().tiempo_arribo <= clock):
                if (cola_listos.largo < 5):
                    for particion in memoria_principal.particiones:
                        proceso = cola_nuevos.unshift()
                            # ACA asignar(proceso, particion)
                        if (proceso):
                            if(not particion.proceso):
                                match proceso.tamaño:
                                    case n if n <= 60:
                                        proceso.estado = "Listo"
                                        particion[1].proceso = proceso
                                        particion[1].frag_in = particion.tamaño - proceso.tamaño
                                        proceso.particion = particion[1]
                                    case n if n <= 120:
                                        proceso.estado = "Listo"
                                        particion[2].proceso = proceso
                                        particion[2].frag_in = particion.tamaño - proceso.tamaño
                                        proceso.particion = particion[2]
                                    case n if n <= 250:
                                        proceso.estado = "Listo"
                                        particion[3].proceso = proceso
                                        particion[3].frag_in = particion.tamaño - proceso.tamaño
                                        proceso.particion = particion[3]
                            else:
                                proceso.estado = "Suspendido"
                            cola_listos.shift(proceso)
                else: 
                    break

             # Round-Robin:
                # Revisar este condicional
            if(CPU):
                clock += 1
            else:
                # Revisar porque acá estoy sacando de la cola de listos. Si hacemos un print no va a aparecer
                proceso = cola_listos.unshift()
                if (proceso):
                    while (proceso.estado == "Listo"):
                        proceso.estado = "Ejecutando"
                        quantum = 2
                        clock += 1
                        proceso.tiempo_irrupcion -= 1

                        if (proceso.tiempo_irrupcion == 0):
                            proceso.estado = "Saliente"
                            if (proceso.particion):
                                proceso.particion.proceso = None
                            CPU = None
                            if (cola_listos.largo == 0 and cola_nuevos.largo == 0):
                                # TODO: Se supone que termina
                                print("TODO: Se supone que termina")

                        quantum -= 1
                        if (quantum != 0):
                            # TODO: vuelvo al inicio
                            print("TODO: vuelvo al inicio")
                            continue
                        
                        cola_listos.shift(proceso)
                        CPU = None
                        if(cola_listos.peek().estado == "Listo"):
                            # TODO: vuelvo al inicio
                            print("TODO: vuelvo al inicio")
                            continue
                        
                        p = cola_listos.unshift()
                        if (p):
                            min:int = 1000 
                            min_part = Particion
                            tmp = 0
                            for particion in memoria_principal.particiones:
                                tmp = particion.tamaño - p.tamaño
                                if (min > tmp):
                                    min = tmp
                                    min_part = particion

                            if (not min_part.proceso):


                                



                    # proceso.tiempo_irrupcion -= 1
                    # clock += 1
                    # # TODO: Fijarme que cuando cargo procesos de un archivo, no haya alguno con un tiempo de irrupcion <= 0
                    # if (proceso.tiempo_irrupcion == 0):
                    #     CPU = None
                    #     particion.usada = False
                    #     if (cola_listos.largo == 0 and cola_nuevos.largo == 0):
                    #         break 
                    # else:
                    #     quantum -= 1
                    #     if (quantum == 0):
                    #         cola_listos.shift(proceso)
                    #         particion.usada = False
                    #         CPU = None
                    #     else:
                    #         print("TODO")
                    
                    # proceso_n = cola_listos.unshift()
                    # if (proceso_n):
                    #     if(not proceso_n.cargado):
                    #         # Best-Fit
                    #         print("TODO")

                    #         min = particion, particion.tamaño - proceso_n.tamaño 
                    #         for particion in memoria_principal.particiones:
                    #             frag_in = particion.tamaño - proceso_n.tamaño
                    #             if(min[1] > frag_in and frag_in >= 0):
                    #                 min = particion, frag_in 

                    #         if(min[0].usada):
                    #             proceso.cargado = False
                    #         else:
                    #             proceso_n.cargado = True
                    #             min[0].usada = True
                    #         # Una mejor solución podría ser que particion conozca al proceso que alberga en un instante.








                    


    except ValueError as e:
        print(f"Error: Extensión incorrecta. {e}")
    except FileNotFoundError as e:
        print(f"Error: {e} El archivo no existe o no es encontrado.")
    except IsADirectoryError as e:
        print(f"Error: El path: {e}")


if __name__ == "__main__":
    main()
