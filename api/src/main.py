from estructura.biblia import Biblia
from visualizador import Visualizador

def main():    
    biblia = Biblia()
    ruta_dataset = '../data/t_asv.csv'
    ruta_keys = '../data/key_english.csv'
    
    try:
        biblia.cargar_datos(ruta_dataset, ruta_keys)
    except Exception as e:
        print(f"Ocurrió un error al cargar los datos: {e}")

    visualizador = Visualizador(biblia)
    promedios = visualizador.obtener_distribucion_longitud_versiculos()

    for nombre, promedio in promedios.items():
        print(f'{nombre}: {promedio}')

if __name__ == "__main__":
    main()