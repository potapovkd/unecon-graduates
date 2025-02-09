"""Сервисы для стратовых графиков."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_career_sunburst_plot(data):
    """График Магистратура - выпускник - компания."""
    data = data[:]

    magistracy_graduates_counts = data.groupby(
        "magistracy", as_index=False
    ).agg(magistracy_graduates_counts=("graduate", "nunique"))
    graduate_median_salary = data.groupby("graduate", as_index=False).agg(
        median_salary_person=("salary", "median")
    )
    data = data.merge(
        graduate_median_salary,
        on="graduate",
    )
    data = data.merge(
        magistracy_graduates_counts,
        on="magistracy",
    )
    return px.sunburst(
        data,
        path=["magistracy", "graduate", "company"],
        values="salary",
        color="magistracy",
        title="Распределение мест работы и зарплат по магистратурам",
        custom_data=["salary", "step", "magistracy_graduates_counts"],
        height=700,
    )


def get_count_graduates_by_magistracy_barplot(data):
    """График Магистратура - количество выпускников с группировкой по годам."""
    data = data[:]
    data = data[data["step"] == 0]
    data_magistracy = data[(data["magistracy"] == "Другая магистратура")]
    data_unecon = data[data["magistracy"] == "Магистратура ПМ СПбГЭУ"]
    data_other = data[data["magistracy"] == "Без магистратуры"]

    grouped_data_magistracy = (
        data_magistracy.groupby("graduation_year")
        .agg(
            Магистратура=("magistracy", "count"),
            Медиана_первая_зарплата=("first_salary", "median"),
            Медиана_текущая_зарплата=("last_salary", "median"),
        )
        .reset_index()
    )

    grouped_data_unecon = (
        data_unecon.groupby("graduation_year")
        .agg(
            СПбГЭУ_ПМ=("magistracy", "count"),
            Медиана_первая_зарплата=("first_salary", "median"),
            Медиана_текущая_зарплата=("last_salary", "median"),
        )
        .reset_index()
    )

    grouped_data_other = (
        data_other.groupby("graduation_year")
        .agg(
            Другие=("magistracy", "count"),
            Медиана_первая_зарплата=("first_salary", "median"),
            Медиана_текущая_зарплата=("last_salary", "median"),
        )
        .reset_index()
    )

    grouped_data = pd.merge(
        grouped_data_magistracy,
        grouped_data_unecon,
        on="graduation_year",
        how="outer",
    ).fillna(0)

    grouped_data = pd.merge(
        grouped_data, grouped_data_other, on="graduation_year", how="outer"
    ).fillna(0)

    colors = {
        "Магистратура": "#4F86F7",  # Темно-синий цвет
        "Магистратура СПбГЭУ ПМ": "#00BFAE",  # Бирюзовый цвет
        "Другие": "orange",
    }

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name="Магистратура СПбГЭУ ПМ",
            x=grouped_data["graduation_year"],
            y=grouped_data["СПбГЭУ_ПМ"],
            hovertemplate=(
                "Студентов: %{y}<br>"
                + "Первая зарплата: %{customdata[0]}<br>"
                + "Текущая зарплата: %{customdata[1]}"
            ),
            customdata=grouped_data[
                ["Медиана_первая_зарплата_y", "Медиана_текущая_зарплата_y"]
            ].values,
            marker_color=colors["Магистратура СПбГЭУ ПМ"],
            offsetgroup=0,
        )
    )

    fig.add_trace(
        go.Bar(
            name="Магистратура",
            x=grouped_data["graduation_year"],
            y=grouped_data["Магистратура"],
            hovertemplate=(
                "Студентов: %{customdata[0]}<br>"
                + "Первая зарплата: %{customdata[1]}<br>"
                + "Текущая зарплата: %{customdata[2]}"
            ),
            customdata=grouped_data[
                [
                    "Магистратура",
                    "Медиана_первая_зарплата_x",
                    "Медиана_текущая_зарплата_x",
                ]
            ].values,
            marker_color=colors["Магистратура"],
            offsetgroup=0,
            base=grouped_data["СПбГЭУ_ПМ"],
        )
    )

    fig.add_trace(
        go.Bar(
            name="Другие",
            x=grouped_data["graduation_year"],
            y=grouped_data["Другие"],
            hovertemplate=(
                "Студентов: %{y}<br>"
                + "Первая зарплата: %{customdata[0]}<br>"
                + "Текущая зарплата: %{customdata[1]}"
            ),
            customdata=grouped_data[
                ["Медиана_первая_зарплата", "Медиана_текущая_зарплата"]
            ].values,
            marker_color=colors["Другие"],
            offsetgroup=1,
        )
    )

    fig.add_annotation(
        text="Во всплывающих окнах указана медианная зарплата "
        "по группе выпускников",
        xref="paper",
        yref="paper",
        x=0.5,
        y=-0.25,
        showarrow=False,
        font=dict(size=12),
    )

    fig.update_layout(
        barmode="group",
        title="Сравнение выпускников по годам",
        xaxis_title="Год выпуска",
        yaxis_title="Количество",
        xaxis=dict(tickmode="linear", dtick=1),
    )
    return fig
