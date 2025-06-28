import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots


# Configuração da página
st.set_page_config(
    layout="wide", 
    page_title="📊 Análise de Vendas - Livraria",
    page_icon="📚"
)


# Carregar os dados
@st.cache_data
def load_data(file_path = 'df.csv'):
    data = pd.read_csv(file_path)
    if "order_id" in data.columns:
        data = data.drop_duplicates(subset=["order_id"])
    return data

def filter_data(rating=False, file_path = 'df.csv'):

    df = load_data(file_path = file_path)
    # Filtros interativos
    genres = df["genre_desc"].unique().tolist()
    selected_genre = st.sidebar.pills("Selecione o(s) gênero(s):",
                                        genres,
                                        selection_mode="multi",
                                        default=genres,
                                        help="Escolha os gêneros para análise")
    if selected_genre == []:
        selected_genre = genres  # Se nenhum gênero for selecionado, mostrar todos

    min_price, max_price = float(df["price"].min()), float(df["price"].max())
    selected_price_range = st.sidebar.slider(
        "💵 Intervalo de preço:", 
        min_price, max_price, 
        (min_price, max_price),
        help="Defina a faixa de preço para análise"
    )
    if not rating:
        discount_option = st.sidebar.radio(
            "🏷️ Filtro de desconto:",
            ("Todos os produtos", "Apenas com desconto"),
            help="Escolha se deseja ver todos os produtos ou apenas os vendidos com desconto"
        )


    # Aplicar filtros
    df_filtered = df[
        (df["genre_desc"].isin(selected_genre)) &
        (df["price"] >= selected_price_range[0]) &
        (df["price"] <= selected_price_range[1])
    ]
    if not rating:
        if discount_option == "Apenas com desconto":
            df_filtered = df_filtered[df_filtered["discount"] > 0]

    return df_filtered


pg = st.navigation(["Geral.py", "Avaliações.py"])
# Sidebar com filtros estilizada
st.sidebar.markdown("## 🎛️ Painel de Filtros")
st.sidebar.markdown("---")
pg.run()