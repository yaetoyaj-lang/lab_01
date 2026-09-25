# Лаба 1 — калькулятор и конвертер

Пакет `toolkit`: калькулятор (`calculator.py`) и конвертер (`converter.py`).

## Как пользоваться

Через CLI:

```bash
python -m toolkit calc "2 + 3 * 4"  # 14.0
python -m toolkit convert 1 --from km --to m  # 1000.0
python -m toolkit --help
```

## Файлы

- `src/toolkit/calculator.py` — `tokenize`, `validate`, `to_rpn`, `evaluate_rpn`, `calculate`, `save_history`
- `src/toolkit/converter.py` — `convert`
- `src/toolkit/errors.py` — ошибки
- `src/toolkit/__main__.py` — CLI
- `tests/` — тесты ядра

## Калькулятор

- Числа целые и дробные, `+ - * / // %`
- Унарный плюс/минус перед числом (`-3 // 2 == -2`)
- Пробелы не важны
- `* / // %` считаются раньше `+ -`
- Считаем через `Decimal`, потом отдаем `float`
- Внутри `tokenize` / `validate` / `to_rpn` + `evaluate_rpn` стеком

## Конвертер

- Длина: `mm cm m km`, масса: `g kg`, температура: `c f k`
- Регистр не важен (`KM` = `km`)
- Между группами нельзя (`m` -> `kg` ошибка)
- Температура ниже абсолютного нуля запрещена
- Ответ всегда `float`

## Проверки

```bash
python -m pytest
ruff check src tests
```
