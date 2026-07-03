from estructura.biblia import Biblia
from visualizador import Visualizador
from buscador import Buscador
from generador import Generador

def main():    
    biblia = Biblia()
    ruta_dataset = '../data/t_asv.csv'
    ruta_keys = '../data/key_english.csv'
    
    try:
        biblia.cargar_datos(ruta_dataset, ruta_keys)
    except Exception as e:
        print(f"Ocurrió un error al cargar los datos: {e}")

    visualizador = Visualizador(biblia)
    promedios = visualizador.obtener_promedio_longitud_versiculos()

    for nombre, promedio in promedios.items():
        print(f'{nombre}: {promedio}')
        
    print(f"Palabras únicas: {len(biblia.vocabulario)}")
    top = sorted(biblia.frecuencias_globales.items(), key=lambda x: x[1], reverse=True)[:5]
    print("Las 5 palabras más frecuentes:")
    for palabra, frec in top:
        print(f" - {palabra}: {frec}")
    
    buscador = Buscador(biblia)
    frase_buscar = input("Ingrese la frase que desea buscar: ")
    buscador.procesar_biblia()
    buscador.buscar_frase(frase_buscar, 5)
    
    generador = Generador(biblia)
    generador.entrenar_modelos(n_maximo=4)
    palabra = input("Ingresa una palabra inicial (ej. 'the', 'god', 'jesus'): ")
    try:
        n = int(input("Ingresa el valor de N para el modelo (1-4): "))
        if 1 <= n <= 4:
            versiculo_generado = generador.generar_versiculo(n, palabra)
            print(f"Texto generado (N={n}):")
            print(f"   {versiculo_generado.capitalize()}")
        else:
            print("Error: El valor de N debe estar entre 1 y 4.")
    except ValueError:
        print("Error: Debes ingresar un número entero.")

if __name__ == "__main__":
    main()