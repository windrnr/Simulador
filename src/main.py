import sys, traceback, argparse
from pathlib import Path
from prompt import Prompt
from sim import Run
from utils import generar_desde_archivo


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="Simulador",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage="%(prog)s [options]",
        description=
        '''\
        Trabajo Práctico Integrador de Sistemas Operativos. Simulador de asignación de memoria y planificación de procesos.\n 
        Autores: Acosta Quintana, L. Stegmayer, T. Vallejos, E. Zappa, E. Obregón, E.
        ''',
        epilog="Github Repo: https://github.com/lau-acosta/Simulador"
    )
    parser.add_argument(
        "-f",
        "--full-run",
        action="store_true",
        help="Muestra la información en cada clock, esperando al usuario.",
    )
    parser.add_argument(
        "-i",
        "--ininterrumpido",
        action="store_true",
        help="Muestra la información sin esperar al usuario.",
    )
    parser.add_argument(
        "file_path",
        type=Path,
        nargs="?",
        default=None,
        help="Dirección del archivo con los procesos (opcional).",
    )
    args = parser.parse_args()

    try:
        if args.file_path is not None:
            cola_nuevos = generar_desde_archivo(args.file_path, 10)
            Run(cola_nuevos, args.full_run, args.ininterrumpido)
        else:
            Prompt(args.full_run, args.ininterrumpido)

    except KeyboardInterrupt:
        print("\nSimulador apagándose..")
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    main()
