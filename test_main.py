from unittest.mock import patch

import pytest
import csv
import sys
from main import get_group_data, calculate_median, main


@pytest.fixture
def sample_csv(tmp_path):
    file_path = tmp_path / "test_data.csv"
    content = [
        ['student', 'coffee_spent'],
        ['Алексей', '400'],
        ['Алексей', '600'],
        ['Дарья', '200']
    ]
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(content)
    return str(file_path)


def test_get_group_data(sample_csv):
    """Проверяем, что данные группируются корректно"""
    result = get_group_data([sample_csv], 'student', 'coffee_spent')

    assert 'Алексей' in result
    assert result['Алексей'] == [400.0, 600.0]
    assert result['Дарья'] == [200.0]


def test_calculate_median(sample_csv):
    """Проверяем расчет медианы"""
    result = calculate_median([sample_csv], 'student', 'coffee_spent')

    res_dict = {row[0]: row[1] for row in result}

    assert res_dict['Алексей'] == 500.0
    assert res_dict['Дарья'] == 200.0


def test_file_not_found():
    """Проверяем реакцию на отсутствие файла"""
    with pytest.raises(SystemExit) as e:
        get_group_data(['non_existent.csv'], 'student', 'coffee_spent')
    assert e.value.code == 1


def test_invalid_data(tmp_path):
    """Проверяем обработку некорректных чисел (ValueError)"""
    file_path = tmp_path / "bad_data.csv"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("student,coffee_spent\nIvan,not_a_number")

    result = get_group_data([str(file_path)], 'student', 'coffee_spent')
    assert 'Ivan' not in result


def test_full_run_success(sample_csv, capsys):
    """Интеграционный тест, эмулирует запуск: python main.py --files test.csv --report median-coffee"""

    # Подменяем аргументы командной строки
    test_args = ["main.py", "--files", sample_csv, "--report", "median-coffee"]

    with patch.object(sys, 'argv', test_args):
        main()

    # Захватываем то, что программа напечатала в консоль
    captured = capsys.readouterr()

    # Проверяем, что в выводе есть таблица и знакомые имена
    assert "Student" in captured.out
    assert "Median Coffee" in captured.out
    assert "Алексей" in captured.out
    assert "500" in captured.out