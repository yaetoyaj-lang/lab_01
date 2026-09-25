import json
import re
from decimal import ROUND_FLOOR, ROUND_HALF_UP, Decimal, getcontext

from .errors import (
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidTokenError,
    MissingOperandError,
    TwoOperatorsError,
)

getcontext().prec = 28
getcontext().rounding = ROUND_HALF_UP

_NUMBER_RE = r"(?:\d+\.\d*|\.\d+|\d+)"
_OPERATOR_RE = r"//|[%+\-*/()]"
_TOKEN_RE = re.compile(rf"{_NUMBER_RE}|{_OPERATOR_RE}")
_FULL_NUMBER_RE = re.compile(rf"^{_NUMBER_RE}$")

_OPERATORS = {"+", "-", "*", "/", "//", "%"}
_PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "//": 2, "%": 2}


def tokenize(expression: str) -> list[str]:
    """Разбить строку на токены, пробелы пропустить."""
    if expression.strip() == "":
        raise EmptyExpressionError("пустое выражение")

    tokens = []
    pos = 0
    while pos < len(expression):
        if expression[pos].isspace():
            pos += 1
            continue
        match = _TOKEN_RE.match(expression, pos)
        if match:
            tokens.append(match.group(0))
            pos = match.end()
        else:
            raise InvalidTokenError(f"недопустимый символ '{expression[pos]}'")

    if not tokens:
        raise EmptyExpressionError("пустое выражение")

    # склейка минуса с числом: "-5", "2 * -3"
    merged: list[str] = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        first_or_after_op = len(merged) == 0 or merged[-1] in _OPERATORS or merged[-1] == "("
        if tok in ("+", "-") and first_or_after_op:
            sign = 1
            k = i
            while k < len(tokens) and tokens[k] in ("+", "-"):
                if tokens[k] == "-":
                    sign = -sign
                k += 1
                if k < len(tokens) and _FULL_NUMBER_RE.match(tokens[k]):
                    num = tokens[k]
                    if sign == -1:
                        merged.append("-" + num)
                    else:
                        merged.append(num)
                    i = k + 1
                    break
                elif k < len(tokens) and tokens[k] in ("+", "-"):
                    continue
                else:
                    merged.append(tok)
                    i += 1
                    break
            else:
                merged.append(tok)
                i += 1
            continue
        else:
            merged.append(tok)
            i += 1

    return merged


def validate(tokens: list[str]) -> None:
    """Проверка токенов: число, знак, число."""
    if not tokens:
        raise EmptyExpressionError("пустое выражение")

    def is_number(tok: str) -> bool:
        try:
            Decimal(tok)
            return True
        except Exception:
            return False

    if not is_number(tokens[0]):
        raise MissingOperandError(f"пропущен операнд перед '{tokens[0]}'")
    if not is_number(tokens[-1]):
        raise MissingOperandError(f"пропущен операнд после '{tokens[-1]}'")

    for idx, tok in enumerate(tokens):
        is_num = is_number(tok)
        is_op = tok in _OPERATORS
        if not is_num and not is_op:
            raise InvalidTokenError(f"недопустимый токен '{tok}'")
        if idx > 0:
            prev_is_num = is_number(tokens[idx - 1])
            if prev_is_num and is_num:
                raise MissingOperandError(f"пропущен оператор между '{tokens[idx-1]}' и '{tok}'")
            prev_is_op = tokens[idx - 1] in _OPERATORS
            if prev_is_op and is_op:
                raise TwoOperatorsError(f"два оператора подряд: '{tokens[idx-1]}' и '{tok}'")


def to_rpn(tokens: list[str]) -> list[str]:
    """Переделка в обратную польскую запись для счета стеком."""
    output: list[str] = []
    op_stack: list[str] = []

    def is_number(tok: str) -> bool:
        try:
            Decimal(tok)
            return True
        except Exception:
            return False

    for tok in tokens:
        if is_number(tok):
            output.append(tok)
        elif tok in _OPERATORS:
            # вытолкнуть знаки с приоритетом больше или равным
            while op_stack and op_stack[-1] in _OPERATORS:
                top = op_stack[-1]
                if _PRECEDENCE[tok] <= _PRECEDENCE[top]:
                    output.append(op_stack.pop())
                else:
                    break
            op_stack.append(tok)
        elif tok == "(":
            op_stack.append(tok)
        elif tok == ")":
            while op_stack and op_stack[-1] != "(":
                output.append(op_stack.pop())
            if not op_stack:
                raise InvalidTokenError("несогласованные скобки")
            op_stack.pop()  # убрать "("
        else:
            raise InvalidTokenError(f"неизвестный токен в to_rpn: '{tok}'")

    while op_stack:
        top = op_stack.pop()
        if top in ("(", ")"):
            raise InvalidTokenError("несогласованные скобки")
        output.append(top)

    return output


def evaluate_rpn(rpn: list[str]) -> Decimal:
    """Счет RPN стеком через Decimal."""
    stack: list[Decimal] = []

    def is_number(tok: str) -> bool:
        try:
            Decimal(tok)
            return True
        except Exception:
            return False

    for tok in rpn:
        if is_number(tok):
            stack.append(Decimal(tok))
        elif tok in _OPERATORS:
            if len(stack) < 2:
                raise MissingOperandError(f"недостаточно операндов для '{tok}'")
            right = stack.pop()
            left = stack.pop()

            if tok == "+":
                res = left + right
            elif tok == "-":
                res = left - right
            elif tok == "*":
                res = left * right
            elif tok == "/":
                if right == 0:
                    raise DivisionByZeroError("деление на ноль")
                res = left / right
            elif tok == "//":
                if right == 0:
                    raise DivisionByZeroError("деление на ноль")
                res = (left / right).to_integral_value(rounding=ROUND_FLOOR)
            elif tok == "%":
                if right == 0:
                    raise DivisionByZeroError("деление на ноль")
                floored = (left / right).to_integral_value(rounding=ROUND_FLOOR)
                res = left - floored * right
            else:
                raise InvalidTokenError(f"неизвестный оператор '{tok}'")

            stack.append(res)
        else:
            raise InvalidTokenError(f"неизвестный токен в evaluate_rpn: '{tok}'")

    if len(stack) != 1:
        raise MissingOperandError("неверное количество операндов после вычисления")

    return stack[0]


def calculate(expression: str) -> float:
    """Главная функция: токены, проверка, RPN и ответ."""
    tokens = tokenize(expression)
    validate(tokens)
    rpn = to_rpn(tokens)
    result = evaluate_rpn(rpn)
    return float(result)


def save_history(task: str, result: float) -> None:
    """Записывает историю вычислений!"""
    try:
        with open("history.json", "r", encoding="utf-8") as file:
            history = json.load(file)
    except FileNotFoundError:
        history = []

    history.append({"expression": task, "result": result})

    with open("history.json", "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=4)
