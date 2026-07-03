class Libro:
    def __init__(self, id_libro, nombre, testamento, genero_id):
        self.id_libro = id_libro
        self.nombre = nombre
        self.testamento = testamento
        self.genero_id = genero_id
        
        self.capitulos = {}             

    def agregar_capitulo(self, capitulo):
        self.capitulos[capitulo.numero] = capitulo