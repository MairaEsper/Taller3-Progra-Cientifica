class Testamento:
    def __init__(self, nombre):
        self.nombre = nombre
        self.libros = {}

    def agregar_libro(self, libro):
        self.libros[libro.id_libro] = libro