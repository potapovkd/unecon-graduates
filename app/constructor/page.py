"""Страница конструктора графиков."""

import traceback

import streamlit as st

from core.config import get_color_discrete_sequence
from .config import ChartForConstruction
from .services.filters_services import cache_filters
from .services.barplot_services import set_barplot_params, plot_bar
from .services.sunburst_services import plot_sunburst, set_sunburst_params


CHART_FUNCTION_MAPPER = {
    ChartForConstruction.SUNBURST.value: {
        "function_for_set_params": set_sunburst_params,
        "function_for_plot": plot_sunburst,
    },
    ChartForConstruction.BARPLOT.value: {
        "function_for_set_params": set_barplot_params,
        "function_for_plot": plot_bar,
    },
}


def init_constructor_page(data, debug=False):
    """Инициализация страницы конструктора."""
    chart_type = st.selectbox(
        "Выберите тип графика",
        ChartForConstruction.get_charts_for_construction(),
    )
    fig_title = st.text_input("Введите название графика")
    with st.sidebar:
        st.session_state.filtered_data = cache_filters(data)

    st.session_state.chart_params = CHART_FUNCTION_MAPPER[chart_type][
        "function_for_set_params"
    ](data)

    if st.session_state.filtered_data.empty:
        st.warning(
            "Нет данных для построения графика. "
            "Пожалуйста, настройте данные в Конструкторе."
        )
    else:
        params = st.session_state.chart_params
        data = st.session_state.filtered_data

        try:
            fig = CHART_FUNCTION_MAPPER[chart_type]["function_for_plot"](
                data,
                params,
                **{
                    "title": fig_title,
                    "color_discrete_sequence": get_color_discrete_sequence(),
                },
            )
            st.plotly_chart(fig)

            if st.button("Сохранить в хранилище", key="Сохранить в хранилище"):
                st.session_state.figures.append({"figure": fig, "flag": False})
                st.write("График успешно сохранен в хранилище!")
            elif st.button(
                "Добавить на дашборд",
                key="Добавить на дашборд",
            ):
                st.session_state.figures.append({"figure": fig, "flag": True})
                st.write("График успешно добавлен на дашборд!")

        except Exception:
            if debug:
                debug_string = f" {traceback.format_exc()}"
            else:
                debug_string = ""
            st.warning(
                f"Невозможно построить {chart_type} график для выбранных "
                f"параметров.{debug_string}"
            )
