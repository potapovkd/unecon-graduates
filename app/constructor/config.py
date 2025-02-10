"""Настройки модуля конструктора."""

from enum import Enum


class ChartForConstruction(Enum):
    """Доступные для конструирования типы графиков."""

    SUNBURST = "Sunburst"
    BARPLOT = "Barplot"

    @classmethod
    def get_charts_for_construction(cls):
        """Получить названия всех доступных типов графиков."""
        return [p.value for p in cls]
