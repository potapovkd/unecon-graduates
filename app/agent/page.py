"""Страница ИИ-агента."""

import plotly.graph_objects as go
from smolagents import CodeAgent, HfApiModel
import streamlit as st

from core.config import settings, get_color_discrete_sequence
from utils.etl_utils import clean_salary
from .services.tools_for_agents import sql_engine


general_prompt = (
    "Отвечай на русском языке. "
    "Если просят сгенерировать график, подписи должны быть на русском языке. "
    "Если просят сгенерировать график верни объект plotly go Figure, иначе - "
    "текстовый ответ. Учитывай последнее (текущее) место работы - "
    "максимальный step для каждого graduate, если в запросе не указано иное. "
    "Запрос пользователя: "
)



def init_agent_page():
    """Инициализация страницы ИИ-агента."""

    model_choice = st.radio(
        "Выберите модель",
        ["Qwen2.5 Coder 7B", "Qwen2.5 Coder 32B"]
    )
    if model_choice == "Qwen2.5 Coder 1.5B":
        model = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
    else:
        model = "Qwen/Qwen2.5-Coder-32B-Instruct"
    agent = CodeAgent(
        tools=[sql_engine, clean_salary, get_color_discrete_sequence],
        model=HfApiModel(model=model, token=settings.TOKEN),
        additional_authorized_imports=["pandas", "plotly", "io"],
    )

    user_input = st.text_area("Введите запрос", value="", height=150)

    if st.button("Спросить"):
        if user_input.strip():
            st.subheader("Ответ:")
            result = agent.run(
                general_prompt + user_input,
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
