class ToolkitError(Exception):
    """Базовая ошибка всего toolkit. От неё наследуются все остальные."""

    pass


class CalculatorError(ToolkitError):
    """Базовая ошибка калькулятора."""

    pass


class EmptyExpressionError(CalculatorError):
    """Пустое выражение. Например: "" или "   "."""

    pass


class InvalidTokenError(CalculatorError):
    """Недопустимый символ. Например: "2 & 3" или "2a + 3"."""

    pass


class MissingOperandError(CalculatorError):
    """Пропущенный операнд. Например: "2 +" или "* 3" или "2 3 +"."""

    pass


class TwoOperatorsError(CalculatorError):
    """Два бинарных оператора подряд. Например: "2 + * 3" или "2 // * 3"."""

    pass


class DivisionByZeroError(CalculatorError):
    """Деление на ноль: / , // , % с нулевым делителем."""

    pass


class ConverterError(ToolkitError):
    """Базовая ошибка конвертера."""

    pass


class UnknownUnitError(ConverterError):
    """Неизвестная единица. Например: --from xyz."""

    pass


class IncompatibleUnitsError(ConverterError):
    """Несовместимые единицы. Например: m -> kg."""

    pass


class InvalidValueError(ConverterError):
    """Неверное числовое значение. Например: VALUE = "abc"."""

    pass


class AbsoluteZeroError(ConverterError):
    """Температура ниже абсолютного нуля. Например: -300 C или -1 K."""

    pass
