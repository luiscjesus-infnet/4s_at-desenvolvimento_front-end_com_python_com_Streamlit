import streamlit as st
from statsbombpy import sb
import pandas as pd

# Eu criei essas funções aqui pra não misturar com o código das telas.
# Como foi ensinado nos vídeos de aula, modularizei o código pra ficar mais fácil de ler e manter.

@st.cache_data
def carregar_competicoes():
    """
    Vou buscar todas as competições que têm na API pública do Statsbomb.
    Uso o cache do streamlit (st.cache_data) para não ficar baixando toda hora
    e deixar o site mais rápido.
    """
    tabela = sb.competitions()
    return tabela

@st.cache_data
def carregar_partidas(id_competicao, id_temporada):
    """
    Pego a lista de partidas de um campeonato e temporada específica.
    """
    tabela = sb.matches(competition_id=id_competicao, season_id=id_temporada)
    return tabela

@st.cache_data
def carregar_eventos_partida(id_partida):
    """
    Carrego todos os eventos de uma única partida.
    """
    tabela = sb.events(match_id=id_partida)
    return tabela

def converter_dataframe_csv(tabela):
    """
    Transformo o meu dataframe em um CSV pra conseguir baixar depois.
    """
    return tabela.to_csv(index=False).encode('utf-8')
