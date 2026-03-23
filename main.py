from typing import List, Dict, Any
from tabulate import tabulate
import statistics
import argparse
import csv
import sys


def get_group_data(files: List[str], id_col: str, val_col: str) -> Dict[str, List[float]]:
    """Собирает данные из нескольких CSV файлов в словарь по ID."""
    data = {}
    for path in files:
        try:
            with open(path, 'r', encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    student = row[id_col]
                    try:
                        value = float(row[val_col])
                    except ValueError:
                        print(f"Предупреждение: Некорректное число в файле {path}, строка пропущена.")
                        continue

                    data.setdefault(student, []).append(value)
        except FileNotFoundError:
            print(f"Ошибка: Файл {path} не найден.")
            sys.exit(1)
    return data


def calculate_median(files: List[str], id_col: str, val_col: str) -> List[List[str | float]] | None:
    """Расчет медианы."""
    grouped = get_group_data(files, id_col, val_col)

    if not grouped:
        print("Данные для отчета отсутствуют.")
        return None

    table_data = [
        [student, statistics.median(values)]
        for student, values in grouped.items()
    ]
    return table_data


def median_coffee(files: List[str]):
    """Формирование отчета по медиане трат на кофе."""

    table_data = calculate_median(files, 'student', 'coffee_spent')

    table_data.sort(key=lambda x: x[1], reverse=True)

    headers = ['Student', 'Median Coffee']

    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid", floatfmt=".0f"))


REPORTS: Dict[str, Any]  = {
        "median-coffee": median_coffee,
    }


def main() -> None:


    parser = argparse.ArgumentParser()
    parser.add_argument('--files', nargs='+',  required=True, help='Список файлов CSV')
    parser.add_argument('--report', choices=REPORTS.keys(), required=True, help='Список файлов CSV')

    args = parser.parse_args()

    REPORTS[args.report](args.files)


if __name__ == '__main__':
    main()