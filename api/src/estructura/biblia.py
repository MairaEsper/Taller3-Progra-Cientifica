import pandas as pd

from estructura.testamento import Testamento
from estructura.libro import Libro
from estructura.capitulo import Capitulo
from estructura.versiculo import Versiculo
from preprocesador import Preprocesador

class Biblia:
    def __init__(self):
        self.testamentos = {
            "OT": Testamento("OT"),
            "NT": Testamento("NT")
        }

        self.preprocesador = Preprocesador()
        self.frecuencias_globales = {}  
        self.vocabulario = set() 

    def cargar_datos(self, ruta_dataset, ruta_keys):
        df_texto = pd.read_csv(ruta_dataset)
        df_keys = pd.read_csv(ruta_keys)

        num_filas_texto = df_texto.shape[0]
        num_filas_keys = df_keys.shape[0]

        for i in range(num_filas_keys):
            fila = df_keys.iloc[i]

            id_libro = int(fila["b"])
            nombre = str(fila["n"])
            testamento = str(fila["t"]) 
            genero_id = int(fila["g"])

            libro = Libro(id_libro, nombre, testamento, genero_id)
            self.testamentos[testamento].agregar_libro(libro)
        
        for i in range(num_filas_texto):
            fila = df_texto.iloc[i]

            id = int(fila["id"])
            id_libro = int(fila["b"])
            num_capitulo = int(fila["c"])
            num_versiculo = int(fila["v"])
            texto = str(fila["t"])

            if id_libro in self.testamentos["OT"].libros:
                libro_actual = self.testamentos["OT"].libros[id_libro]
            elif id_libro in self.testamentos["NT"].libros:
                libro_actual = self.testamentos["NT"].libros[id_libro]
            else:
                continue

            if num_capitulo not in libro_actual.capitulos:
                libro_actual.agregar_capitulo(Capitulo(num_capitulo))
            
            capitulo_actual = libro_actual.capitulos[num_capitulo]

            nuevo_versiculo = Versiculo(id, num_versiculo, texto)
            tokens_limpios = self.preprocesador.procesar_texto(texto)
            nuevo_versiculo.tokens = tokens_limpios

            for token in tokens_limpios:
                self.frecuencias_globales[token] = self.frecuencias_globales.get(token, 0) + 1

            capitulo_actual.agregar_versiculo(nuevo_versiculo)

        self.vocabulario = set(self.frecuencias_globales.keys())
