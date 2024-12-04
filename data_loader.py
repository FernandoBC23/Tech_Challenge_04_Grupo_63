import streamlit as st
import pandas as pd

# data_loader.py
@st.cache_data
def carregar_dados():
    tabela_preco = pd.read_excel("Dados/preco_petroleo_brent.xlsx")
    tabela_preco = tabela_preco.rename(columns={"Preço - petróleo bruto - Brent (FOB)": "Preço"})

    tabela_demanda = pd.read_excel("Dados/Demanda_Mundial_Petroleo.xlsx")
    tabela_producao = pd.read_excel("Dados/Producao_Mundial_Petroleo.xlsx")

    return tabela_preco, tabela_demanda, tabela_producao
