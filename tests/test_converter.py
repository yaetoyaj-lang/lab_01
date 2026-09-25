import pytest

from toolkit.converter import convert
from toolkit.errors import (
    AbsoluteZeroError,
    IncompatibleUnitsError,
    InvalidValueError,
    UnknownUnitError,
)


def test_length_km_to_m():
    assert convert(1, "km", "m") == 1000.0


def test_length_mm_to_cm():
    assert convert(10, "mm", "cm") == 1.0


def test_mass_kg_to_g():
    assert convert(1, "kg", "g") == 1000.0


def test_mass_case_insensitive():
    assert convert(1, "KM", "M") == 1000.0
    assert convert(1, "KG", "G") == 1000.0


def test_temperature_c_to_k():
    assert convert(0, "c", "k") == pytest.approx(273.15)


def test_temperature_f_to_c():
    assert convert(32, "f", "c") == pytest.approx(0.0)


def test_temperature_k_to_c():
    assert convert(273.15, "k", "c") == pytest.approx(0.0)


def test_unknown_unit():
    with pytest.raises(UnknownUnitError):
        convert(1, "xyz", "m")


def test_incompatible_units():
    with pytest.raises(IncompatibleUnitsError):
        convert(1, "m", "kg")


def test_invalid_value():
    with pytest.raises(InvalidValueError):
        convert("abc", "m", "km")


def test_absolute_zero_c():
    with pytest.raises(AbsoluteZeroError):
        convert(-300, "c", "k")


def test_absolute_zero_k():
    with pytest.raises(AbsoluteZeroError):
        convert(-1, "k", "c")


def test_temperature_result_float():
    assert isinstance(convert(0, "c", "k"), float)
