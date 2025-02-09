"""Инструменты для ETL-процесса."""

import numpy as np
import pandas as pd
from smolagents import tool


@tool
def clean_salary(salary_range: str) -> float:
    """
    Allows you to get the numerical value salary from the salary range.

    # noqa: D401
    Returns int or float salary from salary range.

    Args:
        salary_range: Salary range from database, text.
    """
    if salary_range is None or salary_range == "None":
        return np.nan
    salary_range = (
        salary_range.replace(" руб.", "")
        .replace(" — ", "-")
        .replace(",", "")
        .replace("'", "")
        .replace(" ", "")
    )
    if salary_range.isalpha():  # noqa
        return np.nan
    elif "-" in salary_range:
        min_sal, max_sal = salary_range.split("-")
        return (int(min_sal) + int(max_sal)) / 2
    elif salary_range.startswith("Менее"):
        return int(salary_range.split("Менее")[1])
    elif salary_range.startswith("Более"):
        return int(salary_range.split("Более")[1])
    else:
        return int(salary_range)


def get_salary_value(data):
    """Усреднение зарплаты из интервала."""
    data = data[:]
    data["salary_range"] = data["salary_range"].map(
        lambda x: "Не указано" if x is None else x
    )
    data["salary"] = data["salary_range"].apply(clean_salary)
    data["first_salary"] = data.groupby("graduate")["salary"].transform(
        "first"
    )
    data["last_salary"] = data.groupby("graduate")["salary"].transform("last")
    return data


def rename_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Переименование столбцов датафрейма после импорта данных из БД."""
    data = data[:]
    data.rename(
        {
            "graduate": "Выпускник",
            "step": "Номер места работы",
            "company": "Название места работы",
            "position": "Должность",
            "salary_range": "Диапазон зарплаты",
            "graduation_year": "Год выпуска",
            "math_group": "Математический поток",
            "magistracy": "Магистратура",
            "salary": "Зарплата (среднее значение из диапазона)",
        },
        axis=1,
        inplace=True,
    )
    return data
