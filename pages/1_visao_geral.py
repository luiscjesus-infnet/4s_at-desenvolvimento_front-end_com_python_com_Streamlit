import streamlit as st
import sys
import os

# Pego o caminho da pasta raiz do projeto pra poder importar as minhas utils de forma certa.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import carregar_competicoes, carregar_partidas, converter_dataframe_csv

st.set_page_config(page_title="Visão Geral", page_icon="🏆", layout="wide")

st.title("🏆 Visão Geral dos Campeonatos")

# Mostrando informacoes enquanto carrega
with st.spinner("Carregando as competições lá do StatsBomb... aguarde!"):
    todas_competicoes = carregar_competicoes()

st.markdown("### Escolha o campeonato para análise:")

# Organizando em colunas pra ficar mais bonito
col1, col2 = st.columns(2)

with col1:
    # Faço uma lista com o nome do campeonato e a temporada para o dropdown
    opcoes_comp = todas_competicoes.apply(
        lambda linha: f"{linha['competition_name']} - {linha['season_name']}", axis=1
    )
    
    # Formulário interativo de seletor. 
    competicao_selecionada = st.selectbox("Qual campeonato você quer ver?", opcoes_comp)

# Descubro qual é a linha do dataframe que o usuário escolheu
idx_escolhido = opcoes_comp[opcoes_comp == competicao_selecionada].index[0]
id_comp = todas_competicoes.loc[idx_escolhido, 'competition_id']
id_temp = todas_competicoes.loc[idx_escolhido, 'season_id']
nome_comp = todas_competicoes.loc[idx_escolhido, 'competition_name']
nome_temp = todas_competicoes.loc[idx_escolhido, 'season_name']

# Salvo na sessão pra não perder quando mudar de tela
st.session_state['id_competicao_salvo'] = id_comp
st.session_state['id_temporada_salvo'] = id_temp
st.session_state['nome_competicao_salvo'] = nome_comp
st.session_state['nome_temporada_salvo'] = nome_temp

st.success(f"Você selecionou: **{nome_comp}** (Temporada: {nome_temp})")

st.markdown("---")
st.markdown("### 🏟️ Partidas disponíveis")

with st.spinner("Puxando as partidas desse campeonato..."):
    partidas = carregar_partidas(id_comp, id_temp)

if partidas.empty:
    st.warning("Não achei nenhuma partida pra esse campeonato. Escolha outro novamente acima!")
else:
    # Seleção da partida específica com dropdown
    lista_partidas = partidas.apply(
        lambda x: f"{x['match_date']} - {x['home_team']} vs {x['away_team']}", axis=1
    )
    
    partida_escolhida_texto = st.selectbox("E qual partida você quer analisar?", lista_partidas)
    idx_partida = lista_partidas[lista_partidas == partida_escolhida_texto].index[0]
    
    id_partida = partidas.loc[idx_partida, 'match_id']
    st.session_state['id_partida_salva'] = id_partida
    st.session_state['nome_partida_salva'] = f"{partidas.loc[idx_partida, 'home_team']} x {partidas.loc[idx_partida, 'away_team']}"

    st.write(f"Partida selecionada: **{st.session_state['nome_partida_salva']}**")
    
    # Mostro um dataframe das partidas 
    st.markdown("#### Lista completa das partidas pra analisar:")
    st.dataframe(partidas[['match_date', 'kick_off', 'home_team', 'home_score', 'away_team', 'away_score']], use_container_width=True)
    
    # Botão pra baixar os dados
    csv_partidas = converter_dataframe_csv(partidas)
    st.download_button(
        label="📥 Baixar lista de partidas (CSV)",
        data=csv_partidas,
        file_name=f"partidas_{nome_comp}_{nome_temp}.csv",
        mime="text/csv",
    )
    
    st.info("Após escolher vá na barra ao lado e clique em **Análise da Partida** pra ver os detalhes dessa partida que você escolheu!")
