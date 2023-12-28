import streamlit as st
from PIL import Image 

st.set_page_config(
    page_title = 'Home',
    page_icon = ':knife_fork_plate:')

image=Image.open('fome_01.jpg')
st.sidebar.image(image, width=150)

st.sidebar.title('Zomato Restaurants')
st.sidebar.subheader('For the love of Food')
st.sidebar.subheader('', divider='gray')
st.sidebar.subheader('Powered by: Edon Gomes Leite')

st.write('# Zomato Restaurants - Dashbord')

st.markdown(
    """
   Seja bem vindo ao Dashboard da empresa Zomato Restaurants, este dashboard foi construído para o acompanhamento 
   das métricas da empresa baseado em 4 visões importantes para o negócio:                      
   Geográfica, Países, Cidades e Culinárias.
   
   ### Sobre a Zomato:  
   A zomato é um serviço de busca de restaurantes e delivery, ela atua em diversos países da Ásia, Europa e alguns páises na américa,
   ela foi fundada em julho de 2008 com o intuito de ajudar os clientes a encontrarem restaurantes que atendessem suas necessidades, 
   se tornando um excelente lugar para empresas do segmento de restaurantes ficarem expostas para seus clientes, potencializando seus 
   resultados. 
   
   ### Fonte dos dados:
   Os dados utilizados no estudo e construção deste dashboard foram disponibilizados na plataforma Kaggle, sendo assim, os dados 
   ficaram publicos para qualquer pessoa utilizá-los em suas analises. O link para download dos arquivos é: 
   https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv.     
   É importante salientar que a empresa Zomato cresceu e hoje atua em mais países e cidades além das apresentadas aqui.
   
    ### Como utilizar esse Dashboard?
    
    - #### Visão Geográfica:
        - Informações úteis para análise geral e geográfica de negócio;
        - Mapa com a localização dos restaurantes por país.
                
    - #### Visão Países:
      - Quantidade de restaurantes registrados por país;
      - Quantidade de cidades registradas por país;
      - Média de avaliações feitas por país;
      - Média de preço de um prato para duas pessoas por país;
      - Quantidade de culinária distinta por país;
      - Restaurantes que aceitam reservas por país.
           
    - #### Visão Cidades: 
        - Quantidade de restaurantes registrados por cidades;
        - 8 Melhores restaurantes na média de avaliação acima 4.0;
        - 8 Melhores restaurantes na média de avaliação acima 2.5;
        - Melhores restaurantes por cidades que fazem reservas;
        - Cidades com maior quantidade de entregas;
        - Cidades com maior quantidade pedidos on-line.
        
     - #### Visão Restaurantes: 
        - Os melhores restaurantes;
        - Os 10 melhores restaurantes com maior avaliação;
        - Os 10 melhores restaurantes de culinária brasileira do Brasil com maior nota média;
        - Restaurantes que aceitam pedidos on-line tem maiores avaliações;
        - Restaurantes que aceitam reservas, possuem o maior valor médio de um prato para duas pessoas.
        
     - #### Visão Culinárias: 
        - Avaliações dos principais tipos culinários;
        - As 10 melhores culinárias com preço médio de um prato para duas pessoas;  
        - Tipos de culinárias que aceitam pedidos on-line e fazem entregas;
        - Os 10 melhores tipos de culinárias;
        - Os 10 piores tipos de culinárias.
        
    ### Contato do desenvolvedor:
    - Discord: edon_leite
    - Linkedin: www.linkedin.com/in/edonleite
    - GitHub: https://github.com/edonleite      
""")