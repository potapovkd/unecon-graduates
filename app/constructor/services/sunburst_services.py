"""Сервисы для иерархических графиков."""

import plotly.express as px
import streamlit as st


def set_sunburst_params(data):
    """Ф-ция для установки параметров графика."""
    num_levels = st.slider(
        "Количество уровней",
        min_value=1,
        max_value=len(data.columns),
        value=3,
    )
    selected_levels = []
    for i in range(num_levels):
        level = st.selectbox(
            f"Уровень {i + 1}", options=data.columns, key=f"level_{i}"
        )
        selected_levels.append(level)
    value = st.selectbox("Значение", options=data.columns, key="value")
    return {
        "type": "Sunburst",
        "levels": selected_levels,
        "value": value,
    }


def plot_sunburst(data, params, **kwargs):
    """Ф-ция для получения графика sunburst."""
    return px.sunburst(
        data,
        path=params["levels"],
        values=params["value"],
        color=params["levels"][0],
        height=800,
        **kwargs,
    )
