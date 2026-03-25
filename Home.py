import streamlit as st
from PIL import Image

# ==================================================
# Configuração da Página
# ==================================================
st.set_page_config(
    page_title="Home | Zomato Restaurants",
    page_icon="🍽️",
    layout="wide"
)

# ==================================================
# Sidebar
# ==================================================
try:
    image = Image.open("fome_01.jpg")
    st.sidebar.image(image, width=150)
except FileNotFoundError:
    st.sidebar.warning("Imagem não encontrada")

st.sidebar.title("Zomato Restaurants")
st.sidebar.caption("For the love of Food")
st.sidebar.divider()
st.sidebar.caption("Powered by **Edon Gomes Leite**")

# ==================================================
# Conteúdo Principal
# ==================================================
st.title("🍴 Zomato Restaurants – Dashboard")
st.divider()

st.markdown(
    """
### 👋 Bem-vindo!

Este dashboard foi desenvolvido para o **acompanhamento de métricas estratégicas** da empresa **Zomato Restaurants**, 
com foco em **análise exploratória de dados** e **apoio à tomada de decisão**.

A análise está organizada em **5 visões principais**:
- 🌍 Geográfica  
- 🌎 Países  
- 🏙️ Cidades  
- 🏪 Restaurantes  
- 🍜 Culinárias  

---

### 🏢 Sobre a Zomato
A **Zomato** é uma plataforma de busca de restaurantes e serviços de delivery, fundada em **julho de 2008**.  
Atua em diversos países da **Ásia, Europa e Américas**, conectando clientes a restaurantes que atendem às suas preferências.

Além de facilitar a escolha do consumidor, a Zomato também é uma **vitrine estratégica** para empresas do setor gastronômico.

---

### 📊 Fonte dos Dados
Os dados utilizados neste projeto foram obtidos no **Kaggle** e são de acesso público:

🔗 https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset

> ⚠️ Observação: A Zomato atualmente atua em mais países e cidades do que os apresentados neste conjunto de dados.

---

### 🧭 Como utilizar este Dashboard?

#### 🌍 Visão Geográfica
- Análise geral e distribuição geográfica
- Mapa com a localização dos restaurantes por país

#### 🌎 Visão Países
- Quantidade de restaurantes por país  
- Quantidade de cidades por país  
- Média de avaliações  
- Preço médio para duas pessoas  
- Diversidade de culinárias  
- Restaurantes que aceitam reservas  

#### 🏙️ Visão Cidades
- Quantidade de restaurantes por cidade  
- Melhores restaurantes por avaliação  
- Restaurantes que aceitam reservas  
- Cidades com maior volume de entregas  
- Pedidos on-line por cidade  

#### 🏪 Visão Restaurantes
- Restaurantes mais bem avaliados  
- Top 10 restaurantes  
- Destaque para culinária brasileira  
- Impacto de delivery e reservas no preço médio  

#### 🍜 Visão Culinárias
- Avaliações dos principais tipos culinários  
- Culinárias mais caras  
- Culinárias com delivery  
- Melhores e piores culinárias  

---

### 📬 Contato do Desenvolvedor
- 💬 **Discord:** edon_leite  
- 💼 **LinkedIn:** https://www.linkedin.com/in/edonleite  
- 🧑‍💻 **GitHub:** https://github.com/edonleite  
"""
)
