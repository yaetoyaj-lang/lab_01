import pytest

from toolkit.calculator import calculate, to_rpn, tokenize
from toolkit.errors import (
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidTokenError,
    MissingOperandError,
    TwoOperatorsError,
)


def test_simple_add():
    assert calculate("2 + 3") == 5.0


def test_precedence():
    assert calculate("2 + 3 * 4") == 14.0


def test_unary_minus():
    assert calculate("-5 + 3") == -2.0


def test_unary_plus():
    assert calculate("+5 + +3") == 8.0


def test_float():
    assert calculate("2.5 * 2") == 5.0


def test_spaces_ignored():
    assert calculate("  2   +   3  ") == 5.0


def test_floor_division_positive():
    assert calculate("7 // 2") == 3.0


def test_floor_division_negative():
    assert calculate("-3 // 2") == -2.0


def test_modulo_negative():
    assert calculate("-3 % 2") == 1.0


def test_modulo_positive():
    assert calculate("7 % 3") == 1.0


def test_rpn_direct():
    assert to_rpn(["2", "+", "3", "*", "4"]) == ["2", "3", "4", "*", "+"]


def test_tokenize_regex():
    assert tokenize(" -3.5 * +2 // 3 ") == ["-3.5", "*", "2", "//", "3"]


def test_decimal_precision():
    assert calculate("0.1 + 0.2") == pytest.approx(0.3)



def test_empty_expression():
    with pytest.raises(EmptyExpressionError):
        calculate("   ")


def test_invalid_symbol():
    with pytest.raises(InvalidTokenError):
        calculate("2 & 3")


def test_missing_operand():
    with pytest.raises(MissingOperandError):
        calculate("2 +")


def test_two_operators():
    with pytest.raises(TwoOperatorsError):
        calculate("2 + * 3")


def test_division_by_zero():
    with pytest.raises(DivisionByZeroError):
        calculate("5 / 0")


def test_division_by_zero_floor():
    with pytest.raises(DivisionByZeroError):
        calculate("5 // 0")


def test_division_by_zero_mod():
    with pytest.raises(DivisionByZeroError):
        calculate("5 % 0")
