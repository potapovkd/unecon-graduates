"""Основной модуль приложения."""
import os

import pandas as pd
import streamlit as st

from agent.page import init_agent_page
from constructor.page import init_constructor_page
from core.config import settings
from dashboard.page import init_dashboard_page
from start.page import init_start_page
from storage.page import init_storage_page


st.set_page_config(layout="wide")

def main(**kwargs):
    """Инициализация приложения."""
    page = st.sidebar.radio(
        "Выберите страницу",
        [
            "Загрузка данных",
            "Dashboard",
            "Конструктор графиков",
            "ИИ-агент",
            "Хранилище"
        ],
    )
    if not st.session_state.get("figures", None):
        st.session_state["figures"] = []
    if os.path.exists(settings.DATABASE_URL):
        data = pd.read_sql_table("graduates", con=f"sqlite:///{settings.DATABASE_URL}")
        if page == "Загрузка данных":
            init_start_page()
        if page == "Dashboard":
            init_dashboard_page()
        elif page == "Конструктор графиков":
            init_constructor_page(data, **kwargs)
        elif page == "ИИ-агент":
            init_agent_page()
        elif page == "Хранилище":
            init_storage_page()


if "__main__" == __name__:
    main(debug=True)
