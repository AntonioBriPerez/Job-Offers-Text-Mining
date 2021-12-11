from sklearn.feature_extraction.text import CountVectorizer
import re
import pandas as pd
from nltk.corpus import stopwords
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import numpy as np
from nltk.tokenize import word_tokenize
import os

def limpiar_tokenizar(texto):
    '''
    Esta función limpia y tokeniza el texto en palabras individuales.
    El orden en el que se va limpiando el texto no es arbitrario.
    El listado de signos de puntuación se ha obtenido de: print(string.punctuation)
    y re.escape(string.punctuation)
    '''
    
    # Se convierte todo el texto a minúsculas
    nuevo_texto = texto.lower()
    # Eliminación de páginas web (palabras que empiezan por "http")
    nuevo_texto = re.sub('http\S+', ' ', nuevo_texto)
    # Eliminación de signos de puntuación
    regex = '[\\!\\"\\#\\$\\%\\&\\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\=\\>\\?\\@\\[\\\\\\]\\^_\\`\\{\\|\\}\\~]'
    nuevo_texto = re.sub(regex , ' ', nuevo_texto)
    # Eliminación de números
    nuevo_texto = re.sub("\d+", ' ', nuevo_texto)
    # Eliminación de espacios en blanco múltiples
    nuevo_texto = re.sub("\\s+", ' ', nuevo_texto)
    # Tokenización por palabras individuales
    nuevo_texto = nuevo_texto.split(sep = ' ')
    # Eliminación de tokens con una longitud < 2
    nuevo_texto = [token for token in nuevo_texto if len(token) > 1]
    
    return(nuevo_texto)

def get_text_from_file(file):
    with open(file, 'r', encoding='utf-8') as input_file:
        return input_file.read()

def main():
    text = limpiar_tokenizar(get_text_from_file('data_eng_corpus.txt'))
    text_without_sw= [word for word in text if not word in stopwords.words()]
    
    key_word = get_text_from_file('DataEngineer_KeyWords.txt')
    key_word_list = list(map(lambda x: x.lower(), list(key_word.split('\n'))))

    text_without_sw = list(filter(lambda x: x in key_word_list, text_without_sw))
    print(text_without_sw)

    job_df = pd.DataFrame(text_without_sw, columns=['job_description'])
    job_df = job_df['job_description'].value_counts()
    base_filename = 'Values.txt'
    with open(os.path.join('.', base_filename),'w') as outfile:
        job_df.to_string(outfile)
        

if __name__ == "__main__":
    main()

