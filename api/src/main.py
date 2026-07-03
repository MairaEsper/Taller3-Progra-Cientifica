from estructura.biblia import Biblia

def main():    
    biblia = Biblia()
    ruta_dataset = '../data/t_asv.csv'
    ruta_keys = '../data/key_english.csv'
    
    try:
        biblia.cargar_datos(ruta_dataset, ruta_keys)
    except Exception as e:
        print(f"Ocurrió un error al cargar los datos: {e}")

if __name__ == "__main__":
    main()