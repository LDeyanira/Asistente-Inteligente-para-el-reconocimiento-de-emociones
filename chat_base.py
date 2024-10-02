import random
import io
import streamlit as st
import json
import pickle
import numpy as np
import requests
from tensorflow.keras.models import load_model
import subprocess
import re


# Función para descargar archivos desde URLs
def download_file(url, local_filename):
    response = requests.get(url)
    response.raise_for_status()
    with open(local_filename, 'wb') as f:
        f.write(response.content)

# URLs de los archivos
intents_url = 'https://github.com/LDeyanira/Asistente-Inteligente-para-el-reconocimiento-de-emociones/blob/641799bb1f48b12d6951acd477c2f691b52a7f02/intents.json'
words_url = 'https://github.com/LDeyanira/Asistente-Inteligente-para-el-reconocimiento-de-emociones/blob/641799bb1f48b12d6951acd477c2f691b52a7f02/words.pkl'
classes_url = 'https://github.com/LDeyanira/Asistente-Inteligente-para-el-reconocimiento-de-emociones/blob/641799bb1f48b12d6951acd477c2f691b52a7f02/classes.pkl'
model_url = 'https://github.com/LDeyanira/Asistente-Inteligente-para-el-reconocimiento-de-emociones/blob/641799bb1f48b12d6951acd477c2f691b52a7f02/chatbot_model.h5'

# Descargar archivos
download_file(intents_url, 'intents.json')
download_file(words_url, 'words.pkl')
download_file(classes_url, 'classes.pkl')
download_file(model_url, 'chatbot_model.h5')

# Cargar archivos locales
with open('intents.json') as f:
    intents = json.load(f)
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')  # Cargar el modelo de la ruta

# Función que tokeniza usando expresiones regulares en lugar de NLTK
def clean_up_sentence(sentence):
    sentence_words = re.findall(r'\b\w+\b', sentence.lower())
    return sentence_words

# Convertimos la información a unos y ceros según si están presentes en los patrones
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

# Predecimos la categoría a la que pertenece la oración
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    max_index = np.where(res == np.max(res))[0][0]
    category = classes[max_index]
    return category
# Abrir otro proceso de Python
def abrir_script():
    script_path = "C:/Users/Deyanira LS/Desktop/Asistente-Inteligente-para-el-reconocimiento-de-emociones/reconocimientoEmociones.py"
    try:
        result = subprocess.run(
            ["python", script_path],
            capture_output=True, text=True, check=True
        )
        return result.stdout, result.stderr
    except FileNotFoundError:
        return "El archivo no fue encontrado.", ""
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr
    except Exception as e:
        return "", str(e)


# Predecimos la categoría a la que pertenece la oración
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    max_index = np.where(res == np.max(res))[0][0]
    category = classes[max_index]
    return category

# Obtenemos una respuesta aleatoria
def get_response(tag, intents_json):
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i['responses'])
            break
    
    if tag == "analisis":
        abrir_script()
    
    return result