"""Страница хранилища."""

import streamlit as st


def init_storage_page():
    """Инициализация страницы хранилища."""
    figures = st.session_state.figures
    for fig_num, figure in enumerate(figures):
        st.plotly_chart(figure["figure"])
        if st.button(
            "Удалить из хранилища", key=f"Удалить из хранилища {fig_num}"
        ):
            figures.pop(fig_num)
            st.rerun()
        if not figure["flag"]:
            if st.button(
                "Добавить на дашборд", key=f"Добавить на дашборд {fig_num}"
            ):
                figure["flag"] = True
                st.rerun()
