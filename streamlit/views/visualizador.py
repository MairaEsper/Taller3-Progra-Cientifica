import streamlit as st
import pandas as pd
import plotly.express as px
from api_client import api_get

def render(base_url: str):
    st.title("Visualizador de PCA y Word2Vec")

    col1, col2 = st.columns(2)
    
    with col1:
        modelo_seleccionado = st.radio(
            "Selecciona el modelo:",
            ("PCA (TF-IDF)", "Word2Vec + PCA")
        )
        
    with col2:
        dimensiones = st.radio(
            "Selecciona las dimensiones:",
            (2, 3),
            format_func=lambda x: f"{x}D"
        )


    if modelo_seleccionado == "PCA (TF-IDF)":
        endpoint = "/pca-versiculos"
    else:
        endpoint = "/word2vec-versiculos"

    params = {"dimensiones": dimensiones}

    with st.spinner("Cargando..."):
        data = api_get(base_url, endpoint, params=params)

        if not data or "puntos" not in data:
            st.error("No se pudieron cargar los datos de la API.")
            return

        df_puntos = pd.DataFrame(data["puntos"])
        varianza = data.get("varianza", 0)

        st.metric(label="Varianza", value=f"{varianza}%")
        
        if dimensiones == 2:
            fig = px.scatter(
                df_puntos, 
                x="x", 
                y="y", 
                color="testamento",
                title=f"Proyección 2D - {modelo_seleccionado}",
                hover_data=df_puntos.columns
            )
            
        else:
            fig = px.scatter_3d(
                df_puntos, 
                x="x", 
                y="y", 
                z="z", 
                color="testamento",
                title=f"Proyección 3D - {modelo_seleccionado}",
                hover_data=df_puntos.columns
            )
            fig.update_layout(height=700)

        st.plotly_chart(fig, width='stretch')