"""Основной модуль приложения."""

import pandas as pd
import streamlit as st

from agent.page import init_agent_page
from constructor.page import init_constructor_page
from core.config import settings
from dashboard.page import init_dashboard_page
from storage.page import init_storage_page
from utils.etl_utils import get_salary_value, rename_columns

st.set_page_config(layout="wide")


def main(data, **kwargs):
    """Инициализация приложения."""
    data = get_salary_value(data)
    data = rename_columns(data)
    page = st.sidebar.radio(
        "Выберите страницу",
        ["Dashboard", "Конструктор графиков", "ИИ-агент", "Хранилище"],
    )
    if not st.session_state.get("figures", None):
        st.session_state["figures"] = []
    if page == "Dashboard":
        init_dashboard_page()
    elif page == "Конструктор графиков":
        init_constructor_page(data, **kwargs)
    elif page == "ИИ-агент":
        init_agent_page()
    elif page == "Хранилище":
        init_storage_page()


if "__main__" == __name__:
    data = pd.read_sql_table("graduates", con=settings.DATABASE_URL)
    main(data, debug=True)
