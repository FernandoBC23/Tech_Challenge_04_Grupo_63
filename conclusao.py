import streamlit as st

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

def render_conclusao():
    st.markdown("""
    ## Conclusão do Projeto: Uma Visão Estratégica sobre o Mercado do Petróleo Brent

    O projeto explorou a influência de eventos globais e geopolíticos no comportamento do mercado de petróleo Brent, proporcionando uma análise robusta para compreender suas oscilações e implicações estratégicas. As principais conclusões incluem:

    ### Principais Conclusões

    1. **Impacto dos Eventos Globais no Preço do Petróleo**
       Eventos históricos demonstraram como crises e conflitos globais moldam o mercado. Destacamos:
       - **Guerra do Golfo (1990-1991)**: Resultou em um choque de oferta devido à intervenção militar, levando a um aumento significativo nos preços.
       - **Crise Financeira de 2008**: Marcada por picos de preços seguidos por quedas abruptas, causadas pela recessão global e pela redução da demanda.
       - **Primavera Árabe (2010-2011)**: A instabilidade política no Oriente Médio impactou diretamente a produção, causando oscilações de preço.
       - **Guerra de Preços (2014-2016)**: O confronto entre a OPEP e o shale oil dos EUA levou a quedas prolongadas nos preços.
       - **Pandemia de 2020**: Causou a maior desaceleração de demanda já registrada, provocando volatilidade extrema.
       - **Guerra entre Rússia e Ucrânia (2022)**: Intensificou preocupações energéticas globais, especialmente na Europa, aumentando significativamente os preços.

       Esses eventos reforçam a necessidade de monitorar variáveis externas e avaliar os riscos em mercados voláteis.

    2. **Relevância Estratégica do Brent como Referência Global**
       O Brent serve como um barômetro para medir o impacto de:
       - **Políticas da OPEP**.
       - **Avanços tecnológicos no shale oil**.
       - **Oscilações de demanda causadas por crises econômicas e geopolíticas**.

       Além de influenciar diretamente o setor energético, o Brent impacta a formulação de políticas públicas e decisões empresariais em setores estratégicos.

    3. **Machine Learning e Previsões Dinâmicas**
       A integração do modelo **Prophet** permitiu analisar e prever o comportamento dos preços:
       - **Previsões ajustáveis**: Insights precisos para períodos curtos e médios.
       - **Intervalos de confiança**: Destacaram a importância de monitorar incertezas em momentos de instabilidade.
       - **Processamento eficiente**: Hiperparâmetros otimizados fora do Streamlit reduziram tempos de processamento e aprimoraram os resultados.

       O uso do aprendizado de máquina demonstrou como ferramentas analíticas avançadas podem complementar métodos tradicionais, fornecendo insights valiosos para mercados complexos.

    ### Reflexões Finais
    O mercado de petróleo Brent é um indicador crucial para a economia global. Suas flutuações refletem:
    - A vulnerabilidade a choques externos.
    - A necessidade de estratégias resilientes em setores críticos como transporte, aviação e energia.

    Além disso, crises históricas aceleraram a transição para fontes renováveis e tecnologias mais eficientes, destacando a importância de investir em soluções sustentáveis.

    ### Próximos Passos
    Para aprofundar as análises futuras, recomenda-se:
    - **Incorporar variáveis externas**: Como produção global, estoques e indicadores econômicos.
    - **Aprimorar modelos preditivos**: Integrar séries temporais multivariadas para capturar dinâmicas complexas.
    - **Expandir o escopo de análise**: Considerando o impacto da transição energética e a adoção de fontes renováveis.

    Este projeto destacou a relevância de unir dados históricos, aprendizado de máquina e conhecimento setorial para uma compreensão estratégica do mercado global de petróleo.

    ---

    ### Referências
    - **Dados Históricos**: IPEA - Preços do Petróleo Brent ([Link](http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view)).
    - **Relatórios Econômicos**: OPEC ([Link](https://publications.opec.org/asb/Download)).
    - **Modelo Prophet**: Meta (Documentação Oficial: [Link](https://facebook.github.io/prophet/)).    
    """)

    st.markdown("""
        ### Grupo 63 - FIAP
        - **RM355682– Cristina Filippini**
        - **RM355774– Fernando Chagas**
        - **RM355488– Ingrid Miranda**        
        """, unsafe_allow_html=True)