import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

class Preprocesador:
    def __init__(self):
        self.stopwords = set(stopwords.words('english'))

    def procesar_texto(self, texto):
        texto = texto.lower()
        texto = re.sub(r'[^a-z\s]', '', texto)
        tokens = texto.split()
        tokens_limpios = [palabra for palabra in tokens if palabra not in self.stopwords]
        
        return tokens_limpios