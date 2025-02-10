"""Инструменты ИИ-агента."""

from smolagents import tool
from sqlalchemy import (
    create_engine,
    text,
)

from core.config import settings

engine = create_engine(f"sqlite:///{settings.DATABASE_URL}")


@tool
def sql_engine(query: str) -> str:
    """
    Allows you to perform SQL queries on the table.
    Returns a string representation of the result.
    The table is named 'graduates'. Its description is as follows:
        Columns:
            index :  INTEGER
            graduate :  INTEGER
            step :  INTEGER is the job number of a particular graduate
            company :  TEXT is jobs
            position :  TEXT is post
            salary_range :  TEXT in interval for salary, use tool for parse
            graduation_year :  INTEGER
            math_group :  TEXT
            magistracy: TEXT unique value:
                [
                    "Магистратура ПМ СПбГЭУ",
                    "Другая магистратура",
                    "Без магистратуры"
                ]

    Args:
        query: The query to perform. This should be correct SQL.
    """
    output = ""
    with engine.connect() as con:
        rows = con.execute(text(query))
        for row in rows:
            output += "\n" + str(row)
    return output
