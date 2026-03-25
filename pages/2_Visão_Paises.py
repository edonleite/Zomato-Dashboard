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
    page_title="Visão Países",
    page_icon="🌍",
    layout="wide"
)

# ==================================================
# Funções de Apoio
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
    cols = df.columns
    cols = [inflection.titleize(col) for col in cols]
    cols = [col.replace(" ", "") for col in cols]
    cols = [inflection.underscore(col) for col in cols]
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
def aceit_resev(df):
    df = (
        df[df["has_table_booking"] == 1]
        .groupby("country")["restaurant_id"]
        .nunique()
        .reset_index()
    )

    fig = px.pie(
        df,
        values="restaurant_id",
        names="country",
        hole=0.4,
        title="Restaurantes que aceitam reservas"
    )
    fig.update_traces(textfont_size=12)
    return fig


def cul_dist_aceit_resv(df):
    df = (
        df.groupby("country")["cuisines"]
        .nunique()
        .reset_index()
    )

    fig = px.sunburst(
        df,
        path=["country"],
        values="cuisines",
        color="cuisines",
        color_continuous_scale="Rainbow",
        title="Quantidade de culinárias distintas por país"
    )
    return fig


def prato_dois(df):
    df = (
        df.groupby(["country", "currency"])["average_cost_for_two"]
        .mean()
        .round(2)
        .reset_index()
        .sort_values("average_cost_for_two", ascending=False)
    )

    fig = px.bar(
        df,
        x="country",
        y="average_cost_for_two",
        color="currency",
        text_auto=True,
        title="Preço médio de um prato para duas pessoas"
    )
    return fig


def med_aval_pais(df):
    df = df.groupby("country")["votes"].sum().reset_index()

    fig = px.scatter(
        df,
        x="country",
        y="votes",
        size="votes",
        color="country",
        text="votes",
        title="Total de avaliações por país"
    )
    return fig


def qnt_rest_pais(df):
    df = (
        df.groupby("country")["restaurant_id"]
        .nunique()
        .reset_index()
        .sort_values("restaurant_id", ascending=False)
    )

    fig = px.bar(
        df,
        x="country",
        y="restaurant_id",
        text_auto=True,
        title="Quantidade de restaurantes por país"
    )
    return fig


def qnt_city_pais(df):
    df = (
        df.groupby("country")["city"]
        .nunique()
        .reset_index()
        .sort_values("city", ascending=False)
    )

    fig = px.bar(
        df,
        x="country",
        y="city",
        text_auto=True,
        title="Quantidade de cidades por país"
    )
    return fig


# ==================================================
# Carregamento dos Dados
# ==================================================
df_raw = load_data()
df = clean_data(df_raw)

# ==================================================
# Sidebar
# ==================================================
try:
    image = Image.open("fome_03.jpg")
    st.sidebar.image(image, width=150)
except:
    st.sidebar.warning("Imagem não encontrada")

st.sidebar.title("Zomato Restaurants")
st.sidebar.subheader("For the love of Food")
st.sidebar.divider()

paises = st.sidebar.multiselect(
    "Selecione os países:",
    sorted(df["country"].unique()),
    default=[
        "Australia",
        "Brazil",
        "Canada",
        "England",
        "India",
        "Indonesia",
        "South Africa",
        "United States of America",
    ],
)

if st.sidebar.button("🔄 Atualizar dados"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.divider()
st.sidebar.caption("Powered by Edon Gomes Leite")

# ==================================================
# Filtro
# ==================================================
df = df[df["country"].isin(paises)]

# ==================================================
# Layout Principal
# ==================================================
st.title("Visão de Negócio - Países")
st.divider()

st.subheader("Informações úteis para tomadas de decisão de negócio")

col1, col2 = st.columns(2)
col1.plotly_chart(qnt_city_pais(df), use_container_width=True)
col2.plotly_chart(qnt_rest_pais(df), use_container_width=True)

st.divider()
st.plotly_chart(med_aval_pais(df), use_container_width=True)

st.divider()
st.plotly_chart(prato_dois(df), use_container_width=True)

st.divider()
col1, col2 = st.columns(2)
col1.plotly_chart(cul_dist_aceit_resv(df), use_container_width=True)
col2.plotly_chart(aceit_resev(df), use_container_width=True)
