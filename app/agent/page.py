"""Страница ИИ-агента."""

import plotly.graph_objects as go
from smolagents import CodeAgent, HfApiModel
import streamlit as st

from core.config import settings
from utils.etl_utils import clean_salary
from .services.tools_for_agents import sql_engine


agent = CodeAgent(
    tools=[sql_engine, clean_salary],
    model=HfApiModel(settings.MODEL, token=settings.TOKEN),
    additional_authorized_imports=["pandas", "plotly", "io"],
)


def init_agent_page():
    """Инициализация страницы ИИ-агента."""
    user_input = st.text_area("Введите запрос", value="", height=150)

    if st.button("Спросить"):
        if user_input.strip():
            st.subheader("Ответ:")
            result = agent.run(
                user_input,
            )
            if isinstance(result, go.Figure):
                st.session_state["last_ai_figure"] = result
            else:
                st.write(result)
        else:
            st.warning("Пожалуйста, введите запрос.")

    if st.session_state.get("last_ai_figure", None):
        st.plotly_chart(
            st.session_state["last_ai_figure"], use_container_width=True
        )

        if st.button("Сохранить в хранилище", key="Сохранить в хранилище"):
            st.session_state.figures.append(
                {
                    "figure": st.session_state["last_ai_figure"],
                    "flag": True,
                }
            )
        elif st.button("Добавить на дашборд", key="Добавить на дашборд"):
            st.session_state.figures.append(
                {
                    "figure": st.session_state["last_ai_figure"],
                    "flag": True,
                }
            )
