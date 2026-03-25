# ==================================================
# Bibliotecas Necessárias
# ==================================================
import pandas as pd
import inflection
import folium
import streamlit as st
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from PIL import Image

# ==================================================
# Configuração da Página
# ==================================================
st.set_page_config(
    page_title="Visão Geográfica",
    page_icon="🌎",
    layout="wide"
)

# ==================================================
# Funções
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
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"


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


def mapa(df):
    df_map = df[
        [
            "restaurant_name",
            "average_cost_for_two",
            "currency",
            "longitude",
            "latitude",
            "aggregate_rating",
            "color_rating_name",
        ]
    ].drop_duplicates()

    mapa = folium.Map(zoom_start=2)
    marker_cluster = MarkerCluster().add_to(mapa)

    for _, row in df_map.iterrows():
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=f"""
            <b>{row['restaurant_name']}</b><br>
            Custo médio: {row['average_cost_for_two']} {row['currency']}<br>
            Avaliação: {row['aggregate_rating']}
            """,
            icon=folium.Icon(color=row["color_rating_name"], icon="home"),
        ).add_to(marker_cluster)

    folium_static(mapa, width=1100, height=450)


# ==================================================
# Carregamento e Limpeza dos Dados
# ==================================================
df_raw = load_data()
df = clean_data(df_raw)

# ==================================================
# Barra Lateral
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
        "England",
        "India",
        "South Africa",
        "United States of America",
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
st.title("Visão de Negócio - Geográfica")
st.divider()

st.subheader("Informações úteis para análise geral e geográfica de negócio")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Restaurantes", df["restaurant_id"].nunique())
col2.metric("Países", df["country"].nunique())
col3.metric("Cidades", df["city"].nunique())
col4.metric("Avaliações", df["votes"].sum())
col5.metric("Culinárias", df["cuisines"].nunique())

st.divider()
st.subheader("📍 Mapa com a localização dos restaurantes")
mapa(df)
