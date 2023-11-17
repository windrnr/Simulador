# Simulador de asignación de memoria y planificación de procesos

## Uso:

Para ejecutar el programa nos debemos posicionar en la carpeta dist:

Linux:
./Capybara

Windows:
.\Capybara.exe

Luego debemos elegir si cargar los procesos por terminal o desde un archivo json o csv

- Selección de Terminal:
  Se debe ingresar la cantidad de procesos a cargar y de cada proceso el ID, tiempo de arribo (TA), tiempo de irrupción (TI) y Tamaño (TAM)
- Selección de Archivo:
  Se debe ingresar el path del archivo, por ejemplo: ../test/test-1ConTA10.json

Una vez cargada la carga de trabajo solo se debe avanzar con enter hasta que termina.
Si se desea finalizar antes de tiempo presione ctrl+c

Otra forma de ejecutar el programa es llamar al Archivo json o csv de la siguiente manera:

Linux:
./Capybara ../test/<nombre-archivo.extensión>

Windows:
.\Capybara.exe ..\test\<nombre-archivo.extensión>

## Comandos:

-h: abre una interfaz de ayuda donde se especifica el uso de los comandos -i y -f.
-i: ejecuta el programa sin interrupciones.
-f: ejecuta el programa avanzando el clock de a 1.
-if o -fi: combina los comandos -i y -f, ejecutando el programa sin interrupciones y avanzando de a 1 el clock

Linux:
./Capybara -<comando>

Windows:
.\Capybara.exe -<comando>

## Ejecución con comando y archivo incluido

Puede combinar todas las formas de ejecucion:

Linux:
./Capybara -comando ../test/nombre-archivo.extensión

Windows:
.\Capybara.exe -comando ..\test\<nombre-archivo.extensión>
