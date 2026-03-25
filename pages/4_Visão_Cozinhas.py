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
    page_title="Visão Culinária",
    page_icon="🍲",
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
# Funções de Análise
# ==================================================
def melhores_culinarias(df, top_n, asc=False):
    df = (
        df.groupby("cuisines")["aggregate_rating"]
        .mean()
        .reset_index()
        .sort_values("aggregate_rating", ascending=asc)
        .head(top_n)
    )

    fig = px.bar(
        df,
        x="cuisines",
        y="aggregate_rating",
        color="cuisines",
        text_auto=True,
        labels={
            "cuisines": "Tipos de Culinária",
            "aggregate_rating": "Média de Avaliação",
        },
    )
    return fig


def culinarias_com_entrega(df):
    df = (
        df[(df["has_online_delivery"] == 1) & (df["is_delivering_now"] == 1)]
        .groupby("cuisines")["restaurant_id"]
        .nunique()
        .reset_index()
        .sort_values("restaurant_id", ascending=False)
    )
    return df


def culinarias_mais_caras(df, top_n):
    df = (
        df.groupby(["cuisines", "currency"])["average_cost_for_two"]
        .mean()
        .reset_index()
        .sort_values("average_cost_for_two", ascending=False)
        .head(top_n)
    )
    return df


def top_restaurantes_por_culinaria(df, culinaria):
    df = (
        df[df["cuisines"] == culinaria]
        .sort_values("aggregate_rating", ascending=False)
        .head(1)
    )
    return df.iloc[0] if not df.empty else None


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
        "England",
        "India",
        "South Africa",
        "United States of America",
    ],
)

qtde_cul = st.sidebar.slider("Quantidade de culinárias:", 1, 30, 10)

culinarias = st.sidebar.multiselect(
    "Selecione as culinárias:",
    sorted(df["cuisines"].unique()),
    default=[
        "Italian",
        "American",
        "Arabian",
        "Japanese",
        "Brazilian",
    ],
)

if st.sidebar.button("🔄 Atualizar dados"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.divider()
st.sidebar.caption("Powered by Edon Gomes Leite")

# ==================================================
# Filtros
# ==================================================
df = df[df["country"].isin(paises)]
df = df[df["cuisines"].isin(culinarias)]

# ==================================================
# Layout Principal
# ==================================================
st.markdown("## Visão de Negócio – Culinária")
st.divider()

st.subheader("⭐ Destaque por tipo de culinária")

cols = st.columns(len(culinarias))
for col, cul in zip(cols, culinarias):
    with col:
        info = top_restaurantes_por_culinaria(df, cul)
        if info is not None:
            st.metric(
                label=cul,
                value=f"{info['aggregate_rating']}/5.0",
                help=f"""
                Restaurante: {info['restaurant_name']}
                País: {info['country']}
                Cidade: {info['city']}
                Preço (2 pessoas): {info['currency']} {info['average_cost_for_two']}
                """,
            )

st.divider()
st.subheader("💰 Culinárias com maior custo médio")
st.dataframe(culinarias_mais_caras(df, qtde_cul), use_container_width=True)

st.divider()
st.subheader("🚴 Culinárias com pedidos online e entrega")
st.dataframe(culinarias_com_entrega(df), use_container_width=True)

st.divider()
st.subheader("🏆 Melhores culinárias por avaliação")
st.plotly_chart(melhores_culinarias(df, qtde_cul, asc=False), use_container_width=True)

st.divider()
st.subheader("⚠️ Piores culinárias por avaliação")
st.plotly_chart(melhores_culinarias(df, qtde_cul, asc=True), use_container_width=True)
