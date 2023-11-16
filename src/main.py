import sys, traceback, argparse
from pathlib import Path
from prompt import Prompt
from sim import Run
from utils import generar_desde_archivo

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--full-run",
        action="store_true",
        help="Habilita a mostrar la información en cada tiempo del clock.",
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
            Run(cola_nuevos, args.full_run)
        else:
            Prompt(args.full_run)

    except KeyboardInterrupt:
        print("\nSimulador apagándose..")
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    main()
