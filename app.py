
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Painel ParaguaTrader", layout="wide", initial_sidebar_state="expanded")

# Estilo dark mode
st.markdown(
    """<style>
        body { background-color: #111 !important; color: #EEE !important; }
        .stApp { background-color: #111; }
    </style>""", unsafe_allow_html=True
)

# Logo
st.image("PARAGUATRADER - LOGO.png", width=200)

# Carregar os dados
df = pd.read_excel("Dados de Trading.xlsx")

# Formatando datas
if 'Data' in df.columns:
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)

# Filtros na barra lateral
st.sidebar.header("Filtros")
times = st.sidebar.multiselect("Times", df["Time"].dropna().unique())
ligas = st.sidebar.multiselect("Ligas", df["Campeonato"].dropna().unique())
paises = st.sidebar.multiselect("Países", df["País"].dropna().unique())
metodos = st.sidebar.multiselect("Métodos", df["Método"].dropna().unique())
data_ini = st.sidebar.date_input("Data Início", df['Data'].min())
data_fim = st.sidebar.date_input("Data Fim", df['Data'].max())

# Aplicar filtros
filtro = (df["Data"] >= pd.to_datetime(data_ini)) & (df["Data"] <= pd.to_datetime(data_fim))
if times:
    filtro &= df["Time"].isin(times)
if ligas:
    filtro &= df["Campeonato"].isin(ligas)
if paises:
    filtro &= df["País"].isin(paises)
if metodos:
    filtro &= df["Método"].isin(metodos)

df_filtrado = df[filtro]

# Gráfico de lucro por mês
df_filtrado['AnoMes'] = df_filtrado['Data'].dt.to_period("M").astype(str)
lucro_mes = df_filtrado.groupby("AnoMes")["Profit / Loss"].sum().reset_index()
fig_lucro = px.bar(lucro_mes, x="AnoMes", y="Profit / Loss", title="Lucro por Mês",
                   color="Profit / Loss", color_continuous_scale=["red", "green"])
st.plotly_chart(fig_lucro, use_container_width=True)

# Lucro acumulado
df_filtrado = df_filtrado.sort_values("Data")
df_filtrado["Lucro Acumulado"] = df_filtrado["Profit / Loss"].cumsum()
fig_acumulado = px.line(df_filtrado, x="Data", y="Lucro Acumulado", title="Evolução da Banca")
st.plotly_chart(fig_acumulado, use_container_width=True)
