import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from gensim.models import Word2Vec
from tfidf import TfIdf

class Visualizador:
    def __init__(self, biblia):
        self.biblia = biblia
        self.tfidf = TfIdf()

    def obtener_versiculos_por_libro(self, testamento=None, libro=None, capitulo=None):
        datos = []

        if testamento is None or testamento == "OT":
            for libro_obj in self.biblia.testamentos["OT"].libros.values():
                if libro and libro_obj.nombre != libro:
                    continue

                total_versiculos = 0
                for capitulo_obj in libro_obj.capitulos.values():
                    if capitulo is not None and capitulo_obj.numero != capitulo:
                        continue
                    total_versiculos += len(capitulo_obj.versiculos)

                datos.append((libro_obj.nombre, total_versiculos))

        if testamento is None or testamento == "NT":
            for libro_obj in self.biblia.testamentos["NT"].libros.values():
                if libro and libro_obj.nombre != libro:
                    continue

                total_versiculos = 0
                for capitulo_obj in libro_obj.capitulos.values():
                    if capitulo is not None and capitulo_obj.numero != capitulo:
                        continue
                    total_versiculos += len(capitulo_obj.versiculos)

                datos.append((libro_obj.nombre, total_versiculos))

        df = pd.DataFrame(datos, columns=["Libro", "Cantidad"])
        return df.to_dict(orient="records")

    def obtener_promedio_longitud_versiculos(self, testamento=None, libro=None, capitulo=None):
        libros = {}

        if testamento is None or testamento == "OT":
            for libro_obj in self.biblia.testamentos["OT"].libros.values():
                if libro and libro_obj.nombre != libro:
                    continue

                for capitulo_obj in libro_obj.capitulos.values():
                    if capitulo is not None and capitulo_obj.numero != capitulo:
                        continue

                    for versiculo in capitulo_obj.versiculos:
                        if libro_obj.nombre not in libros:
                            libros[libro_obj.nombre] = {"palabras": 0, "versiculos": 0}

                        cant_palabras = len(versiculo.texto_original.split())
                        libros[libro_obj.nombre]["palabras"] += cant_palabras
                        libros[libro_obj.nombre]["versiculos"] += 1

        if testamento is None or testamento == "NT":
            for libro_obj in self.biblia.testamentos["NT"].libros.values():
                if libro and libro_obj.nombre != libro:
                    continue

                for capitulo_obj in libro_obj.capitulos.values():
                    if capitulo is not None and capitulo_obj.numero != capitulo:
                        continue

                    for versiculo in capitulo_obj.versiculos:
                        if libro_obj.nombre not in libros:
                            libros[libro_obj.nombre] = {"palabras": 0, "versiculos": 0}

                        cant_palabras = len(versiculo.texto_original.split())
                        libros[libro_obj.nombre]["palabras"] += cant_palabras
                        libros[libro_obj.nombre]["versiculos"] += 1


        promedios = {}

        for nombre, cantidades in libros.items():
            promedios[nombre] = round(cantidades.get("palabras")/cantidades.get("versiculos"),2)

        return promedios

    def obtener_nube_palabras(self, top_n=100, testamento=None, libro=None, capitulo=None):
        if testamento is None and libro is None and capitulo is None:
            frecuencias = self.biblia.frecuencias_globales
        else:
            frecuencias = {}

            if testamento is None or testamento == "OT":
                for libro_obj in self.biblia.testamentos["OT"].libros.values():
                    if libro and libro_obj.nombre != libro:
                        continue

                    for capitulo_obj in libro_obj.capitulos.values():
                        if capitulo is not None and capitulo_obj.numero != capitulo:
                            continue

                        for versiculo in capitulo_obj.versiculos:
                            for token in versiculo.tokens:
                                frecuencias[token] = frecuencias.get(token, 0) + 1

            if testamento is None or testamento == "NT":
                for libro_obj in self.biblia.testamentos["NT"].libros.values():
                    if libro and libro_obj.nombre != libro:
                        continue

                    for capitulo_obj in libro_obj.capitulos.values():
                        if capitulo is not None and capitulo_obj.numero != capitulo:
                            continue

                        for versiculo in capitulo_obj.versiculos:
                            for token in versiculo.tokens:
                                frecuencias[token] = frecuencias.get(token, 0) + 1

        frecuencias_ordenadas = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True,)[:top_n]

        return [{"palabra": palabra, "frecuencia": frecuencia} for palabra, frecuencia in frecuencias_ordenadas]

    def _obtener_corpus_versiculos(self):
        textos_versiculos = []
        etiquetas_testamento = []

        for nombre_testamento, testamento in self.biblia.testamentos.items():
            for libro in testamento.libros.values():
                for capitulo in libro.capitulos.values():
                    for versiculo in capitulo.versiculos:
                        if len(versiculo.tokens) > 0:
                            palabras = versiculo.tokens
                        else:
                            texto_limpio = versiculo.texto_original.lower().replace(".", "").replace(",", "").replace('"', "")
                            palabras = texto_limpio.split()
                        if len(palabras) > 0:
                            textos_versiculos.append(palabras)
                            etiquetas_testamento.append(nombre_testamento)

        return textos_versiculos, etiquetas_testamento

    def coordenadas_a_puntos(self, coordenadas, etiquetas_testamento, n_componentes):
        puntos = []

        for i, etiqueta in enumerate(etiquetas_testamento):
            punto = {
                "testamento": etiqueta,
                "x": round(float(coordenadas[i, 0]), 2),
                "y": round(float(coordenadas[i, 1]), 2),
            }
            if n_componentes == 3:
                punto["z"] = round(float(coordenadas[i, 2]), 2)

            puntos.append(punto)

        return puntos

    def obtener_pca_versiculos(self, n_componentes=2):
        textos_versiculos, etiquetas_testamento = self._obtener_corpus_versiculos()

        vectores_tfidf = self.tfidf.calcular_tfidf(textos_versiculos)
        matriz_tfidf = np.array(vectores_tfidf)

        pca = PCA(n_components=n_componentes)
        coordenadas = pca.fit_transform(matriz_tfidf)

        return {
            "puntos": self.coordenadas_a_puntos(coordenadas, etiquetas_testamento, n_componentes),
            "varianza": round(sum(pca.explained_variance_ratio_.tolist()) * 100, 2),
        }

    def obtener_word2vec_versiculos(self, n_componentes=2, vector_size=100, window=5, min_count=1):
        textos_versiculos, etiquetas_testamento = self._obtener_corpus_versiculos()

        modelo = Word2Vec(
            sentences=textos_versiculos,
            vector_size=vector_size,
            window=window,
            min_count=min_count,
            workers=1,
            seed=42,
        )

        vectores_documentos = []
        etiquetas_validas = []

        for palabras, etiqueta in zip(textos_versiculos, etiquetas_testamento):
            vectores_palabras = [modelo.wv[palabra] for palabra in palabras if palabra in modelo.wv]
            if len(vectores_palabras) > 0:
                vectores_documentos.append(np.mean(vectores_palabras, axis=0))
                etiquetas_validas.append(etiqueta)

        array = np.array(vectores_documentos)

        pca = PCA(n_components=n_componentes)
        coordenadas = pca.fit_transform(array)

        return {
            "puntos": self.coordenadas_a_puntos(coordenadas, etiquetas_validas, n_componentes),
            "varianza": round(sum(pca.explained_variance_ratio_.tolist()) * 100, 2),
        }
