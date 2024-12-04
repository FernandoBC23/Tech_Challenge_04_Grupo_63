import streamlit as st
import pandas as pd
from data_loader import carregar_dados
from prophet import Prophet
import plotly.graph_objects as go
import json

# CSS para layout responsivo e título no padrão
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
        font-size: 36px;
        color: #D4AF37;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Função para carregar os dados com cache
@st.cache_data
def carregar_dados_otimizado():
    return carregar_dados()

# Função principal da página de Machine Learning
def render_machinelearning():
    # Título centralizado com formatação no padrão
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
    <center><h1 class="title-test">Previsão Dinâmica do Preço do Petróleo Brent com Machine Learning</h1></center>"""

    st.markdown(html_title, unsafe_allow_html=True)  

    # Carregar os dados
    base_preco, _, _ = carregar_dados_otimizado()

    # Garantir que a coluna 'Data' está no formato correto
    base_preco['Data'] = pd.to_datetime(base_preco['Data'], errors='coerce')
    base_preco = base_preco.dropna(subset=['Data']).sort_values(by='Data', ascending=True)

    # Renomear colunas
    base_preco = base_preco.rename(columns={'Data': 'ds', 'Preço': 'y'})

    # Verificar se os dados estão corretos
    if base_preco.empty:
        st.error("Os dados estão vazios. Verifique o arquivo de dados.")
        return

    # Filtrar os últimos 3 anos úteis
    max_date = base_preco['ds'].max()
    last_3_years_business_days = pd.bdate_range(end=max_date, periods=3 * 252)
    base_preco = base_preco[base_preco['ds'].isin(last_3_years_business_days)]

    if base_preco.empty:
        st.error("Não há dados suficientes nos últimos 3 anos úteis para análise.")
        return

    # Ajustar dias úteis para previsão futura
    st.sidebar.header("Ajustes de Parâmetros")
    dias_uteis_previsao = st.sidebar.slider("Número de dias úteis para previsão futura", min_value=1, max_value=30, value=10, step=1)

    # Dividir os últimos 3 anos úteis em treino e teste
    last_30_business_days = pd.bdate_range(end=max_date, periods=30)
    train = base_preco[~base_preco['ds'].isin(last_30_business_days)]
    test = base_preco[base_preco['ds'].isin(last_30_business_days)]

    # Verificar se há dados suficientes para treino
    if len(train) < 30:
        st.error("O conjunto de treino tem menos de 30 linhas válidas. Ajuste os dados ou carregue mais informações.")
        return

    # Carregar os melhores hiperparâmetros
    try:
        with open('Dados/melhores_hiperparametros.json', 'r') as f:
            best_params = json.load(f)
    except FileNotFoundError:
        st.error("O arquivo de hiperparâmetros não foi encontrado. Verifique o diretório.")
        return

    # Treinar o modelo Prophet com os melhores hiperparâmetros
    model = Prophet(
        changepoint_prior_scale=best_params['changepoint_prior_scale'],
        seasonality_prior_scale=best_params['seasonality_prior_scale']
    )
    model.fit(train)

    # Fazer previsões futuras para o período de teste
    future_teste_hiper = model.make_future_dataframe(periods=len(test), freq='B')
    forecast = model.predict(future_teste_hiper)

    # Fazer previsões adicionais para os próximos dias úteis ajustáveis
    future_days = pd.date_range(start=test['ds'].max() + pd.Timedelta(days=1), periods=dias_uteis_previsao, freq='B')
    future_days_df = pd.DataFrame({'ds': future_days})
    forecast_future = model.predict(future_days_df)

    # Função para gerar o gráfico interativo com intervalos de confiança
    def plot_interactive_graph_with_confidence(train, test, forecast, forecast_future):
        fig = go.Figure()

        # Dados de treinamento
        fig.add_trace(go.Scatter(
            x=train['ds'], y=train['y'],
            mode='lines', name='Treinamento',
            line=dict(color='#4A90E2', width=2)
        ))

        # Dados de teste
        fig.add_trace(go.Scatter(
            x=test['ds'], y=test['y'],
            mode='lines', name='Teste',
            line=dict(color='#F5A623', width=2)
        ))

        # Previsões do período de teste
        fig.add_trace(go.Scatter(
            x=forecast['ds'], y=forecast['yhat'],
            mode='lines', name='Previsão - Teste',
            line=dict(color='#7ED321', dash='dash')
        ))

        # Intervalo de confiança para o teste
        fig.add_trace(go.Scatter(
            x=pd.concat([forecast['ds'], forecast['ds'][::-1]]),
            y=pd.concat([forecast['yhat_upper'], forecast['yhat_lower'][::-1]]),
            fill='toself',
            fillcolor='rgba(126, 211, 33, 0.3)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=False
        ))

        # Previsões futuras
        fig.add_trace(go.Scatter(
            x=forecast_future['ds'], y=forecast_future['yhat'],
            mode='lines', name='Previsão - Futuro',
            line=dict(color='#FFC300', dash='dash')
        ))

        # Intervalo de confiança para os dias futuros
        fig.add_trace(go.Scatter(
            x=pd.concat([forecast_future['ds'], forecast_future['ds'][::-1]]),
            y=pd.concat([forecast_future['yhat_upper'], forecast_future['yhat_lower'][::-1]]),
            fill='toself',
            fillcolor='rgba(255, 195, 0, 0.3)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=False
        ))

        fig.update_layout(
            title="Previsão Interativa do Preço do Petróleo com Intervalos de Confiança",
            xaxis_title="Data",
            yaxis_title="Preço (USD)",
            plot_bgcolor="#1B1B1B",
            paper_bgcolor="#1B1B1B",
            font=dict(color="white"),
            legend=dict(bgcolor="#1B1B1B", font=dict(color="white"))
        )

        return fig

    # Exibir o gráfico
    fig = plot_interactive_graph_with_confidence(train, test, forecast, forecast_future)
    st.plotly_chart(fig, use_container_width=True)

    # Exibir insights dinâmicos com descrição detalhada
    col1, col2 = st.columns(2)

    col1.subheader("Insights Dinâmicos")
    media_futura = forecast_future['yhat'].mean()
    min_futura = forecast_future['yhat'].min()
    max_futura = forecast_future['yhat'].max()

    col1.write(f"""
    - **Média Prevista**: ${media_futura:.2f}
    - **Maior Valor Previsto**: ${max_futura:.2f}
    - **Menor Valor Previsto**: ${min_futura:.2f}
    """)

    col2.subheader("Previsões Detalhadas")
    forecast_future['Data'] = forecast_future['ds'].dt.strftime('%d/%m/%Y')
    forecast_table = forecast_future[['Data', 'yhat', 'yhat_lower', 'yhat_upper']].rename(columns={
        'yhat': 'Preço Previsto (USD)',
        'yhat_lower': 'Limite Inferior',
        'yhat_upper': 'Limite Superior'
    })
    col2.dataframe(forecast_table, use_container_width=True)

    # Adicionar botão de download para as previsões
    csv = forecast_table.to_csv(index=False).encode('utf-8')
    col2.download_button(
        label="Baixar Previsões",
        data=csv,
        file_name="previsoes_petroleo.csv",
        mime="text/csv"
    )

    # Descrição mais detalhada abaixo do gráfico
    st.markdown(f"""
    ### Análise Detalhada
    A previsão do preço do petróleo Brent apresenta uma média projetada de {media_futura:.2f} dólares, 
    com um intervalo de valores entre {min_futura:.2f} dólares e {max_futura:.2f} dólares. 
    Estes dados destacam a estabilidade no curto prazo, mas os intervalos de confiança mais amplos
    para o longo prazo indicam possíveis oscilações devido a fatores externos, como crises geopolíticas 
    ou mudanças na demanda global.
    """)

    st.divider()

    # Nota sobre os hiperparâmetros
    st.markdown("""
    ### Nota sobre os Hiperparâmetros
    Os hiperparâmetros utilizados no modelo Prophet foram calculados previamente em um ambiente externo ao Streamlit. 
    Isso foi necessário devido ao tempo significativo que o ajuste de hiperparâmetros demanda. Para otimizar esse processo, 
    realizamos o ajuste em um ambiente de maior capacidade computacional, salvando os melhores valores em um 
    arquivo JSON (`melhores_hiperparametros.json`), que é carregado nesta aplicação para agilizar a configuração do modelo.
    """)
