import streamlit as st
import os
from views import dashboard, buscador, generador, visualizador

st.set_page_config(page_title="Dashboard Biblia", layout="wide")

DEFAULT_API_URL = "http://127.0.0.1:8000"

st.title("Dashboard Principal")

dashboard.render(DEFAULT_API_URL)

buscador.render(DEFAULT_API_URL)

generador.render(DEFAULT_API_URL)

visualizador.render(DEFAULT_API_URL)
