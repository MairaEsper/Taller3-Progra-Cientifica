import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from api_client import api_get

def render(base_url: str):
    st.sidebar.header("Filtros")

    testamentos_api = api_get(base_url, "/filtros/testamentos") or []
    testamento_seleccionado = st.sidebar.selectbox("Testamento", ["Todos"] + testamentos_api)
    testamento_param = None if testamento_seleccionado == "Todos" else testamento_seleccionado

    libro_param = None
    if testamento_param:
        params_libros = {"testamento": testamento_param} if testamento_param else {}
        libros_api = api_get(base_url, "/filtros/libros", params=params_libros) or []
        
        libro_seleccionado = st.sidebar.selectbox("Libro", ["Todos"] + libros_api)
        libro_param = None if libro_seleccionado == "Todos" else libro_seleccionado

    capitulo_param = None
    if libro_param:
        capitulos_api = api_get(base_url, "/filtros/capitulos", params={"libro": libro_param}) or []
        opciones_capitulo = ["Todos"] + [str(c) for c in capitulos_api]
        capitulo_seleccionado = st.sidebar.selectbox("Capítulo", opciones_capitulo)
        capitulo_param = None if capitulo_seleccionado == "Todos" else int(capitulo_seleccionado)

    if st.button("Cargar Datos", type="primary"):
        filtros_api = {}
        if testamento_param: filtros_api["testamento"] = testamento_param
        if libro_param: filtros_api["libro"] = libro_param
        if capitulo_param: filtros_api["capitulo"] = capitulo_param

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Top Palabras Más Frecuentes")
            with st.spinner("Cargando frecuencias..."):
                data_top = api_get(base_url, "/top-frecuentes", params=filtros_api)
                
                if data_top:
                    df_top = pd.DataFrame(data_top, columns=["Palabra", "Frecuencia"])
                    st.dataframe(df_top, use_container_width=True, hide_index=True)
                else:
                    st.warning("No hay datos para estos filtros.")

        with col2:
            pass
            
        st.divider()
