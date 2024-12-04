import streamlit as st
from PIL import Image

# CSS para layout responsivo
st.markdown("""
    <style>
    div.block-container {
        padding-top: 0.1rem;
        padding-bottom: 1rem;
        padding-left: 5rem;
        padding-right: 1rem;
    }
    .title-test {
        font-weight: bold;
        font-size: 24px;
        color: #D4AF37;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

def render_homepage():
    # Título centralizado com CSS
    html_title = """
    <style>
    .title-test {
        font-weight: bold;
        font-size: 36px; /* Tamanho do texto */
        color: #FFFFFF;
        text-align: center;            
        margin-bottom: 5px;
    }
    </style>
    <center><h1 class="title-test">Análise do Preço do Petróleo Brent</h1></center>"""   

    st.markdown(html_title, unsafe_allow_html=True)


    # Dividir em duas colunas
    col1, col2 = st.columns([2, 1])  # Ajuste as proporções das colunas conforme necessário

    # Coluna 1: Imagem
    with col1:
        try:
            # Substitua pelo caminho correto da imagem
            image = Image.open("imagens/foto_capa_petroleo.webp")
            st.image(image, caption="Imagem representativa do petróleo Brent", width=400)  # Defina a largura da imagem
        except FileNotFoundError:
            st.error("Imagem não encontrada. Verifique o caminho do arquivo.")

    # Coluna 2: Nomes dos integrantes
    with col2:
        st.markdown("""
        ### Grupo 63 - FIAP
        - **RM355682– Cristina Filippini**
        - **RM355774– Fernando Chagas**
        - **RM355488– Ingrid Miranda**        
        """, unsafe_allow_html=True)

    # Descrição introdutória do projeto
    st.markdown("""
    <div style="text-align: justify; font-size: 1.1rem;">
        Bem-vindo ao projeto Tech Challenge! Este projeto foi desenvolvido para gerar insights baseados em dados sobre a evolução do preço do petróleo Brent ao longo dos anos. Utilizando técnicas de análise de séries temporais e Machine Learning, analisamos o impacto de eventos geopolíticos, crises econômicas e mudanças na oferta e demanda no mercado global.
    </div>
    <hr>
    """, unsafe_allow_html=True)

    # Objetivos
    st.markdown("""
    ### Objetivos

    - **Analisar os dados históricos do preço do petróleo Brent** para identificar padrões e tendências de mercado.
    - **Gerar insights estratégicos** sobre a influência de eventos geopolíticos e econômicos no preço do petróleo.
    - **Desenvolver um modelo preditivo** com Machine Learning para realizar forecasting de preços futuros.
    - **Disponibilizar um dashboard interativo** que facilite o acesso a informações importantes e indicadores-chave.

    <hr>
    """, unsafe_allow_html=True)

    # Navegação
    st.markdown("""
    ### Navegação

    Explore as diferentes seções do projeto:

    - **Dashboard de Indicadores**: Descubra métricas como preço máximo, mínimo, média e volatilidade anual e mensal. Visualize gráficos interativos de preços históricos e comparações de demanda e produção.
    - **Análise Histórica**: Examine os impactos de crises econômicas, conflitos geopolíticos e mudanças de mercado nos preços do petróleo.
    - **Eventos Históricos**: Explore uma análise detalhada de eventos críticos que influenciaram o mercado, como a Guerra do Golfo, crise financeira Global, a Primavera Árabe, a Pandemia de 2020 e Guerra entre Rússia e Ucrânia.
    - **Previsão de Preços (Machine Learning)**: Consulte previsões de preços diários geradas por nosso modelo de Machine Learning, junto com insights econômicos e análise de desempenho.
    - **Conclusão**: Confira um resumo do projeto e os principais aprendizados.

    <hr>
    """, unsafe_allow_html=True)

    # Contexto do Projeto
    st.markdown("""
    ### Contexto do Projeto

    O petróleo Brent, uma referência global para o mercado de energia, é um ativo estratégico e altamente influenciado por eventos econômicos e geopolíticos. Este projeto utiliza dados históricos extraídos do **[site do IPEA](http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view)** para analisar as oscilações de preços e como eventos externos moldaram a dinâmica do mercado ao longo do tempo.

    <hr>
    """)

    # Ferramentas Utilizadas
    st.markdown("""
    ### Ferramentas Utilizadas

    Este projeto integra diversas ferramentas e tecnologias para garantir uma análise robusta e visualização interativa:

    - **Análise de Dados**: Python, Pandas, NumPy.
    - **Visualização**: Streamlit, Plotly.
    - **Machine Learning**: Prophet para séries temporais.
    - **Deploy**: Streamlit Cloud.

    <hr>

    _Agradecemos por explorar nosso projeto!_
    """, unsafe_allow_html=True)