# Tech Challenge 04 | Análise e Forecasting do Petróleo Brent

Aplicação em Streamlit para análise histórica, contextualização geopolítica e previsão de curto prazo do preço do petróleo Brent. O projeto combina exploração visual, storytelling orientado a negócio e um modelo de séries temporais com Prophet.

## Visão de portfólio

Este projeto foi estruturado para demonstrar capacidade em:

- construção de produto analítico com Streamlit;
- tratamento e integração de bases em Excel;
- análise temporal com apoio de eventos históricos;
- validação de modelo preditivo com métricas objetivas;
- comunicação executiva de achados para tomada de decisão.

## Problema de negócio

O preço do Brent responde rapidamente a choques de oferta, crises geopolíticas, recessões e mudanças estruturais na demanda global por energia. A proposta deste projeto é transformar esse contexto em uma experiência analítica navegável, capaz de:

- explicar movimentos históricos relevantes do preço;
- relacionar oferta, demanda e volatilidade;
- projetar cenários de curto prazo com um modelo de forecasting;
- apoiar uma leitura mais estratégica do mercado.

## O que a aplicação entrega

- `Visão Geral`: contexto do projeto, objetivo analítico e narrativa executiva.
- `Dashboard`: indicadores-chave, série histórica, volatilidade e comparação normalizada entre preço, demanda e produção.
- `Análise Geral`: leitura histórica guiada dos principais movimentos do Brent.
- `Eventos Históricos`: destaque visual e analítico de eventos geopolíticos e econômicos.
- `Machine Learning`: previsão com Prophet, intervalo de confiança, tabela de projeções e métricas de validação.
- `Conclusão`: síntese executiva e próximos passos recomendados.

## Stack

- Python
- Streamlit
- Pandas
- Plotly
- Prophet
- OpenPyXL
- Scikit-learn

## Estrutura do repositório

```text
.
├── app/
│   ├── main.py
│   ├── assets/
│   ├── pages/
│   └── services/
├── archive/
├── data/
├── notebooks/
├── main.py
└── README.md
```

## Como executar

1. Crie e ative um ambiente virtual.
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Inicie a aplicação:

```bash
streamlit run main.py
```

## Base de dados

- Preço histórico do Brent: IPEA
- Demanda e produção mundial: planilhas consolidadas no diretório `data/`
- Eventos históricos: arquivo `app/assets/eventos.json`

## Melhorias implementadas nesta revisão

- centralização dos caminhos de arquivos e leitura de dados;
- reorganização da estrutura em `app`, `data`, `assets` e `archive`;
- inclusão de `.gitignore` para evitar artefatos locais no repositório;
- dependências explícitas no `requirements.txt`;
- métricas de avaliação na página de Machine Learning;
- README reescrito com foco em apresentação de portfólio.

## Próximos incrementos recomendados

- separar regras visuais e utilitários compartilhados em módulos próprios;
- adicionar testes para transformações de dados e métricas;
- publicar a aplicação em ambiente acessível com URL pública;
- substituir partes do texto estático por conclusões derivadas automaticamente dos dados.
