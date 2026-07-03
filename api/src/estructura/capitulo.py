class Capitulo:
    def __init__(self, numero):
        self.numero = numero
        self.versiculos = []            

    def agregar_versiculo(self, versiculo):
        self.versiculos.append(versiculo)