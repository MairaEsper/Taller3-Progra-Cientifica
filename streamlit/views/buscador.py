import streamlit as st
import pandas as pd
from api_client import api_post

def render(base_url: str):
    st.title("Buscador Semántico de Versículos")

    frase_input = st.text_input("Frase a buscar:")

    if st.button("Buscar Versículos", type="primary"):
        if not frase_input.strip():
            st.warning("Por favor, ingresa una frase válida antes de buscar.")
            return

        with st.spinner("Buscando coincidencia..."):
            body = {"frase": frase_input.strip()}
            
            resultados = api_post(base_url, "/buscador", body=body)

            if resultados is None:
                pass
            elif len(resultados) == 0:
                st.info("No se encontraron versículos similares para esa frase.")
            else:
                st.subheader("Resultados")
                
                tabla = []
                for resultado in resultados:
                    if " | Similitud:" in resultado:
                        partes = resultado.split(" | Similitud:")
                        texto = partes[0]
                        similitud= partes[1]

                        tabla.append({
                            "Versículo": texto,
                            "Similitud": similitud
                        })
                        
                    else:
                        st.write(resultado)
                
                df_resultados = pd.DataFrame(tabla)
                
                st.dataframe(df_resultados, use_container_width=True, hide_index=True)