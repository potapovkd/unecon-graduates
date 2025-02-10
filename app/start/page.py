import sqlite3

import streamlit as st

from core.config import settings
from utils.etl_utils import upload_data


def init_start_page():
    cnx = sqlite3.connect(settings.DATABASE_URL)
    st.subheader("Введите ссылку на файл")
    file_url = st.text_input(
        "Ссылка на файл (Яндекс.Диск):",
        key="file_url_input")
    if st.button("Загрузить файл"):
        if not file_url.strip():
            st.warning("Пожалуйста, введите ссылку на файл!")
        else:
            st.info("Загружаем файл...")
            data = upload_data(file_url, cnx)
            if data is not None:
                st.success("Файл успешно загружен и обработан!")
                st.dataframe(data.head())
