import argparse
import sys

from .calculator import calculate, save_history
from .converter import convert
from .errors import ToolkitError


def build_parser() -> argparse.ArgumentParser:
    """Сборка парсера для calc и convert."""
    parser = argparse.ArgumentParser(prog="toolkit", description="Калькулятор и конвертер")
    sub = parser.add_subparsers(dest="command")

    calc = sub.add_parser("calc", help="посчитать выражение")
    calc.add_argument("expression", help="например '2 + 2 * 2'")

    conv = sub.add_parser("convert", help="перевести величину")
    conv.add_argument("value", help="число")
    conv.add_argument("--from", dest="from_unit", required=True, help="из чего")
    conv.add_argument("--to", dest="to_unit", required=True, help="во что")
    return parser


def main(argv=None) -> None:
    """Запуск CLI, ошибки в stderr с кодом 2."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        if argv is None:
            argv = sys.argv[1:]
        if "--help" in argv or "-h" in argv:
            parser.print_help(sys.stdout)
            sys.exit(0)
        parser.print_help(sys.stderr)
        sys.exit(2)

    try:
        if args.command == "calc":
            result = calculate(args.expression)
            print(result)
            save_history(args.expression, result)
        elif args.command == "convert":
            print(convert(args.value, args.from_unit, args.to_unit))
    except ToolkitError as e:
        print(f"ошибка: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
