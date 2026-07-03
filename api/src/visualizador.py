import pandas as pd

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