import streamlit as st
import pandas as pd
import json
from datetime import datetime
from data_loader import carregar_dados
import plotly.graph_objects as go

# CSS para layout responsivo
st.markdown("""
    <style>
    div.block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;        
    }
    .title-test {
        font-weight: bold;
        font-size: 24px;
        color: #D4AF37;
        text-align: center;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

def render_eventos():
    # Inicializar o estado da sessão para controlar a exibição
    if 'acao_selecionada' not in st.session_state:
        st.session_state.acao_selecionada = "Visualizar Eventos"

    # Carregar dados
    base_preco, _, _ = carregar_dados()

    # Função para normalizar o preço para visualização
    def normalizar_serie(serie):
        return (serie - serie.min()) / (serie.max() - serie.min())

    # Normalizar o preço do petróleo
    base_preco['Preço_Normalizado'] = normalizar_serie(base_preco['Preço'])

    # Definir caminho para o arquivo JSON de eventos
    arquivo_eventos = "eventos.json"

    # Função para carregar eventos do arquivo JSON e garantir que todos tenham a chave "descricao"
    def carregar_eventos():
        try:
            with open(arquivo_eventos, "r") as f:
                eventos = json.load(f)
            # Adicionar "descricao" aos eventos que não a possuem
            for evento, dados in eventos.items():
                if "descricao" not in dados:
                    eventos[evento]["descricao"] = "Descrição não disponível."
            return eventos
        except FileNotFoundError:
            return {}

    # Carregar e atualizar eventos existentes
    eventos = carregar_eventos()
  
    # Conversão das datas dos eventos para o formato datetime
    for nome, dados in eventos.items():
        dados["inicio"] = pd.to_datetime(dados["inicio"])
        dados["fim"] = pd.to_datetime(dados["fim"])

    # Exibir gráfico e indicadores
    evento_visualizar = st.sidebar.selectbox("Selecione o Evento para Visualização", ["Nenhum"] + list(eventos.keys()))

    def calcular_impacto_evento(base_preco, inicio, fim, intervalo_antes, intervalo_depois, nome_evento):
        periodo_antes = base_preco[(base_preco['Data'] >= inicio - pd.DateOffset(months=intervalo_antes)) & (base_preco['Data'] < inicio)]
        periodo_durante = base_preco[(base_preco['Data'] >= inicio) & (base_preco['Data'] <= fim)]
        periodo_depois = base_preco[(base_preco['Data'] > fim) & (base_preco['Data'] <= fim + pd.DateOffset(months=intervalo_depois))]

        media_antes = periodo_antes['Preço'].mean()
        media_durante = periodo_durante['Preço'].mean()
        media_depois = periodo_depois['Preço'].mean()

        volatilidade_antes = periodo_antes['Preço'].std()
        volatilidade_durante = periodo_durante['Preço'].std()
        volatilidade_depois = periodo_depois['Preço'].std()

        st.write(f"### Indicadores para {nome_evento}")
        
        with st.container():
            st.write("#### Preço Médio")
            col1, col2, col3 = st.columns(3)
            col1.metric(f"Antes ({(inicio - pd.DateOffset(months=intervalo_antes)).strftime('%Y-%m-%d')} a {inicio.strftime('%Y-%m-%d')})", f"$ {media_antes:.2f}")
            col2.metric(f"Durante ({inicio.strftime('%Y-%m-%d')} a {fim.strftime('%Y-%m-%d')})", f"$ {media_durante:.2f}")
            col3.metric(f"Depois ({fim.strftime('%Y-%m-%d')} a {(fim + pd.DateOffset(months=intervalo_depois)).strftime('%Y-%m-%d')})", f"$ {media_depois:.2f}")

            st.write("#### Volatilidade")
            col4, col5, col6 = st.columns(3)
            col4.metric("Volatilidade Antes", f"{volatilidade_antes:.2f}")
            col5.metric("Volatilidade Durante", f"{volatilidade_durante:.2f}")
            col6.metric("Volatilidade Depois", f"{volatilidade_depois:.2f}")

        st.divider()
        
    # Função de análise dos indicadores com base nas variações específicas de preço e volatilidade
    def analisar_variacao_preco(preco_anterior, preco_durante, preco_posterior):
        # Preço Médio: Análise do aumento, queda ou estabilidade
        analise_preco = ""
        
        # Análise da variação do preço médio antes e durante o evento
        variacao_antes_durante = (preco_durante - preco_anterior) / preco_anterior * 100
        if preco_durante > preco_anterior:
            if variacao_antes_durante > 5:
                analise_preco += f"Aumento significativo no preço médio durante o evento (aproximadamente {variacao_antes_durante:.2f}%), possivelmente causado por alta demanda, restrições na oferta, ou fatores de incerteza como instabilidade geopolítica ou crises imprevistas. "
            else:
                analise_preco += f"Leve aumento no preço médio durante o evento (aproximadamente {variacao_antes_durante:.2f}%), que pode estar relacionado a uma demanda ligeiramente superior ou ajustes moderados na oferta. "
        elif preco_durante < preco_anterior:
            if abs(variacao_antes_durante) > 5:
                analise_preco += f"Queda significativa no preço médio durante o evento (aproximadamente {variacao_antes_durante:.2f}%), sugerindo uma redução na demanda ou aumento da oferta. "
            else:
                analise_preco += f"Leve queda no preço médio durante o evento (aproximadamente {variacao_antes_durante:.2f}%), talvez indicando uma estabilização do mercado ou menor pressão na demanda. "

        # Análise da variação do preço médio durante e após o evento
        variacao_durante_posterior = (preco_posterior - preco_durante) / preco_durante * 100
        if preco_posterior > preco_durante:
            if variacao_durante_posterior > 5:
                analise_preco += f"Após o evento, houve uma elevação significativa no preço médio (aproximadamente {variacao_durante_posterior:.2f}%), sugerindo recuperação da demanda ou novas restrições na oferta. "
            else:
                analise_preco += f"Após o evento, o preço médio teve uma leve alta (aproximadamente {variacao_durante_posterior:.2f}%), possivelmente refletindo um ajuste gradual do mercado. "
        elif preco_posterior < preco_durante:
            if abs(variacao_durante_posterior) > 5:
                analise_preco += f"Após o evento, o preço médio caiu significativamente (aproximadamente {variacao_durante_posterior:.2f}%), possivelmente indicando estabilização da demanda ou aumento contínuo na oferta. "
            else:
                analise_preco += f"Após o evento, houve uma leve queda no preço médio (aproximadamente {variacao_durante_posterior:.2f}%), o que pode apontar para um ajuste natural do mercado. "
        
        return analise_preco

    def analisar_variacao_volatilidade(volatilidade_anterior, volatilidade_durante, volatilidade_posterior):
        # Volatilidade: Análise do aumento, queda ou estabilidade
        analise_volatilidade = ""

        # Análise da variação da volatilidade antes e durante o evento
        variacao_antes_durante_vol = (volatilidade_durante - volatilidade_anterior) / volatilidade_anterior * 100
        if volatilidade_durante > volatilidade_anterior:
            if variacao_antes_durante_vol > 5:
                analise_volatilidade += f"Aumento significativo na volatilidade durante o evento (aproximadamente {variacao_antes_durante_vol:.2f}%), indicando um período de incertezas ou instabilidade, possivelmente relacionado a eventos inesperados. "
            else:
                analise_volatilidade += f"Leve aumento na volatilidade durante o evento (aproximadamente {variacao_antes_durante_vol:.2f}%), o que pode refletir flutuações de mercado controladas. "
        elif volatilidade_durante < volatilidade_anterior:
            if abs(variacao_antes_durante_vol) > 5:            
                analise_volatilidade += f"Queda significativa na volatilidade durante o evento (aproximadamente {variacao_antes_durante_vol:.2f}%), sugerindo uma possível estabilização no mercado ou menor exposição a incertezas. "
            else:
                analise_volatilidade += f"Leve queda na volatilidade durante o evento (aproximadamente {variacao_antes_durante_vol:.2f}%), indicando uma redução controlada nas flutuações de mercado. "

        # Análise da variação da volatilidade durante e após o evento
        variacao_durante_posterior_vol = (volatilidade_posterior - volatilidade_durante) / volatilidade_durante * 100
        if volatilidade_posterior > volatilidade_durante:
            if variacao_durante_posterior_vol > 5:
                analise_volatilidade += f"Após o evento, houve um aumento significativo na volatilidade (aproximadamente {variacao_durante_posterior_vol:.2f}%), sugerindo novas incertezas ou instabilidade no mercado. "
            else:
                analise_volatilidade += f"Após o evento, a volatilidade aumentou levemente (aproximadamente {variacao_durante_posterior_vol:.2f}%), o que pode indicar uma recuperação das flutuações normais do mercado. "
        elif volatilidade_posterior < volatilidade_durante:
            if abs(variacao_durante_posterior_vol) > 5:
                analise_volatilidade += f"Após o evento, a volatilidade caiu significativamente (aproximadamente {variacao_durante_posterior_vol:.2f}%), apontando para uma estabilização mais sólida no mercado. "
            else:
                analise_volatilidade += f"Após o evento, a volatilidade teve uma leve queda (aproximadamente {variacao_durante_posterior_vol:.2f}%), o que pode sugerir um ajuste natural do mercado rumo à estabilidade. "
        
        return analise_volatilidade


    # Função para exibir a análise detalhada dos resultados
    def exibir_analise_resultados(media_antes, media_durante, media_depois, volatilidade_antes, volatilidade_durante, volatilidade_depois):
        st.write("#### Análise dos Resultados")

        # Análise do preço médio
        analise_preco = analisar_variacao_preco(media_antes, media_durante, media_depois)
        st.write(f"- **Análise do Preço Médio**: {analise_preco}")

        # Análise da volatilidade
        analise_volatilidade = analisar_variacao_volatilidade(volatilidade_antes, volatilidade_durante, volatilidade_depois)
        st.write(f"- **Análise da Volatilidade**: {analise_volatilidade}")

        st.divider()

    # Função para calcular e exibir indicadores e a análise dos resultados
    def calcular_impacto_evento(base_preco, inicio, fim, intervalo_antes, intervalo_depois, nome_evento):
        periodo_antes = base_preco[(base_preco['Data'] >= inicio - pd.DateOffset(months=intervalo_antes)) & (base_preco['Data'] < inicio)]
        periodo_durante = base_preco[(base_preco['Data'] >= inicio) & (base_preco['Data'] <= fim)]
        periodo_depois = base_preco[(base_preco['Data'] > fim) & (base_preco['Data'] <= fim + pd.DateOffset(months=intervalo_depois))]

        media_antes = periodo_antes['Preço'].mean()
        media_durante = periodo_durante['Preço'].mean()
        media_depois = periodo_depois['Preço'].mean()

        volatilidade_antes = periodo_antes['Preço'].std()
        volatilidade_durante = periodo_durante['Preço'].std()
        volatilidade_depois = periodo_depois['Preço'].std()

        st.write(f"### Indicadores para {nome_evento}")
        
        with st.container():
            st.write("#### Preço Médio")
            col1, col2, col3 = st.columns(3)
            col1.metric(f"Antes ({(inicio - pd.DateOffset(months=intervalo_antes)).strftime('%Y-%m-%d')} a {inicio.strftime('%Y-%m-%d')})", f"$ {media_antes:.2f}")
            col2.metric(f"Durante ({inicio.strftime('%Y-%m-%d')} a {fim.strftime('%Y-%m-%d')})", f"$ {media_durante:.2f}")
            col3.metric(f"Depois ({fim.strftime('%Y-%m-%d')} a {(fim + pd.DateOffset(months=intervalo_depois)).strftime('%Y-%m-%d')})", f"$ {media_depois:.2f}")

            st.write("#### Volatilidade")
            col4, col5, col6 = st.columns(3)
            col4.metric("Volatilidade Antes", f"{volatilidade_antes:.2f}")
            col5.metric("Volatilidade Durante", f"{volatilidade_durante:.2f}")
            col6.metric("Volatilidade Depois", f"{volatilidade_depois:.2f}")

        st.divider()

        # Exibir análise dos resultados
        exibir_analise_resultados(media_antes, media_durante, media_depois, volatilidade_antes, volatilidade_durante, volatilidade_depois)

        # Exibir descrição do evento
        descricao = eventos[nome_evento].get("descricao", "Descrição não disponível.")
        st.write("#### Descrição do Evento")
        st.write(descricao)


    if evento_visualizar == "Nenhum":
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
        <center><h1 class="title-test">Eventos Históricos do Petróleo Brent </h1></center>"""

        st.markdown(html_title, unsafe_allow_html=True)  

        # Texto introdutório
        st.write("""
        <div style="text-align: justify; font-size: 1.1rem;">
            Os eventos históricos desempenham um papel crucial na formação dos preços do petróleo Brent. 
            Este gráfico apresenta a linha do tempo do preço normalizado e destaca os períodos de eventos 
            importantes, como crises geopolíticas, conflitos e mudanças no mercado energético. Explore os 
            eventos para entender como eles influenciaram o mercado global.
        </div>
        """, unsafe_allow_html=True)      

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=base_preco['Data'], y=base_preco['Preço_Normalizado'], mode='lines', name='Preço Normalizado'))
        for idx, (nome, dados) in enumerate(eventos.items()):
            inicio, fim = dados["inicio"], dados["fim"]
            # Definir a posição do rótulo com base no índice
            if idx % 3 == 0:
                position = "top left"
            elif idx % 3 == 1:
                position = "bottom right"
            else:
                position = "top left"
            
            fig.add_vrect(
                x0=inicio, x1=fim,
                fillcolor="#FADF62", opacity=0.2, line_width=0,
                annotation_text=nome,
                annotation_position=position
            )

        # Ajustar layout do gráfico para mais espaço vertical
        fig.update_layout(
            margin=dict(t=50, b=50, l=50, r=50),  # Ajuste as margens conforme necessário
            xaxis_title="Ano",
            yaxis_title="Valor Normalizado",
            title="Linha do Tempo de Preços com Eventos Marcantes",
            title_x=0.5
        )

        fig.update_layout(
            title="Linha do Tempo de Preços com Eventos Marcantes",
            xaxis_title="Ano",
            yaxis_title="Valor Normalizado"
        )
        st.plotly_chart(fig)
    else:
        inicio, fim = eventos[evento_visualizar]["inicio"], eventos[evento_visualizar]["fim"]
        intervalo_antes = st.sidebar.slider("Meses antes do evento", 1, 24, 6)
        intervalo_depois = st.sidebar.slider("Meses depois do evento", 1, 24, 6)
        periodo_total = base_preco[(base_preco['Data'] >= inicio - pd.DateOffset(months=intervalo_antes)) & 
                                (base_preco['Data'] <= fim + pd.DateOffset(months=intervalo_depois))]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=periodo_total['Data'], y=periodo_total['Preço_Normalizado'], mode='lines', name='Preço Normalizado'))
        fig.add_vrect(x0=inicio, x1=fim, fillcolor="#FADF62", opacity=0.3, line_width=0, annotation_text=evento_visualizar, annotation_position="top left")
        fig.update_layout(
            title={
                'text': f"Análise do Evento: {evento_visualizar}",
                'font': {
                    'size': 32  # Ajuste o tamanho conforme necessário
                }
            },
            xaxis_title="Ano",
            yaxis_title="Valor Normalizado"
        )
        st.plotly_chart(fig)

        
        calcular_impacto_evento(base_preco, inicio, fim, intervalo_antes, intervalo_depois, evento_visualizar)



