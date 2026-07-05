import requests
import streamlit as st

REQUEST_TIMEOUT = 2000

def api_get(base_url: str, path: str, params: dict = None):
    try:
        response = requests.get(
            f"{base_url.rstrip('/')}{path}",
            params=params,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error de conexión con la API en {path}")
        return None
    
def api_post(base_url: str, path: str, body: dict):
    try:
        response = requests.post(
            f"{base_url.rstrip('/')}{path}",
            json=body,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error de conexión con la API en {path}")
        return None