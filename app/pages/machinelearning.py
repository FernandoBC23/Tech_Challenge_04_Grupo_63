import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error

from app.services.data_loader import (
    carregar_melhores_hiperparametros,
    carregar_preco_petroleo,
)

st.markdown(
    """
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
    """,
    unsafe_allow_html=True,
)


def calcular_metricas(y_real, y_previsto):
    mae = mean_absolute_error(y_real, y_previsto)
    rmse = mean_squared_error(y_real, y_previsto) ** 0.5
    denominador = y_real.replace(0, pd.NA)
    mape = (((y_real - y_previsto).abs() / denominador).dropna().mean()) * 100
    return mae, rmse, mape


def alinhar_previsao_teste(test, forecast):
    comparativo = test[["ds", "y"]].merge(
        forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]],
        on="ds",
        how="inner",
    )
    return comparativo.sort_values("ds").reset_index(drop=True)


def plot_interactive_graph_with_confidence(train, test, forecast, forecast_future):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=train["ds"],
            y=train["y"],
            mode="lines",
            name="Treinamento",
            line=dict(color="#4A90E2", width=2),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=test["ds"],
            y=test["y"],
            mode="lines",
            name="Teste",
            line=dict(color="#F5A623", width=2),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast["ds"],
            y=forecast["yhat"],
            mode="lines",
            name="Previsão - Teste",
            line=dict(color="#7ED321", dash="dash"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=pd.concat([forecast["ds"], forecast["ds"][::-1]]),
            y=pd.concat([forecast["yhat_upper"], forecast["yhat_lower"][::-1]]),
            fill="toself",
            fillcolor="rgba(126, 211, 33, 0.3)",
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast_future["ds"],
            y=forecast_future["yhat"],
            mode="lines",
            name="Previsão - Futuro",
            line=dict(color="#FFC300", dash="dash"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=pd.concat([forecast_future["ds"], forecast_future["ds"][::-1]]),
            y=pd.concat(
                [forecast_future["yhat_upper"], forecast_future["yhat_lower"][::-1]]
            ),
            fill="toself",
            fillcolor="rgba(255, 195, 0, 0.3)",
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.update_layout(
        title="Previsão Interativa do Preço do Petróleo com Intervalos de Confiança",
        xaxis_title="Data",
        yaxis_title="Preço (USD)",
        plot_bgcolor="#1B1B1B",
        paper_bgcolor="#1B1B1B",
        font=dict(color="white"),
        legend=dict(bgcolor="#1B1B1B", font=dict(color="white")),
    )

    return fig


def render_machinelearning():
    html_title = """
    <style>
    .title-test {
        font-weight: bold;
        font-size: 36px;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 5px;
    }
    </style>
    <center><h1 class="title-test">Previsão Dinâmica do Preço do Petróleo Brent com Machine Learning</h1></center>"""

    st.markdown(html_title, unsafe_allow_html=True)

    base_preco = carregar_preco_petroleo().copy()
    base_preco = base_preco.rename(columns={"Data": "ds", "Preço": "y"})

    if base_preco.empty:
        st.error("Os dados estão vazios. Verifique o arquivo de dados.")
        return

    max_date = base_preco["ds"].max()
    last_3_years_business_days = pd.bdate_range(end=max_date, periods=3 * 252)
    base_preco = base_preco[base_preco["ds"].isin(last_3_years_business_days)].copy()

    if base_preco.empty:
        st.error("Não há dados suficientes nos últimos 3 anos úteis para análise.")
        return

    st.sidebar.header("Ajustes de Parâmetros")
    dias_uteis_previsao = st.sidebar.slider(
        "Número de dias úteis para previsão futura",
        min_value=1,
        max_value=30,
        value=10,
        step=1,
    )

    last_30_business_days = pd.bdate_range(end=max_date, periods=30)
    train = base_preco[~base_preco["ds"].isin(last_30_business_days)].copy()
    test = base_preco[base_preco["ds"].isin(last_30_business_days)].copy()

    if len(train) < 30 or test.empty:
        st.error(
            "O conjunto de treino ou teste está insuficiente. Ajuste os dados ou carregue mais informações."
        )
        return

    try:
        best_params = carregar_melhores_hiperparametros()
    except FileNotFoundError:
        st.error("O arquivo de hiperparâmetros não foi encontrado. Verifique o diretório.")
        return

    model = Prophet(
        changepoint_prior_scale=best_params["changepoint_prior_scale"],
        seasonality_prior_scale=best_params["seasonality_prior_scale"],
    )
    model.fit(train)

    future_test = model.make_future_dataframe(periods=len(test), freq="B")
    forecast = model.predict(future_test)
    forecast_test = forecast[forecast["ds"].isin(test["ds"])].copy()
    comparativo_teste = alinhar_previsao_teste(test, forecast_test)

    if comparativo_teste.empty:
        st.error("Não foi possível alinhar previsões e valores reais no período de teste.")
        return

    future_days = pd.bdate_range(
        start=test["ds"].max() + pd.offsets.BDay(1), periods=dias_uteis_previsao
    )
    forecast_future = model.predict(pd.DataFrame({"ds": future_days}))

    fig = plot_interactive_graph_with_confidence(
        train, test, forecast_test, forecast_future
    )
    st.plotly_chart(fig, use_container_width=True)

    mae, rmse, mape = calcular_metricas(
        comparativo_teste["y"], comparativo_teste["yhat"]
    )

    st.markdown("### Validação do Modelo")
    metrica_1, metrica_2, metrica_3 = st.columns(3)
    metrica_1.metric("MAE", f"US$ {mae:.2f}")
    metrica_2.metric("RMSE", f"US$ {rmse:.2f}")
    metrica_3.metric("MAPE", f"{mape:.2f}%")
    st.caption(
        f"Treino: {train['ds'].min():%d/%m/%Y} a {train['ds'].max():%d/%m/%Y} | "
        f"Teste: {comparativo_teste['ds'].min():%d/%m/%Y} a {comparativo_teste['ds'].max():%d/%m/%Y}"
    )

    col1, col2 = st.columns(2)
    col1.subheader("Insights Dinâmicos")

    media_futura = forecast_future["yhat"].mean()
    min_futura = forecast_future["yhat"].min()
    max_futura = forecast_future["yhat"].max()
    direcao = (
        "alta"
        if forecast_future["yhat"].iloc[-1] >= forecast_future["yhat"].iloc[0]
        else "queda"
    )

    col1.write(
        f"""
    - **Média Prevista**: ${media_futura:.2f}
    - **Maior Valor Previsto**: ${max_futura:.2f}
    - **Menor Valor Previsto**: ${min_futura:.2f}
    - **Tendência no horizonte projetado**: {direcao}
    """
    )

    col2.subheader("Previsões Detalhadas")
    forecast_future["Data"] = forecast_future["ds"].dt.strftime("%d/%m/%Y")
    forecast_table = forecast_future[
        ["Data", "yhat", "yhat_lower", "yhat_upper"]
    ].rename(
        columns={
            "yhat": "Preço Previsto (USD)",
            "yhat_lower": "Limite Inferior",
            "yhat_upper": "Limite Superior",
        }
    )
    col2.dataframe(forecast_table, use_container_width=True)

    csv = forecast_table.to_csv(index=False).encode("utf-8")
    col2.download_button(
        label="Baixar Previsões",
        data=csv,
        file_name="previsoes_petroleo.csv",
        mime="text/csv",
    )

    comparativo_validacao = pd.DataFrame(
        {
            "Data": comparativo_teste["ds"].dt.strftime("%d/%m/%Y"),
            "Real (USD)": comparativo_teste["y"],
            "Previsto (USD)": comparativo_teste["yhat"],
        }
    )
    comparativo_validacao["Erro Absoluto"] = (
        comparativo_validacao["Real (USD)"] - comparativo_validacao["Previsto (USD)"]
    ).abs()

    st.markdown("### Comparativo do Período de Teste")
    st.dataframe(comparativo_validacao, use_container_width=True)

    st.markdown(
        f"""
    ### Análise Detalhada
    A projeção para os próximos {dias_uteis_previsao} dias úteis aponta média de {media_futura:.2f} dólares,
    com faixa entre {min_futura:.2f} e {max_futura:.2f} dólares. No recorte de teste, o modelo registrou
    MAE de {mae:.2f} e RMSE de {rmse:.2f}, o que oferece uma leitura objetiva da qualidade da previsão
    antes de extrapolar o cenário futuro.
    """
    )

    st.divider()

    st.markdown(
        """
    ### Nota sobre os Hiperparâmetros
    Os hiperparâmetros utilizados no modelo Prophet foram calculados previamente em um ambiente externo ao Streamlit.
    Essa abordagem reduz o tempo de resposta da aplicação e deixa explícita a separação entre o processo de tuning
    e a camada de visualização do produto.
    """
    )
