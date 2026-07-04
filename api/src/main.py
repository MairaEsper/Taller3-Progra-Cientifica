from fastapi import FastAPI, Query, HTTPException, Request

from estructura.biblia import Biblia
from visualizador import Visualizador
from buscador import Buscador
from generador import Generador

app = FastAPI(
    title = "hola",
    description = "prueba"
)

biblia = Biblia()
ruta_dataset = '../data/t_asv.csv'
ruta_keys = '../data/key_english.csv'

try:
    biblia.cargar_datos(ruta_dataset, ruta_keys)
except Exception as e:
    print(f"Ocurrió un error al cargar los datos: {e}")

@app.post("/buscador")
async def versiculos_similares(request: Request):
    body = await request.json()
    buscador = Buscador(biblia)
    buscador.procesar_biblia()
    return buscador.buscar_frase(body["frase"], 5)

@app.post("/generador")
async def generar_versiculos(request: Request):
    body = await request.json()
    generador = Generador(biblia)
    generador.entrenar_modelos(n_maximo=4)
    versiculo_generado = generador.generar_versiculo(body["n"], body["palabra"])
    return versiculo_generado
