import numpy as np

class Generador:
    def __init__(self, biblia):
        self.biblia = biblia
        self.tablas = {}
        
    def obtener_versiculos_limpios(self):
        versiculos_tokens = []
        libros = list(self.biblia.testamentos["OT"].libros.values()) + list(self.biblia.testamentos["NT"].libros.values())
                 
        for libro in libros:
            for capitulo in libro.capitulos.values():
                for versiculo in capitulo.versiculos:
                    texto = versiculo.texto_original.lower().replace(".", "").replace(",", "").replace('"', "")
                    palabras = ["<start>"] + texto.split() + ["<end>"]
                    versiculos_tokens.append(palabras)
        return versiculos_tokens

    def entrenar_modelos(self, n_maximo=4):
        versiculos = self.obtener_versiculos_limpios()
        
        for n in range(1, n_maximo + 1):
            self.tablas[n] = {}
            
            for palabras in versiculos:
                if n == 1:
                    for palabra in palabras:
                        contexto = ()

                        if contexto not in self.tablas[1]:
                            self.tablas[1][contexto] = {}

                        if palabra not in self.tablas[1][contexto]:
                            self.tablas[1][contexto][palabra] = 0
                            
                        self.tablas[1][contexto][palabra] += 1

                else:
                    cantidad_palabras = len(palabras)
                    limite = cantidad_palabras - n + 1

                    for i in range(limite):
                        inicio_ventana = i
                        fin_ventana = i + n
                        ventana = palabras[inicio_ventana : fin_ventana]

                        limite_contexto = n - 1
                        lista_contexto = ventana[0 : limite_contexto]
                        contexto = tuple(lista_contexto)

                        indice_ultima_palabra = n - 1
                        palabra_siguiente = ventana[indice_ultima_palabra]
                        
                        if contexto not in self.tablas[n]:
                            self.tablas[n][contexto] = {}

                        if palabra_siguiente not in self.tablas[n][contexto]:
                            self.tablas[n][contexto][palabra_siguiente] = 0

                        self.tablas[n][contexto][palabra_siguiente] += 1


    def generar_versiculo(self, n, palabra_inicial, max_palabras=30):
        if n not in self.tablas:
            return "Modelo no entrenado."
            
        resultado = [palabra_inicial.lower()]
        
        while len(resultado) < max_palabras:
            if n == 1:
                contexto = ()
                tabla_usar = 1
            else:
                tam_contexto = n - 1
                cantidad_actual = len(resultado)

                if cantidad_actual >= tam_contexto:
                    indice_inicio = cantidad_actual - tam_contexto
                    indice_fin = cantidad_actual
                    
                    lista_contexto = resultado[indice_inicio : indice_fin]
                    contexto = tuple(lista_contexto)
                    tabla_usar = n

                else:
                    contexto = tuple(resultado)
                    tabla_usar = cantidad_actual + 1

            if contexto in self.tablas[tabla_usar]:
                tabla_contexto = self.tablas[tabla_usar][contexto]
            else:
                tabla_contexto = None
            
            if tabla_contexto == None or "<end>" in resultado:
                if "<end>" not in resultado:
                    resultado.append("<end>")
                break
            
            palabras_candidatas = list(tabla_contexto.keys())
            conteos = list(tabla_contexto.values())

            total_conteos = sum(conteos)
            probabilidades = [c / total_conteos for c in conteos]
            
            palabra_elegida = np.random.choice(palabras_candidatas, p=probabilidades)
            resultado.append(palabra_elegida)
            
            if palabra_elegida == "<end>":
                break
        
        texto_final = " ".join(resultado)
        texto_final = texto_final.replace("<start>", "").replace("<end>", "").strip()

        return texto_final