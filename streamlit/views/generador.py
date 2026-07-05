import streamlit as st
from api_client import api_post

def render(base_url: str):
    st.title("Generador de Versículos")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        opciones = {"Unigrama": 1, "Bigrama": 2, "Trigrama": 3, "Cuatrigrama": 4}
        seleccion = st.selectbox("Modelo", list(opciones.keys()))
        n = opciones[seleccion]

    with col2:
        palabra = st.text_input("Palabra inicial")
        
    with col3:
        max_palabras = st.number_input("Largo máximo", min_value=5, max_value=100, value=30, step=5)

    if st.button("Generar Texto", type="primary"):
        if not palabra.strip():
            st.warning("Ingresa una palabra inicial.")
            return

        with st.spinner(f"Cargando..."):
            body = {
                "n": n,
                "palabra": palabra.strip(),
                "max_palabras": max_palabras
            }

            resultado = api_post(base_url, "/generador", body=body)

            if resultado:
                st.info(f'"{resultado}"')
            else:
                st.error("No se pudo generar el texto.")