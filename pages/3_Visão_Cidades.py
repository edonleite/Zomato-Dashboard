# ==================================================
# Bibliotecas Necessárias
# ==================================================
import pandas as pd
import inflection
import plotly.express as px
import streamlit as st
from PIL import Image

# ==================================================
# Configuração da Página
# ==================================================
st.set_page_config(
    page_title="Visão Cidades",
    page_icon="🏙️",
    layout="wide"
)

# ==================================================
# Funções Auxiliares
# ==================================================
def country_name(country_id):
    COUNTRIES = {
        1: "India",
        14: "Australia",
        30: "Brazil",
        37: "Canada",
        94: "Indonesia",
        148: "New Zeland",
        162: "Philippines",
        166: "Qatar",
        184: "Singapure",
        189: "South Africa",
        191: "Sri Lanka",
        208: "Turkey",
        214: "United Arab Emirates",
        215: "England",
        216: "United States of America",
    }
    return COUNTRIES.get(country_id, "Unknown")


def create_price_type(price_range):
    return (
        "cheap" if price_range == 1 else
        "normal" if price_range == 2 else
        "expensive" if price_range == 3 else
        "gourmet"
    )


def rename_columns(dataframe):
    df = dataframe.copy()
    cols = [inflection.titleize(c) for c in df.columns]
    cols = [c.replace(" ", "") for c in cols]
    cols = [inflection.underscore(c) for c in cols]
    df.columns = cols
    return df


def color_name(color_code):
    COLORS = {
        "3F7E00": "darkgreen",
        "5BA829": "green",
        "9ACD32": "lightgreen",
        "CDD614": "orange",
        "FFBA00": "red",
        "CBCBC8": "darkred",
        "FF7800": "darkred",
    }
    return COLORS.get(color_code, "gray")


# ==================================================
# Cache de Dados
# ==================================================
@st.cache_data
def load_data():
    return pd.read_csv("dataset/zomato.csv")


@st.cache_data
def clean_data(df):
    df = rename_columns(df)
    df["country"] = df["country_code"].apply(country_name)
    df["color_rating_name"] = df["rating_color"].apply(color_name)
    df["price_type"] = df["price_range"].apply(create_price_type)
    df = df.dropna().drop_duplicates()
    df["cuisines"] = df["cuisines"].astype(str).apply(lambda x: x.split(",")[0])
    return df


# ==================================================
# Funções de Visualização
# ==================================================
def qnt_rest_cid(df):
    df = (
        df.groupby(["city", "country"])["restaurant_id"]
        .nunique()
        .reset_index()
        .sort_values("restaurant_id", ascending=False)
    )

    return px.bar(
        df,
        x="city",
        y="restaurant_id",
        color="country",
        text_auto=True,
        title="Quantidade de restaurantes por cidade",
        labels={"restaurant_id": "Total de Restaurantes", "city": "Cidades"},
    )


def med_acima(df, nota, titulo):
    df = (
        df[df["aggregate_rating"] >= nota]
        .groupby(["city", "country"])["restaurant_id"]
        .nunique()
        .reset_index()
        .sort_values("restaurant_id", ascending=False)
        .head(8)
    )

    return px.bar(
        df,
        x="city",
        y="restaurant_id",
        color="country",
        text_auto=True,
        title=titulo,
    )


def faz_rev(df):
    df = (
        df[df["has_table_booking"] == 1]
        .groupby(["city", "country"])["restaurant_id"]
        .nunique()
        .reset_index()
        .sort_values("restaurant_id", ascending=False)
    )

    return px.bar(
        df,
        x="city",
        y="restaurant_id",
        color="country",
        text_auto=True,
        title="Restaurantes que aceitam reservas por cidade",
    )


def qnt_ent(df):
    df = (
        df[df["is_delivering_now"] == 1]
        .groupby(["city", "country"])["restaurant_id"]
        .nunique()
        .reset_index()
        .sort_values("restaurant_id", ascending=False)
    )

    return px.bar(
        df,
        x="city",
        y="restaurant_id",
        color="country",
        text_auto=True,
        title="Cidades com restaurantes em entrega ativa",
    )


def ped_online(df):
    df = (
        df[df["has_online_delivery"] == 1]
        .groupby(["city", "country"])["restaurant_id"]
        .nunique()
        .reset_index()
        .sort_values("restaurant_id", ascending=False)
    )

    return px.bar(
        df,
        x="city",
        y="restaurant_id",
        color="country",
        text_auto=True,
        title="Cidades com pedidos online",
    )


# ==================================================
# Carregamento dos Dados
# ==================================================
df_raw = load_data()
df = clean_data(df_raw)

# ==================================================
# Sidebar
# ==================================================
try:
    image = Image.open("cidade.jpg")
    st.sidebar.image(image, width=250)
except:
    st.sidebar.warning("Imagem não encontrada")

st.sidebar.title("Zomato Restaurants")
st.sidebar.subheader("For the love of Food")
st.sidebar.divider()

paises = st.sidebar.multiselect(
    "Selecione os países:",
    sorted(df["country"].unique()),
    default=[
        "Brazil",
        "Canada",
        "Indonesia",
        "New Zeland",
        "Philippines",
        "Qatar",
        "South Africa",
        "United Arab Emirates",
    ],
)

if st.sidebar.button("🔄 Atualizar dados"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.divider()
st.sidebar.caption("Powered by: Edon Gomes Leite")

# ==================================================
# Filtro
# ==================================================
df = df[df["country"].isin(paises)]

# ==================================================
# Layout Principal
# ==================================================
st.title("Visão de Negócio - Cidades")
st.divider()

st.subheader("Informações úteis para tomadas de decisão com base nas cidades")

st.plotly_chart(qnt_rest_cid(df), use_container_width=True)

st.divider()
col1, col2 = st.columns(2)
col1.plotly_chart(med_acima(df, 4.0, "Top 8 cidades com avaliações ≥ 4.0"), use_container_width=True)
col2.plotly_chart(med_acima(df, 2.5, "Top 8 cidades com avaliações ≥ 2.5"), use_container_width=True)

st.divider()
st.plotly_chart(faz_rev(df), use_container_width=True)

st.divider()
col1, col2 = st.columns(2)
col1.plotly_chart(qnt_ent(df), use_container_width=True)
col2.plotly_chart(ped_online(df), use_container_width=True)
