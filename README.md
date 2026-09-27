# 4S - AT - Desenvolvimento Front-End com Python (com Streamlit)

## Sobre o projeto
Esse é o repositório do Assessment (AT) de Desenvolvimento Front-End com Python. 
Eu criei um dashboard iterativo focado em dados reais de partidas de futebol, para investigar como os passes de uma equipe e de seus jogadores impactam na criação de chances de gols e na posse de bola. 

## (Bibliotecas)
- **Streamlit**: A base da aplicação para criar o dashboard web.
- **Statsbombpy**: Para consultar a API pública e puxar os dados dos campeonatos, partidas e eventos.
- **Mplsoccer**: Usei para desenhar os campos de futebol e plotar os mapas de passes e de chutes.
- **Matplotlib e Seaborn**: Para a criação de outros gráficos complementares.
- **Plotly**: Para os gráficos interativos (como o comparativo de jogadores).
- **Pandas**: Para manipular os dados de forma tabular.

## Como rodar o meu projeto

1. Primeiro, clone esse repositório:
```bash
git clone https://github.com/luiscjesus-infnet/4s_at-desenvolvimento_front-end_com_python_com_Streamlit.git
```
2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
# No Windows
.\venv\Scripts\activate
# No Linux/Mac
source venv/bin/activate
```
3. Instale as dependências que listei no arquivo:
```bash
pip install -r requirements.txt
```
4. Suba o Streamlit!
```bash
streamlit run app.py
```

## Acesse online!
Fiz o deploy no Streamlit Community Cloud. 
Você pode acessar o dashboard funcionando através desse link: 
[Link da Aplicação no Streamlit (https://github.com/luiscjesus-infnet/4s_at-desenvolvimento_front-end_com_python_com_Streamlit.git)]()
