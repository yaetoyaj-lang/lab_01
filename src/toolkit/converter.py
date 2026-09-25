from .errors import AbsoluteZeroError, IncompatibleUnitsError, InvalidValueError, UnknownUnitError

_LENGTH_TO_M = {"mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0}
_MASS_TO_G = {"g": 1.0, "kg": 1000.0}

_UNIT_TO_GROUP = {
    "mm": "length",
    "cm": "length",
    "m": "length",
    "km": "length",
    "g": "mass",
    "kg": "mass",
    "c": "temperature",
    "f": "temperature",
    "k": "temperature",
}


def _normalize_unit(unit: str) -> str:
    """Убрать пробелы и сделать буквы маленькими."""
    return unit.strip().lower()


def _get_group(unit: str) -> str:
    """Определить группу единицы."""
    if unit not in _UNIT_TO_GROUP:
        raise UnknownUnitError(f"неизвестная единица '{unit}'")
    return _UNIT_TO_GROUP[unit]


def _check_absolute_zero(value: float, unit: str) -> None:
    """Проверка температуры не ниже абсолютного нуля."""
    if unit == "c" and value < -273.15:
        raise AbsoluteZeroError(f"температура ниже абсолютного нуля: {value} c")
    if unit == "f" and value < -459.67:
        raise AbsoluteZeroError(f"температура ниже абсолютного нуля: {value} f")
    if unit == "k" and value < 0:
        raise AbsoluteZeroError(f"температура ниже абсолютного нуля: {value} k")


def _convert_temperature(value: float, from_u: str, to_u: str) -> float:
    """Перевод температуры через кельвины."""
    if from_u == "k":
        kelvin = value
    elif from_u == "c":
        kelvin = value + 273.15
    elif from_u == "f":
        kelvin = (value - 32) * 5 / 9 + 273.15
    else:
        raise UnknownUnitError(from_u)

    if kelvin < -1e-9:
        raise AbsoluteZeroError("температура ниже абсолютного нуля (K<0)")

    if to_u == "k":
        return float(kelvin)
    if to_u == "c":
        return float(kelvin - 273.15)
    if to_u == "f":
        return float((kelvin - 273.15) * 9 / 5 + 32)
    raise UnknownUnitError(to_u)


def convert(value, from_unit, to_unit) -> float:
    """Перевод величины из from_unit в to_unit, ответ float."""
    try:
        if isinstance(value, str):
            if value.strip() == "":
                raise ValueError("пустое значение")
            numeric = float(value.strip())
        else:
            numeric = float(value)
    except (ValueError, TypeError) as e:
        raise InvalidValueError(f"неверное числовое значение '{value}'") from e

    from_u = _normalize_unit(from_unit)
    to_u = _normalize_unit(to_unit)

    from_group = _get_group(from_u)
    to_group = _get_group(to_u)

    if from_group != to_group:
        raise IncompatibleUnitsError(f"несовместимые единицы: '{from_unit}' ({from_group}) и '{to_unit}' ({to_group})")

    if from_group == "length":
        meters = numeric * _LENGTH_TO_M[from_u]
        result = meters / _LENGTH_TO_M[to_u]
        return float(result)
    if from_group == "mass":
        grams = numeric * _MASS_TO_G[from_u]
        result = grams / _MASS_TO_G[to_u]
        return float(result)
    if from_group == "temperature":
        _check_absolute_zero(numeric, from_u)
        result = _convert_temperature(numeric, from_u, to_u)
        _check_absolute_zero(result, to_u)
        return float(result)

    raise IncompatibleUnitsError(f"неизвестная группа для '{from_u}' -> '{to_u}'")
