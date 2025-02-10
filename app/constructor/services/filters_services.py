"""Сервисы для фильтров в конструкторе графиков."""

import streamlit as st


def cache_filters(data):
    """Установка фильтров и сохранение их состояния."""
    grad_year_range = st.slider(
        "Год выпуска:",
        min_value=int(data["Год выпуска"].min()),
        max_value=int(data["Год выпуска"].max()),
        value=(
            int(data["Год выпуска"].min()),
            int(data["Год выпуска"].max()),
        ),
    )

    step_filter = st.radio(
        "Этап карьеры",
        options=[
            "Без фильтрации",
            "Первое место работы",
            "Текущее место работы",
        ],
    )

    salary_filter = st.multiselect(
        "Интервал зарплат:",
        options=data["Диапазон зарплаты"].unique(),
        default=data["Диапазон зарплаты"].unique(),
    )

    magistracy_filter = st.multiselect(
        "Магистратура:",
        options=data["Магистратура"].unique(),
        default=data["Магистратура"].unique(),
    )

    filtered_df = data[
        (data["Год выпуска"] >= grad_year_range[0])
        & (data["Год выпуска"] <= grad_year_range[1])
        & (data["Диапазон зарплаты"].isin(salary_filter))
        & (data["Магистратура"].isin(magistracy_filter))
    ]

    if step_filter == "Первое место работы":
        filtered_df = data.loc[
            data.groupby("Выпускник")["Номер места работы"].idxmin()
        ]
    elif step_filter == "Текущее место работы":
        filtered_df = data.loc[
            data.groupby("Выпускник")["Номер места работы"].idxmax()
        ]

    return filtered_df  # noqa: R504
