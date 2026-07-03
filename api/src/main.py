from estructura.biblia import Biblia
from visualizador import Visualizador
from buscador import Buscador

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

if __name__ == "__main__":
    main()