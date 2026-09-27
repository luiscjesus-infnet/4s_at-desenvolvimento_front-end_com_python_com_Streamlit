import streamlit as st
import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer import Pitch
import pandas as pd

# Arrumando o caminho de novo
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import carregar_eventos_partida, converter_dataframe_csv

st.set_page_config(page_title="Análise da Partida", page_icon="📊", layout="wide")

# Verifico se o usuário já escolheu uma partida na primeira página
if st.session_state.get('id_partida_salva') is None:
    st.error("Opa! Você esqueceu de escolher uma partida. Volte na página 'Visão Geral' e selecione uma!")
    st.stop()

id_partida = st.session_state['id_partida_salva']
nome_partida = st.session_state['nome_partida_salva']
nome_comp = st.session_state['nome_competicao_salvo']
nome_temp = st.session_state['nome_temporada_salvo']

st.title(f"Análise da Partida: {nome_partida}")
st.markdown(f"**Competição:** {nome_comp} | **Temporada:** {nome_temp}")

# Pegando os eventos (e uso barra de progresso)
progresso = st.progress(0)
with st.spinner("Analisando todos os lances da partida..."):
    eventos = carregar_eventos_partida(id_partida)
    progresso.progress(100)
    
if eventos.empty:
    st.warning("Não existe eventos detalhados pra essa partida na base.")
    st.stop()

# Criei abas pra organizar melhor a tela
aba_resumo, aba_passes, aba_chutes = st.tabs(["Resumo e Métricas", "Análise de Passes", "Análise de Chutes (Mapa)"])

# Separando os times
time_casa = eventos['team'].iloc[0]
time_fora = eventos['team'].unique()[1] if len(eventos['team'].unique()) > 1 else "Outro"

with aba_resumo:
    st.subheader("Indicadores da Partida")
    
    # Calculando as métricas pra usar no st.metric
    total_passes = len(eventos[eventos['type'] == 'Pass'])
    total_chutes = len(eventos[eventos['type'] == 'Shot'])
    gols = len(eventos[(eventos['type'] == 'Shot') & (eventos['shot_outcome'] == 'Goal')])
    
    col1, col2, col3 = st.columns(3)
    # Mostrando os números na tela com st.metric
    col1.metric("Gols na Partida", gols)
    col2.metric("Total de Passes", total_passes)
    # Taxa de conversão: se não teve chute, é zero.
    taxa_conversao = (gols / total_chutes * 100) if total_chutes > 0 else 0
    col3.metric("Conversão de Chutes em Gol (%)", f"{taxa_conversao:.1f}%")

    st.markdown("### Tabela de Eventos (Pura e bruta!)")
    
    # Filtro usando radio buttons pra deixar interativo
    tipo_evento = st.radio("Selecione o tipo de evento que você quer ver na tabela:", 
                           ["Todos", "Passes", "Chutes", "Desarmes"])
    
    eventos_tabela = eventos.copy()
    if tipo_evento == "Passes":
        eventos_tabela = eventos_tabela[eventos_tabela['type'] == 'Pass']
    elif tipo_evento == "Chutes":
        eventos_tabela = eventos_tabela[eventos_tabela['type'] == 'Shot']
    elif tipo_evento == "Desarmes":
        eventos_tabela = eventos_tabela[eventos_tabela['type'] == 'Duel'] 

    # Colunas mais importantes
    colunas_mostrar = ['minute', 'second', 'team', 'player', 'type']
    st.dataframe(eventos_tabela[colunas_mostrar].dropna(), use_container_width=True)
    
    st.download_button("Baixar Eventos Filtrados (CSV)", data=converter_dataframe_csv(eventos_tabela), file_name="eventos_filtrados.csv", mime="text/csv")


with aba_passes:
    st.subheader("(Mapa de Passes)")
    
    time_selecionado = st.selectbox("Escolha de qual time você quer ver os passes:", [time_casa, time_fora])
    
    # Pego só os passes do time escolhido
    passes = eventos[(eventos['type'] == 'Pass') & (eventos['team'] == time_selecionado)].copy()
    
    # Tratamento das coordenadas pra usar no mplsoccer
    if not passes.empty and 'location' in passes.columns and 'pass_end_location' in passes.columns:
        passes = passes.dropna(subset=['location', 'pass_end_location'])
        passes['x'] = passes['location'].apply(lambda loc: loc[0])
        passes['y'] = passes['location'].apply(lambda loc: loc[1])
        passes['end_x'] = passes['pass_end_location'].apply(lambda loc: loc[0])
        passes['end_y'] = passes['pass_end_location'].apply(lambda loc: loc[1])
        
        # Desenho o campinho de futebol com o Mplsoccer
        pitch = Pitch(pitch_type='statsbomb', pitch_color='#aabb97', line_color='white')
        fig, ax = pitch.draw(figsize=(8, 4))
        
        # Desenho as linhas de passe
        pitch.lines(passes.x, passes.y, passes.end_x, passes.end_y,
                    lw=2, transparent=True, comet=True, ax=ax, color='#1f77b4', alpha=0.5)
        
        # Botar os (pontos) onde o passe começou
        pitch.scatter(passes.x, passes.y, s=20, ax=ax, color='white', edgecolors='black', zorder=2)
        
        plt.title(f"Mapa de Passes - {time_selecionado}", fontsize=15)
        st.pyplot(fig)
    else:
        st.write("Sem dados de passes suficientes pra desenhar o mapa pra esse time.")
        
    # Visualização com Matplotlib/Seaborn (relação estatística)
    st.markdown("### Quem mais passou a bola?")
    top_passadores = passes['player'].value_counts().head(10).reset_index()
    top_passadores.columns = ['Jogador', 'Número de Passes']
    
    if not top_passadores.empty:
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        sns.barplot(data=top_passadores, x='Número de Passes', y='Jogador', palette='viridis', ax=ax2)
        plt.title("Top 10 Passadores")
        st.pyplot(fig2)

with aba_chutes:
    st.subheader("Análise de chutes (Mapa de Chutes)")
    
    chutes = eventos[eventos['type'] == 'Shot'].copy()
    
    if not chutes.empty and 'location' in chutes.columns:
        chutes = chutes.dropna(subset=['location'])
        chutes['x'] = chutes['location'].apply(lambda loc: loc[0])
        chutes['y'] = chutes['location'].apply(lambda loc: loc[1])
        
        pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
        fig3, ax3 = pitch.draw(figsize=(8, 4))
        
        # Vou colorir diferente o que foi gol e o que não foi
        gols_df = chutes[chutes['shot_outcome'] == 'Goal']
        outros_df = chutes[chutes['shot_outcome'] != 'Goal']
        
        # Desenho os chutes que não foram gols
        pitch.scatter(outros_df.x, outros_df.y, s=100, ax=ax3, c='red', alpha=0.6, edgecolors='black', label='Errou')
        # Desenho os gols
        pitch.scatter(gols_df.x, gols_df.y, s=150, ax=ax3, c='yellow', marker='*', edgecolors='black', label='Gol!')
        
        ax3.legend(loc='lower left')
        plt.title("Mapa de Chutes da Partida", color='white', fontsize=15)
        st.pyplot(fig3)
    else:
        st.write("Sem chutes cadastrados pra essa partida :(")
