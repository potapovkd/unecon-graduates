"""Страница дашборда."""

import streamlit as st

from .services.report_services import create_html, create_pdf


def init_dashboard_page():
    """Инициализация страницы дашборда."""
    figures_for_dashboard = [
        figures["figure"]
        for figures in st.session_state.figures
        if figures["flag"]
    ]
    if len(figures_for_dashboard) > 0:
        if st.button("Выгрузить статичный отчет в PDF"):
            pdf_path = create_pdf(figures_for_dashboard)
            st.success("PDF отчет успешно создан!")

            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="Скачать отчет",
                    data=pdf_file,
                    file_name="report.pdf",
                    mime="application/pdf",
                )
        if st.button("Выгрузить интерактивный отчет в HTML"):
            html_path = create_html(figures_for_dashboard)
            st.success("HTML отчет успешно создан!")

            with open(html_path, "rb") as html_file:
                st.download_button(
                    label="Скачать отчет",
                    data=html_file,
                    file_name="report.html",
                    mime="text/html",
                )

    for figure in st.session_state.figures:
        if figure["flag"]:
            st.plotly_chart(figure["figure"])
            if st.button(
                "Удалить с дашборда", key=f"Удалить с дашборда {figure}"
            ):
                figure["flag"] = False
                st.rerun()
