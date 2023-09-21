# Simulador de asignación de memoria y planificación de procesos

## Material de Interés:
- Trello: https://shorturl.at/xH047
- Libro de William Stallings: https://shorturl.at/mJLU6
- Libro de Tanenbaum: https://shorturl.at/jzQZ8
- **En el archivo Git.md** les dejé una descripción de los pasos a realizar para descargar el repositorio y poder contribuir usando git.

## Consigna
El simulador deberá brindar la posibilidad de cargar procesos por parte del usuario. Para facilitar la implementación se permitirán como máximo 10 procesos y la asignación de memoria se realizará con particiones fijas. El esquema de particiones será el siguiente:
- 100K destinados al Sistema Operativo.
- 250K para trabajos los más grandes.
- 120K para trabajos medianos.
- 60K para trabajos pequeños.

## Funcionamiento
- El programa debe permitir ingreso de nuevos procesos cuando sea posible ( **manteniendo el grado de
multiprogramación en 5** ). 
- La política de asignación de memoria será Best-Fit.
- Por cada proceso se debe ingresar o leer desde un archivo:
    - ID de proceso.
    - Tamaño del proceso. 
    - Tiempo de arribo 
    - Tiempo de irrupción.
- La planificación de CPU será dirigida por un algoritmo Round-Robin con q=2.
- Las presentaciones de salida deberán realizarse cada vez que llega un nuevo proceso y cuando se termina un proceso en ejecución.
- No se permiten corridas ininterrumpidas de simulador, desde que se inicia la simulación hasta que termina el último proceso. (Quiere que el usuario controle el avance del programa, presionando enter o cualquier otro método).

### El simulador deberá presentar como salida la siguiente información:
- El estado del procesador (proceso que se encuentra corriendo en ese instante)
- La tabla de particiones de memoria, la cual deberá contener (Id de partición, dirección de comienzo de
partición, tamaño de la partición, id de proceso asignado a la partición, fragmentación interna)
- El estado de la cola de procesos listos.
- Al finalizar la simulación se deberá presentar un informe estadístico con, tiempo de retorno y espera para cada
proceso y los respectivos tiempos promedios.

## Fechas de Entrega:
- 10/10
- 07/11
- 14/11
- La entrega final será el 21 de noviembre.
- El **coloquio de defensa del TPI se llevará a cabo el 28/11 o 07/12** (a confirmar para cada grupo).


