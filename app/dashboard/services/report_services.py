"""Модуля для формирования отчетов на основе собранного дашборда."""

import os
from tempfile import NamedTemporaryFile

from fpdf import FPDF
from plotly.io import to_html


def create_pdf(figures):
    """Ф-ция для получения временного pdf файла со статичным отчетом."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for i, fig in enumerate(figures):
        temp_file = NamedTemporaryFile(delete=False, suffix=".jpg")
        fig.write_image(temp_file.name, format="jpg")
        fig.write_image(f"img{i}.png", format="png")
        pdf.add_page()
        pdf.image(temp_file.name, x=10, y=30, w=pdf.w - 20)

        os.unlink(temp_file.name)

    temp_pdf = NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_pdf.name)

    return temp_pdf.name


def create_html(figures):
    """Ф-ция для получения временного html файла с интерактивным отчетом."""
    html_content = ""
    for i, fig in enumerate(figures):
        html_content += to_html(fig, full_html=False, include_plotlyjs=False)

    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    temp_html = NamedTemporaryFile(delete=False, suffix=".html")

    with open(temp_html.name, "w") as f:
        f.write(full_html)

    return temp_html.name
