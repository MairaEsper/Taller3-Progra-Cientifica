from tfidf import TfIdf

class Buscador:
    def __init__(self, biblia):
        self.biblia = biblia
        self.tfidf = TfIdf()
        
        self.corpus_versiculos = [] 
        self.referencias = [] 
        
    def procesar_biblia(self):
        libros = list(self.biblia.testamentos["OT"].libros.values()) + list(self.biblia.testamentos["NT"].libros.values())
                 
        for libro in libros:
            for capitulo in libro.capitulos.values():
                for versiculo in capitulo.versiculos:
                    texto_limpio = versiculo.texto_original.lower().replace(".", "").replace(",", "").replace('"', "")
                    
                    self.corpus_versiculos.append(texto_limpio.split())
                    self.referencias.append((libro.nombre, capitulo.numero, versiculo.numero, versiculo.texto_original))
        

    def buscar_frase(self, frase, k):
        frase_limpia = frase.lower().replace(".", "").replace(",", "").replace('"', "").split()
        
        corpus_temporal = self.corpus_versiculos + [frase_limpia]
        
        vectores_completos = self.tfidf.calcular_tfidf(corpus_temporal)
        
        vector_frase = vectores_completos[-1]
        vectores_biblia = vectores_completos[:-1]
        
        resultados = []
        for i, vector_versiculo in enumerate(vectores_biblia):
            similitud = self.tfidf.similitud_coseno(vector_frase, vector_versiculo)
            
            if similitud > 0:
                resultados.append((similitud, self.referencias[i]))
                
        resultados.sort(key=lambda x: x[0], reverse=True)
        
        print(f"\n--- RESULTADOS ---")
        if not resultados:
            print("No se encontraron coincidencias.")
            return

        for i in range(min(k, len(resultados))):
            similitud = resultados[i][0]
            refs = resultados[i][1]

            libro = refs[0]
            cap = refs[1]
            ver = refs[2]
            texto = refs[3]
            
            print(f"{i+1}. {texto} {libro} {cap}:{ver} | Similitud: {similitud}")