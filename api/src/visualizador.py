import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from tfidf import TfIdf

class Visualizador:
    def __init__(self, biblia):
        self.biblia = biblia

    def obtener_versiculos_por_libro(self):
        datos = []

        for libro in self.biblia.testamentos["OT"].libros.values():
            total_versiculos = 0
            for capitulo in libro.capitulos.values():
                total_versiculos += len(capitulo.versiculos)
            
            datos.append((libro.nombre, total_versiculos))

        for libro in self.biblia.testamentos["NT"].libros.values():
            total_versiculos = 0
            for capitulo in libro.capitulos.values():
                total_versiculos += len(capitulo.versiculos)
            
            datos.append((libro.nombre, total_versiculos))

        df = pd.DataFrame(datos, columns=["Libro", "Cantidad"])

    
    def obtener_promedio_longitud_versiculos(self):
        libros = {}

        for libro in self.biblia.testamentos["OT"].libros.values():
            if libro.nombre not in libros:
                libros[libro.nombre] = {"palabras": 0, "versiculos": 0}

            for capitulo in libro.capitulos.values():
                for versiculo in capitulo.versiculos:
                    cant_palabras = len(versiculo.texto_original.split())
                    libros[libro.nombre]["palabras"] += cant_palabras
                    libros[libro.nombre]["versiculos"] += 1

        for libro in self.biblia.testamentos["NT"].libros.values():
            if libro.nombre not in libros:
                libros[libro.nombre] = {"palabras": 0, "versiculos": 0}

            for capitulo in libro.capitulos.values():
                for versiculo in capitulo.versiculos:
                    cant_palabras = len(versiculo.texto_original.split())
                    libros[libro.nombre]["palabras"] += cant_palabras
                    libros[libro.nombre]["versiculos"] += 1

        
        promedios = {}

        for nombre, cantidades in libros.items():
            promedios[nombre] = cantidades.get("palabras")/cantidades.get("versiculos")

        return promedios
    
    def obtener_pca_versiculos(self):
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

        vectores_tfidf = self.tfidf.calcular_tfidf(textos_versiculos)

        pca = PCA(n_components=2)
        matriz_tfidf = np.array(vectores_tfidf)
        coordenadas_2d = pca.fit_transform(matriz_tfidf)

        x_ot = []
        y_ot = []
        x_nt = []
        y_nt = []

        for i in range(len(etiquetas_testamento)):
            etiqueta = etiquetas_testamento[i]
    
            if etiqueta == "OT":
                x_ot.append(coordenadas_2d[i, 0])
                y_ot.append(coordenadas_2d[i, 1])
            else:
                x_nt.append(coordenadas_2d[i, 0])
                y_nt.append(coordenadas_2d[i, 1])