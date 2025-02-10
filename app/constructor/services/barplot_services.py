"""Сервисы для графиков lineplot, barplot."""

import plotly.express as px
import streamlit as st


def set_barplot_params(data):
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
    return {
        "x": x_axis,
        "y": y_axis,
        "agg": aggregation_fn,
        "color": None if color == "None" else color,
    }


def plot_bar(data, params, **kwargs):
    """Ф-ция для получения графика barplot."""
    data = data[:]
    columns_for_groupby = (
        [params["x"], params["color"]] if params["color"] else params["x"]
    )
    data = data.groupby(columns_for_groupby).agg(
        agg_data=(params["y"], params["agg"])
    ).reset_index()
    fig = px.bar(
        data,
        x=params["x"],
        y="agg_data",
        color=params["color"] if params["color"] else None,
        **kwargs,
    )
    fig.update_layout(
        yaxis_title=params["y"],
    )
    return fig
