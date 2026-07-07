## Taller 3 Programación Científica

### Integrantes:
- Maira Cortés Araya - 21.324.438-8
- Francisco Plaza Pizarro - 20.007.355-K

## Instrucciones de ejecución:
### API
#### Creación y activación entorno virtual Python:
Dentro de carpeta /api hacer:
```
python -m venv venv
```
```
.\venv\Scripts\activate
```

#### Instalación de librerías:
```
pip install -r requirements.txt
```

#### Levantar API (FastAPI):
```
cd src
uvicorn main:app --reload
```
---
### Streamlit
#### Creación y activación entorno virtual Python:
Dentro de carpeta /streamlit hacer:
```
python -m venv venv
```
```
.\venv\Scripts\activate
```

#### Instalación de librerías:
```
pip install -r requirements.txt
```

#### Levantar Streamlit:
```
streamlit run main.py
```
