import numpy as np
import math

class TfIdf:
    def similitud_coseno(self, vector_a, vector_b):
        producto_punto = np.dot(vector_a, vector_b)
        magnitud_a = np.sqrt(np.sum(vector_a**2))
        magnitud_b = np.sqrt(np.sum(vector_b**2))
        
        if magnitud_a == 0 or magnitud_b == 0:
            return 0.0
        return producto_punto / (magnitud_a * magnitud_b)

    def calcular_tfidf(self, corpus):
        frecuencias_documento = {}
        
        for palabras_doc in corpus:
            for palabra in set(palabras_doc):
                frecuencias_documento[palabra] = frecuencias_documento.get(palabra, 0) + 1
                
        vocabulario = list(frecuencias_documento.keys())
        total_docs = len(corpus)
        
        idf = {}
        for palabra, df in frecuencias_documento.items():
            idf[palabra] = math.log10(total_docs / df)
            
        vectores_tfidf = []
        for palabras_doc in corpus:
            total_palabras = len(palabras_doc)
            
            conteo_tf = {}
            for palabra in palabras_doc:
                conteo_tf[palabra] = conteo_tf.get(palabra, 0) + 1
            
            vector_doc = np.zeros(len(vocabulario))
            for i, palabra in enumerate(vocabulario):
                if palabra in conteo_tf:
                    tf = conteo_tf[palabra] / total_palabras
                    vector_doc[i] = tf * idf[palabra]
                    
            vectores_tfidf.append(vector_doc)
            
        return vectores_tfidf