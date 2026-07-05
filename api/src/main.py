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
    max_largo = body.get("max_palabras", 30)
    versiculo_generado = generador.generar_versiculo(body["n"], body["palabra"], max_palabras=max_largo)
    return versiculo_generado

@app.get("/top-frecuentes")
def top_5_frecuentes(
    testamento: str = Query(None, pattern="^(OT|NT)$"),
    libro: str = Query(None),
    capitulo: int = Query(None, ge=1),
):
    if testamento is None and libro is None and capitulo is None:
        frecuencias = biblia.frecuencias_globales
    else:
        frecuencias = {}

        if testamento is None or testamento == "OT":
            for libro_obj in biblia.testamentos["OT"].libros.values():
                if libro and libro_obj.nombre != libro:
                    continue

                for capitulo_obj in libro_obj.capitulos.values():
                    if capitulo is not None and capitulo_obj.numero != capitulo:
                        continue

                    for versiculo in capitulo_obj.versiculos:
                        for token in versiculo.tokens:
                            frecuencias[token] = frecuencias.get(token, 0) + 1

        if testamento is None or testamento == "NT":
            for libro_obj in biblia.testamentos["NT"].libros.values():
                if libro and libro_obj.nombre != libro:
                    continue

                for capitulo_obj in libro_obj.capitulos.values():
                    if capitulo is not None and capitulo_obj.numero != capitulo:
                        continue

                    for versiculo in capitulo_obj.versiculos:
                        for token in versiculo.tokens:
                            frecuencias[token] = frecuencias.get(token, 0) + 1

    top = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)[:5]
    return top

@app.get("/cantidad-versiculos-libro")
def cant_versiculos_libro(
    testamento: str = Query(None, pattern="^(OT|NT)$"),
    libro: str = Query(None),
    capitulo: int = Query(None, ge=1),
):
    visualizador = Visualizador(biblia)
    return visualizador.obtener_versiculos_por_libro(testamento=testamento, libro=libro, capitulo=capitulo)

@app.get("/longitud-promedio-versiculos")
def long_promedio_vers_libro(
    testamento: str = Query(None, pattern="^(OT|NT)$"),
    libro: str = Query(None),
    capitulo: int = Query(None, ge=1),
):
    visualizador = Visualizador(biblia)
    promedios = visualizador.obtener_promedio_longitud_versiculos(testamento=testamento, libro=libro, capitulo=capitulo)
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
def nube_palabras(
    top_n: int = Query(100, ge=10, le=500),
    testamento: str = Query(None, pattern="^(OT|NT)$"),
    libro: str = Query(None),
    capitulo: int = Query(None, ge=1),
):
    visualizador = Visualizador(biblia)
    return visualizador.obtener_nube_palabras(top_n=top_n, testamento=testamento, libro=libro, capitulo=capitulo)

@app.get("/filtros/testamentos")
def get_testamentos():
    return ["OT", "NT"]

@app.get("/filtros/libros")
def get_libros(testamento: str = Query(None, pattern="^(OT|NT)$")):
    libros_lista = []
    if testamento:
        if testamento in biblia.testamentos:
            libros_lista = [libro.nombre for libro in biblia.testamentos[testamento].libros.values()]
    else:
        for t in biblia.testamentos.values():
            libros_lista.extend([libro.nombre for libro in t.libros.values()])
    return sorted(libros_lista)

@app.get("/filtros/capitulos")
def get_capitulos(libro: str = Query(...)):
    for t in biblia.testamentos.values():
        for l in t.libros.values():
            if l.nombre == libro:
                return sorted(list(l.capitulos.keys()))
    raise HTTPException(status_code=404, detail="Libro no encontrado")