"""Глобальные настройки приложения."""

import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv(".env")

hf_token = os.getenv("HF_TOKEN")
model_name = os.getenv("MODEL_NAME")
db_path = os.getenv("DB_PATH")


class Settings(BaseSettings):
    """Настройки проекта."""

    # DATABASE_URL: str = (
    #     f"sqlite:///{db_path}"
    # )
    DATABASE_URL: str = "sqlite:///graduates.db"
    MODEL: str = "Qwen/Qwen2.5-Coder-32B-Instruct"
    TOKEN: str = "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"


settings = Settings(
    DATABASE_URL=f"sqlite:///{db_path}",
    TOKEN=hf_token,
    MODEL=model_name,
)


def get_color_discrete_sequence():
    """Для построения графиков plotly для цветного экспорта."""
    return [
        "#0068c9",
        "#83c9ff",
        "#ff2b2b",
        "#ffabab",
        "#29b09d",
        "#7defa1",
        "#ff8700",
        "#ffd16a",
        "#6d3fc0",
        "#d5dae5",
    ]
