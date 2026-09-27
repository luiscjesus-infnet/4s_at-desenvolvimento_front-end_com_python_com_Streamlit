import streamlit as st

# Configuro a página principal do meu dashboard. 
# Deixei o layout no modo amplo (wide) pra aproveitar melhor a tela (Catei e colei alguns ícones na internet pra ficar mais bonito).
st.set_page_config(
    page_title="Meu Dashboard de Futebol ⚽",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Guardo algumas coisas na sessão pro usuário não perder as escolhas 
# do filtro quando ficar navegando entre as páginas.
if 'id_competicao_salvo' not in st.session_state:
    st.session_state['id_competicao_salvo'] = None
if 'id_temporada_salvo' not in st.session_state:
    st.session_state['id_temporada_salvo'] = None
if 'id_partida_salva' not in st.session_state:
    st.session_state['id_partida_salva'] = None

st.title("⚽ Analytics do Futebol - Projeto de AT")
st.markdown("""
Esse é o meu trabalho de Assessment (AT) da disciplina de Desenvolvimento Front-End com Python.
A ideia é analisar dados de partidas de futebol usando a API do **StatsBomb**.

### Qual a minha pergunta de pesquisa?
Eu quero entender **como os passes de uma equipe e de seus jogadores impactam na criação de chances de gols e na posse de bola em uma partida específica.**

Pra navegar no projeto, use a barra lateral na esquerda!
Tem páginas pra ver os dados gerais, analisar a partida a fundo e comparar jogadores.
""")

# Como foi pedido em aula, usei "imagens, áudios, vídeos, animações ou emojis", 
# resolvi colocar uma imagem pra dar visual bonito na página inicial.
st.image(
    "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?q=80&w=1000&auto=format&fit=crop", 
    caption="Análise Tática de Futebol", 
    use_container_width=True
)
