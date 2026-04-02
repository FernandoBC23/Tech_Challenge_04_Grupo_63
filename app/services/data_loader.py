from pathlib import Path
import json

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
ASSETS_DIR = ROOT_DIR / "app" / "assets"
IMAGENS_DIR = ASSETS_DIR / "imagens"

PRECO_PATH = DATA_DIR / "preco_petroleo_brent.xlsx"
DEMANDA_PATH = DATA_DIR / "Demanda_Mundial_Petroleo.xlsx"
PRODUCAO_PATH = DATA_DIR / "Producao_Mundial_Petroleo.xlsx"
HIPERPARAMETROS_PATH = DATA_DIR / "melhores_hiperparametros.json"
EVENTOS_PATH = ASSETS_DIR / "eventos.json"
LOGO_PATH = IMAGENS_DIR / "Logo_Grupo_63.png"
CAPA_PATH = IMAGENS_DIR / "foto_capa_petroleo.webp"


@st.cache_data
def carregar_dados():
    tabela_preco = pd.read_excel(PRECO_PATH)
    tabela_preco = tabela_preco.rename(
        columns={"Preço - petróleo bruto - Brent (FOB)": "Preço"}
    )

    tabela_demanda = pd.read_excel(DEMANDA_PATH)
    tabela_producao = pd.read_excel(PRODUCAO_PATH)

    return tabela_preco, tabela_demanda, tabela_producao


@st.cache_data
def carregar_preco_petroleo():
    tabela_preco, _, _ = carregar_dados()
    tabela_preco["Data"] = pd.to_datetime(tabela_preco["Data"], errors="coerce")
    tabela_preco = tabela_preco.dropna(subset=["Data"]).sort_values("Data").reset_index(
        drop=True
    )
    return tabela_preco


@st.cache_data
def carregar_melhores_hiperparametros():
    with HIPERPARAMETROS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)
