import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from data_loader import carregar_dados

# CSS para ajustes visuais
st.markdown("""
    <style>
    div.block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    .indicator {
        font-size: 16px;
        font-weight: bold;
        color: #D4AF37;
        text-align: center;
        margin-bottom: 10px;
    }
    .indicator-value {
        font-size: 22px;
        color: white;
        text-align: center;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)


# Função para criar indicadores com design melhorado
def criar_indicadores(indicadores, coluna):
    with coluna:
        for texto, valor in indicadores:
            st.markdown(
                f"""
                <div style="
                    background-color: #2C2F33;
                    border-radius: 10px;
                    padding: 10px;
                    margin-bottom: 10px;
                    text-align: center;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                ">
                    <div style="font-size: 14px; font-weight: bold; color: #FFD700;">{texto}</div>
                    <div style="font-size: 20px; font-weight: bold; color: #FFFFFF;">{valor}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# Função principal do dashboard
@st.cache_data
def carregar_dados_otimizado():
    return carregar_dados()

def render_dashboard():
    # Carregar os dados
    base_preco, base_demanda, base_producao = carregar_dados_otimizado()
    base_preco['Data'] = pd.to_datetime(base_preco['Data'], errors='coerce')
    base_preco = base_preco.dropna(subset=['Data']).sort_values(by='Data', ascending=True)

    # Renomear colunas
    base_preco = base_preco.rename(columns={'Data': 'ds', 'Preço': 'y'})

    # Filtros
    st.sidebar.header("Filtros")
    anos_unicos = sorted(base_preco['ds'].dt.year.dropna().unique())
    anos_selecionados = st.sidebar.select_slider(
        "Selecione o Período de Anos",
        options=anos_unicos,
        value=(anos_unicos[0], anos_unicos[-1])
    )

    # Filtrar os dados
    base_preco['Ano'] = base_preco['ds'].dt.year
    base_preco_filtrada = base_preco[(base_preco['Ano'] >= anos_selecionados[0]) & (base_preco['Ano'] <= anos_selecionados[1])]

    # Calcular indicadores
    retorno_acumulado = ((base_preco_filtrada["y"].iloc[-1] / base_preco_filtrada["y"].iloc[0]) - 1) * 100
    base_preco_filtrada['Mes'] = base_preco_filtrada['ds'].dt.to_period('M').astype(str)
    var_mensal = base_preco_filtrada.groupby('Mes')['y'].mean().pct_change().mean() * 100
    var_anual = base_preco_filtrada.groupby('Ano')['y'].mean().pct_change().mean() * 100
    volatilidade_mensal = base_preco_filtrada.set_index('ds')['y'].resample('M').std().mean()
    volatilidade_anual = base_preco_filtrada.set_index('ds')['y'].resample('Y').std().mean()

    indicadores_esquerda = [
        ("Preço Máximo", f"${base_preco_filtrada['y'].max():.2f}"),
        ("Preço Mínimo", f"${base_preco_filtrada['y'].min():.2f}"),
        ("Preço Médio", f"${base_preco_filtrada['y'].mean():.2f}"),
        ("Retorno Acumulado", f"{retorno_acumulado:.2f}%")
    ]

    indicadores_direita = [
        ("Variação Mensal Média", f"{var_mensal:.2f}%"),
        ("Variação Anual Média", f"{var_anual:.2f}%"),
        ("Volatilidade Mensal Média", f"{volatilidade_mensal:.2f}%"),
        ("Volatilidade Anual Média", f"{volatilidade_anual:.2f}%")
    ]

    # Layout com 4 colunas
    col1, col2, col3, col4 = st.columns([1, 3, 3, 1])

    # Indicadores na coluna da esquerda
    criar_indicadores(indicadores_esquerda, col1)

    # Gráficos centrais
    with col2:
        fig_preco = px.line(base_preco_filtrada.reset_index(), x="ds", y="y", title="Variação do Preço do Petróleo", height=400)
        fig_preco.update_layout(xaxis_title="Data", yaxis_title="Preço (USD)")
        st.plotly_chart(fig_preco, use_container_width=True)

    with col3:
        volatilidade_anual = base_preco_filtrada.groupby('Ano')['y'].std().reset_index()
        volatilidade_anual.columns = ['Ano', 'Volatilidade']
        media_volatilidade = volatilidade_anual['Volatilidade'].mean()
        fig_volatilidade = px.bar(volatilidade_anual, x='Ano', y='Volatilidade', title="Volatilidade Anual dos Preços", height=400)
        fig_volatilidade.add_hline(y=media_volatilidade, line_dash="dash", line_color="red", annotation_text=f"Média: {media_volatilidade:.2f}")
        st.plotly_chart(fig_volatilidade, use_container_width=True)

    # Indicadores na coluna da direita
    criar_indicadores(indicadores_direita, col4)

    # Gráfico comparativo na parte inferior
    base_demanda['Ano'] = pd.to_datetime(base_demanda['Ano'], format='%Y', errors='coerce').dt.year
    base_producao['Ano'] = pd.to_datetime(base_producao['Ano'], format='%Y', errors='coerce').dt.year

    base_demanda_filtrada = base_demanda[(base_demanda['Ano'] >= anos_selecionados[0]) & (base_demanda['Ano'] <= anos_selecionados[1])]
    base_producao_filtrada = base_producao[(base_producao['Ano'] >= anos_selecionados[0]) & (base_producao['Ano'] <= anos_selecionados[1])]

    # Normalizar os dados
    base_preco_filtrada['Preço_Normalizado'] = (base_preco_filtrada['y'] - base_preco_filtrada['y'].min()) / (base_preco_filtrada['y'].max() - base_preco_filtrada['y'].min())
    base_demanda_filtrada['Demanda_Normalizada'] = (base_demanda_filtrada['Total world'] - base_demanda_filtrada['Total world'].min()) / (base_demanda_filtrada['Total world'].max() - base_demanda_filtrada['Total world'].min())
    base_producao_filtrada['Producao_Normalizada'] = (base_producao_filtrada['Total World'] - base_producao_filtrada['Total World'].min()) / (base_producao_filtrada['Total World'].max() - base_producao_filtrada['Total World'].min())

    # Gráfico comparativo
    fig_comparativo = go.Figure()
    fig_comparativo.add_trace(go.Scatter(x=base_preco_filtrada.reset_index()['ds'], y=base_preco_filtrada['Preço_Normalizado'], mode='lines', name='Preço'))
    fig_comparativo.add_trace(go.Scatter(x=base_demanda_filtrada['Ano'], y=base_demanda_filtrada['Demanda_Normalizada'], mode='lines', name='Demanda'))
    fig_comparativo.add_trace(go.Scatter(x=base_producao_filtrada['Ano'], y=base_producao_filtrada['Producao_Normalizada'], mode='lines', name='Produção'))
    fig_comparativo.update_layout(
        title="Preço, Demanda e Produção de Petróleo (Normalizados)",
        xaxis_title="Ano",
        yaxis_title="Valor Normalizado",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        height=400
    )
    st.plotly_chart(fig_comparativo, use_container_width=True)
