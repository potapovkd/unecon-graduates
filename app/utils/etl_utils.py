"""Инструменты для ETL-процесса."""

import tempfile
import traceback
from json import loads

import numpy as np
import pandas as pd
import requests
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


def create_unique_id_generator():
    """Функция для создания глобального генератора."""
    counter = 1
    while True:
        yield counter
        counter += 1


def get_ids_for_empty_name(value, id_generator):
    """Предобработка пропусков в ФИО."""
    if value == "":
        return f"anon_{next(id_generator)}"
    else:
        return value


def transform_work_list(work_list):
    """Парсинг информации о работе/должности/зарплате."""
    work_list = work_list.strip("[]")
    parsed_list = [item.strip() for item in work_list.split(",")]
    сompanies_num = parsed_list.count("Компания")
    freelance_num = parsed_list.count("Фриланс")
    total_num = сompanies_num + freelance_num
    works_info = [
        {
            "name": parsed_list[total_num + i],
            "post": parsed_list[total_num * 2 + i],
            "salary_range": parsed_list[total_num * 3 + i]
        } if total_num * 3 + i < len(parsed_list) and parsed_list[total_num * 3 + i] != "" else
        {
            "name": parsed_list[total_num + i],
            "post": parsed_list[total_num * 2 + i],
            "salary_range": None
        }
        for i in range(total_num)
    ]
    return works_info


def get_data_from_file(temp_file) -> pd.DataFrame:
    """Получение данных из файла."""
    unique_id_generator = create_unique_id_generator()
    try:
       data = pd.read_excel(
            temp_file.name,
            converters={
                "ФИО": lambda x: get_ids_for_empty_name(
                    x,
                    unique_id_generator
                ),
            }
        )
    except Exception:
        data = pd.DataFrame()
        print(traceback.format_exc())
    finally:
        temp_file.close()

    data["Где работал"] = data["Где работал"].map(transform_work_list)
    return data


def parse_magistracy(magistracy):
    """Парсинг информации об учебе в магистратуре."""
    magistracy = magistracy.strip("[]")
    magistracy = [item.strip() for item in magistracy.split(",")]
    return magistracy


def flatten_data(data: pd.DataFrame) -> pd.DataFrame:
    """Нормализация данных."""
    rows = []
    for idx, row in data.iterrows():
        for step, job in enumerate(row["Где работал"]):
            rows.append({
                "graduate": idx,
                "step": step,
                "company": job["name"],
                "position": job["post"],
                "salary_range": job["salary_range"],
                "graduation_year": row["Год выпуска"],
                "math_group": row["Матпоток"],
                "magistracy": parse_magistracy(row["Магистратура"])
            })
    data = pd.DataFrame(rows)
    data = data.sort_values(by=["graduate", "step"])

    return data


def get_magistracy(x):
    """Нормализация данных об учебе в магистратуре."""
    if x[1] == "СПбГЭУ" and any([(substring in x[2].lower())
    for substring in ["пм", "прикладная математика", "анализ данных"]]):
        return "Магистратура ПМ СПбГЭУ"
    elif x[0] == "Да":
        return "Другая магистратура"
    else:
        return "Без магистратуры"


def upload_data(url: str, cnx):
    """Загрузка данных из внешних источников электронных таблиц."""
    url_for_download = loads(
            requests.get(
                "https://cloud-api.yandex.net/v1/disk/public/resources/"
                "download?public_key=" + url
            ).content
        )["href"]
    response = requests.get(url_for_download)

    with tempfile.NamedTemporaryFile(
        suffix=".xlsx",
        delete=False
    ) as temp_file:
        temp_file.write(response.content)
    data = get_data_from_file(temp_file)
    data = flatten_data(data)
    data["magistracy"] = data["magistracy"].map(get_magistracy)
    data = get_salary_value(data)
    data = rename_columns(data)
    data.to_sql(name="graduates", con=cnx, index=False, if_exists="replace")
    return data
