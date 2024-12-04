import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_loader import carregar_dados

# CSS para layout responsivo
st.markdown("""
    <style>
    div.block-container {
        padding-top: 1rem;
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

# Função para normalizar séries de dados
def normalizar_serie(serie):
    try:
        return (serie - serie.min()) / (serie.max() - serie.min())
    except ZeroDivisionError:
        return serie

# Função principal do dashboard
@st.cache_data
def carregar_dados_otimizado():
    return carregar_dados()

def render_analise():
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
    <center><h1 class="title-test">Análise Histórica do Petróleo Brent</h1></center>"""

    st.markdown(html_title, unsafe_allow_html=True)

    # Introdução
    st.write("""
    <div style="text-align: justify; font-size: 1.1rem;">
        A análise histórica do petróleo Brent apresenta uma visão detalhada das variações de preço ao longo dos anos. 
        Este estudo abrange impactos de eventos geopolíticos, crises econômicas e mudanças estruturais no mercado global de energia.
    </div>
    """, unsafe_allow_html=True)

    # Carregar os dados
    base_preco, base_demanda, base_producao = carregar_dados()

    # Garantir que a coluna 'Data' esteja no formato datetime
    base_preco['Data'] = pd.to_datetime(base_preco['Data'], errors='coerce')

    # Sidebar
    st.sidebar.header("Filtros")
    anos_unicos = sorted(base_preco['Data'].dt.year.dropna().unique())
    anos_selecionados = st.sidebar.select_slider(
        "Selecione o Período de Anos",
        options=anos_unicos,
        value=(anos_unicos[0], anos_unicos[-1])
    )

    # Filtrar dados com base nos anos selecionados
    base_preco['Ano'] = base_preco['Data'].dt.year
    base_preco_filtrada = base_preco[(base_preco['Ano'] >= anos_selecionados[0]) & (base_preco['Ano'] <= anos_selecionados[1])]

    # Gráfico: Demanda, Produção e Preço Normalizados
    st.markdown("### **Demanda, Produção e Preço (Normalizados)**")
    base_demanda['Ano'] = pd.to_datetime(base_demanda['Ano'], format='%Y', errors='coerce').dt.year
    base_producao['Ano'] = pd.to_datetime(base_producao['Ano'], format='%Y', errors='coerce').dt.year

    base_demanda_filtrada = base_demanda[(base_demanda['Ano'] >= anos_selecionados[0]) & (base_demanda['Ano'] <= anos_selecionados[1])]
    base_producao_filtrada = base_producao[(base_producao['Ano'] >= anos_selecionados[0]) & (base_producao['Ano'] <= anos_selecionados[1])]

    base_preco_filtrada['Preço_Normalizado'] = normalizar_serie(base_preco_filtrada['Preço'])
    base_demanda_filtrada['Demanda_Normalizada'] = normalizar_serie(base_demanda_filtrada['Total world'])
    base_producao_filtrada['Producao_Normalizada'] = normalizar_serie(base_producao_filtrada['Total World'])

    fig_comparativo = go.Figure()
    fig_comparativo.add_trace(go.Scatter(x=base_preco_filtrada['Data'], y=base_preco_filtrada['Preço_Normalizado'], mode='lines', name='Preço'))
    fig_comparativo.add_trace(go.Scatter(x=base_demanda_filtrada['Ano'], y=base_demanda_filtrada['Demanda_Normalizada'], mode='lines', name='Demanda'))
    fig_comparativo.add_trace(go.Scatter(x=base_producao_filtrada['Ano'], y=base_producao_filtrada['Producao_Normalizada'], mode='lines', name='Produção'))
    fig_comparativo.update_layout(
        title="Preço, Demanda e Produção de Petróleo (Normalizados)",
        xaxis_title="Ano",
        yaxis_title="Valor Normalizado",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_comparativo, use_container_width=True)

    st.write("""
    Este gráfico compara o comportamento do preço do petróleo Brent, a demanda global e a produção mundial ao longo dos anos. 
    Os valores foram normalizados para facilitar a comparação. Picos e quedas refletem eventos como crises econômicas, guerras e mudanças estruturais no mercado de energia.
    """)

    st.markdown("---")

    # Gráfico: Variação do Preço
    st.markdown("### **Variação do Preço do Petróleo**")
    fig_preco = px.line(base_preco_filtrada, x="Data", y="Preço", title="Variação do Preço do Petróleo Brent")
    fig_preco.update_layout(xaxis_title="Data", yaxis_title="Preço (USD)")
    st.plotly_chart(fig_preco, use_container_width=True)

    st.write("""
    O gráfico mostra a evolução histórica do preço do petróleo Brent em dólares. É possível observar como eventos geopolíticos 
    e econômicos, como a Guerra do Golfo e a Pandemia de COVID-19, influenciaram as flutuações de preço.
    """)

    st.markdown("---")

    # Gráfico: Volatilidade Anual
    st.markdown("### **Volatilidade Anual dos Preços**")
    volatilidade_anual = base_preco_filtrada.groupby('Ano')['Preço'].std().reset_index()
    volatilidade_anual.columns = ['Ano', 'Volatilidade']
    media_volatilidade = volatilidade_anual['Volatilidade'].mean()

    fig_volatilidade = px.bar(
        volatilidade_anual,
        x='Ano',
        y='Volatilidade',
        title="Volatilidade Anual dos Preços do Petróleo",
        text='Volatilidade'
    )
    fig_volatilidade.add_hline(
        y=media_volatilidade,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Média: {media_volatilidade:.2f}",
        annotation_position="top left"
    )
    fig_volatilidade.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    st.plotly_chart(fig_volatilidade, use_container_width=True)

    st.write("""
    A volatilidade anual mede as oscilações nos preços do petróleo ao longo do tempo. 
    Anos com maior volatilidade, como 2008 e 2020, coincidem com eventos globais significativos, como a crise financeira e a pandemia.
    """)

    st.markdown("---")

    # Eventos Históricos e Insights
    st.markdown("### **Eventos Históricos e Impactos**")
    st.write("""
    - **1990 - Guerra do Golfo**: A instabilidade geopolítica levou a picos de preço e aumento na volatilidade.
    - **2008 - Crise Financeira Global**: Alta inicial seguida de colapso nos preços devido à recessão.
    - **2014-2016 - Guerra de Preços**: O confronto entre a OPEP e o shale oil nos EUA resultou em quedas prolongadas.
    - **2020 - Pandemia de COVID-19**: A maior desaceleração de demanda registrada, com impactos profundos no mercado.
    - **2022 - Guerra Rússia-Ucrânia**: Conflito geopolítico aumentou a incerteza e os preços devido ao impacto na oferta global.
    """)
