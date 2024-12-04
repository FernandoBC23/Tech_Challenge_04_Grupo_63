import streamlit as st

# Configuração da página deve ser a primeira chamada
st.set_page_config(page_title="Análise do Petróleo", layout="wide")

from homepage import render_homepage
from dashboard import render_dashboard
from analise import render_analise
from eventos import render_eventos
from machinelearning import render_machinelearning
from conclusao import render_conclusao
from PIL import Image
import base64
from io import BytesIO


# Função auxiliar para converter imagem em Base64
def sidebar_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="WEBP")
    return base64.b64encode(buffered.getvalue()).decode()

# Carregar imagem do logo
image = Image.open('imagens/Logo_Grupo_63.png')

# Renderizar imagem no sidebar
st.sidebar.markdown(
    f"""
    <div style="display: flex; justify-content: center; margin-bottom: 20px;">
        <img src="data:image/webp;base64,{sidebar_image_to_base64(image)}" alt="Logo" style="width: 200px;"/>
    </div>
    """,
    unsafe_allow_html=True
)

# Dicionário de páginas
pages = {
    "HomePage": render_homepage,
    "Dashboard": render_dashboard,
    "Análise Geral": render_analise,    
    "Eventos Históricos": render_eventos,
    "Machine Learning": render_machinelearning,
    "Conclusão": render_conclusao
    
}

# Filtro de seleção de página
page = st.sidebar.selectbox("Selecione a página", list(pages.keys()))
st.sidebar.markdown("---")  # Separador

# Executa a função associada à página selecionada
if page in pages:
    pages[page]()  # Renderiza a página selecionada
