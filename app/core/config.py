"""Глобальные настройки приложения."""

import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from smolagents import tool


load_dotenv(".env")

hf_token = os.getenv("HF_TOKEN")
model_name = os.getenv("MODEL_NAME")
db_path = os.getenv("DB_PATH")


class Settings(BaseSettings):
    """Настройки проекта."""

    # DATABASE_URL: str = (
    #     f"sqlite:///{db_path}"
    # )
    DATABASE_URL: str = "graduates.db"
    MODEL: str = "Qwen/Qwen2.5-Coder-32B-Instruct"
    TOKEN: str = "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"


settings = Settings(
    # DATABASE_URL=db_path,
    # TOKEN=hf_token,
    # MODEL=model_name,
)


@tool
def get_color_discrete_sequence() -> list:
    """
    A tool for transferring palettes to the plotli graph constructor.
    Make sure to pass the color_discrete_sequence argument.
    """
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
