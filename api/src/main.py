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

@app.get("/top-frecuentes")
def top_5_frecuentes():
    top = sorted(biblia.frecuencias_globales.items(), key=lambda x: x[1], reverse=True)[:5]
    return top

@app.get("/cantidad-versiculos-libro")
def cant_versiculos_libro():
    visualizador = Visualizador(biblia)
    return visualizador.obtener_versiculos_por_libro()
    
@app.get("/longitud-promedio-versiculos")
def long_promedio_vers_libro():
    visualizador = Visualizador(biblia)
    promedios = visualizador.obtener_promedio_longitud_versiculos()
    return promedios

@app.get("/pca-versiculos")
def pca_versiculos(dimensiones: int = Query(2, ge=2, le=3)):
    visualizador = Visualizador(biblia)
    return visualizador.obtener_pca_versiculos(n_componentes=dimensiones)

@app.get("/word2vec-versiculos")
def word2vec_versiculos(dimensiones: int = Query(2, ge=2, le=3)):
    visualizador = Visualizador(biblia)
    return visualizador.obtener_word2vec_versiculos(n_componentes=dimensiones)

@app.get("/nube-palabras")
def nube_palabras(top_n: int = Query(100, ge=10, le=500)):
    visualizador = Visualizador(biblia)
    return visualizador.obtener_nube_palabras(top_n=top_n)