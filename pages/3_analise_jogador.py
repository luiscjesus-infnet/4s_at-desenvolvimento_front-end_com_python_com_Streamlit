import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import carregar_eventos_partida

st.set_page_config(page_title="Análise de Jogadores", page_icon="🏃", layout="wide")

if st.session_state.get('id_partida_salva') is None:
    st.error("Volte na página 'Visão Geral' e seleciona uma partida antes!")
    st.stop()

id_partida = st.session_state['id_partida_salva']
nome_partida = st.session_state['nome_partida_salva']

st.title(f"🏃 Análise de Jogadores: {nome_partida}")

with st.spinner("Puxando os dados dos jogadores..."):
    eventos = carregar_eventos_partida(id_partida)

if eventos.empty:
    st.warning("Sem dados suficientes.")
    st.stop()

st.markdown("### Selecione os jogadores que você quer analisar ou comparar:")

# Pego só quem é jogador mesmo, porque tem evento que é do time e não do jogador
jogadores_disponiveis = eventos['player'].dropna().unique()
jogadores_disponiveis = sorted(jogadores_disponiveis)

# Formulário interativo: comparo dois jogadores
col1, col2 = st.columns(2)
with col1:
    jogador_1 = st.selectbox("Selecione o primeiro jogador:", jogadores_disponiveis)
with col2:
    jogador_2 = st.selectbox("Selecione o segundo jogador (pra comparar):", jogadores_disponiveis)

# Faço um filtro só com os eventos desses dois caras
eventos_j1 = eventos[eventos['player'] == jogador_1]
eventos_j2 = eventos[eventos['player'] == jogador_2]

# Agrupando algumas estatísticas pra jogar no gráfico de radar ou barra
def estatisticas_jogador(df_jogador):
    passes = len(df_jogador[df_jogador['type'] == 'Pass'])
    chutes = len(df_jogador[df_jogador['type'] == 'Shot'])
    desarmes = len(df_jogador[df_jogador['type'] == 'Duel'])
    faltas = len(df_jogador[df_jogador['type'] == 'Foul Committed'])
    
    return {
        'Passes': passes,
        'Chutes': chutes,
        'Desarmes': desarmes,
        'Faltas': faltas
    }

stats_j1 = estatisticas_jogador(eventos_j1)
stats_j2 = estatisticas_jogador(eventos_j2)

df_comparacao = pd.DataFrame([
    {'Jogador': jogador_1, 'Métrica': 'Passes', 'Valor': stats_j1['Passes']},
    {'Jogador': jogador_1, 'Métrica': 'Chutes', 'Valor': stats_j1['Chutes']},
    {'Jogador': jogador_1, 'Métrica': 'Desarmes', 'Valor': stats_j1['Desarmes']},
    {'Jogador': jogador_1, 'Métrica': 'Faltas', 'Valor': stats_j1['Faltas']},
    {'Jogador': jogador_2, 'Métrica': 'Passes', 'Valor': stats_j2['Passes']},
    {'Jogador': jogador_2, 'Métrica': 'Chutes', 'Valor': stats_j2['Chutes']},
    {'Jogador': jogador_2, 'Métrica': 'Desarmes', 'Valor': stats_j2['Desarmes']},
    {'Jogador': jogador_2, 'Métrica': 'Faltas', 'Valor': stats_j2['Faltas']},
])

st.markdown("#### Comparação de Desempenho")
# Criei um gráfico de barras com Plotly pra realizar o requisito de usar Plotly na rubrica
fig_plotly = px.bar(
    df_comparacao, 
    x='Métrica', 
    y='Valor', 
    color='Jogador', 
    barmode='group',
    title="Comparativo de Ações na Partida"
)
st.plotly_chart(fig_plotly, use_container_width=True)

st.markdown("---")
st.markdown("### JSON com os metadados do jogador 1")
st.write("Vou usar o comando Magic ou st.write/st.json pra jogar uns metadados brutões na tela (no formato JSON).")

# Pegando a primeira linha de passe do jogador 1 só pra mostrar os metadados
um_passe_j1 = eventos_j1[eventos_j1['type'] == 'Pass'].head(1)
if not um_passe_j1.empty:
    st.json(um_passe_j1.to_dict(orient='records')[0])
else:
    st.write("Esse jogador não deu nenhum passe :(")
