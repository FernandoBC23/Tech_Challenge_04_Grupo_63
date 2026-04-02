import base64
from io import BytesIO

import streamlit as st
from PIL import Image

from app.pages.analise import render_analise
from app.pages.conclusao import render_conclusao
from app.pages.dashboard import render_dashboard
from app.pages.eventos import render_eventos
from app.pages.homepage import render_homepage
from app.pages.machinelearning import render_machinelearning
from app.services.data_loader import LOGO_PATH


def sidebar_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="WEBP")
    return base64.b64encode(buffered.getvalue()).decode()


def run():
    st.set_page_config(page_title="Análise do Petróleo", layout="wide")

    image = Image.open(LOGO_PATH)

    st.sidebar.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin-bottom: 20px;">
            <img src="data:image/webp;base64,{sidebar_image_to_base64(image)}" alt="Logo" style="width: 200px;"/>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pages = {
        "Visão Geral": render_homepage,
        "Dashboard": render_dashboard,
        "Análise Geral": render_analise,
        "Eventos Históricos": render_eventos,
        "Machine Learning": render_machinelearning,
        "Conclusão": render_conclusao,
    }

    page = st.sidebar.selectbox("Selecione a página", list(pages.keys()))
    st.sidebar.markdown("---")

    if page in pages:
        pages[page]()


if __name__ == "__main__":
    run()
