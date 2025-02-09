"""Сервисы для графиков lineplot, barplot."""

import plotly.express as px
import streamlit as st


def set_other_params(data, chart_type):
    """Ф-ция для установки параметров графика."""
    x_axis = st.selectbox("Выберите ось X", options=data.columns, key="x_axis")
    y_axis = st.selectbox("Выберите ось Y", options=data.columns, key="y_axis")
    aggregation_fn = st.selectbox(
        "Выберите агрегирующую функцию",
        ["mean", "sum", "min", "max", "count", "nunique"],
        key="agg_fn",
    )
    color = st.selectbox(
        "Выберите цветовую группировку",
        options=["None"] + list(data.columns),
        key="color_group",
    )
    st.session_state.chart_params = {
        "type": chart_type,
        "x": x_axis,
        "y": y_axis,
        "agg": aggregation_fn,
        "color": None if color == "None" else color,
    }


def plot_line(data, params, **kwargs):
    """Ф-ция для получения графика lineplot."""
    return px.line(
        data,
        x=params["x"],
        y=params["y"],
        color=params["color"] if params["color"] else None,
        **kwargs,
    )


def plot_bar(data, params, **kwargs):
    """Ф-ция для получения графика barplot."""
    print(data)
    return px.bar(
        data,
        x=params["x"],
        y="agg_data",
        color=params["color"] if params["color"] else None,
        **kwargs,
    )
