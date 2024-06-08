import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import speech_recognition as sr
import pyttsx3
import pywhatkit
import pygame
from keras.models import load_model
import wikipedia
import subprocess
import sys
import webbrowser
import datetime

lemmatizer = WordNetLemmatizer()

# Importamos los archivos generados en el código anterior
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')

listener = sr.Recognizer()
pygame.init()
engine = pyttsx3.init()

# Modulando la voz
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 178)
engine.setProperty('volume', 0.7)
sound3 = pygame.mixer.Sound("hello.wav")
sound4 = pygame.mixer.Sound("hello.wav")

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    print("Palabras clave detectadas:", sentence_words)
    return np.array(bag)

def predict_class(sentence, threshold=0.5):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    print("Salidas del modelo:", res)

    if np.max(res) > threshold:
        max_index = np.where(res == np.max(res))[0][0]
        category = classes[max_index]
        print("Categoría predicha:", category)
        return category
    else:
        print("No se detectó ninguna intención.")
        return None

def get_response(tag, intents_json):
    list_of_intents = intents_json['intents']
    
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i['responses'])
            break
    if not result:
        result = "Disculpa actualmente no puedo procesar tu peticion"

    return result

# Chatbot hablando
def talk(message, intent_tag=None):
    engine.say(message)
    engine.runAndWait()

    
def listen():
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            audio = listener.listen(source)
            try:
                user_input = listener.recognize_google(audio, language="es")
                print("Has dicho:", user_input)
                return user_input.lower() if user_input else None
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                return None
    except:
        return None
#abrir otro proceso de python
def abrir_script():
    try:
        subprocess.run(["python", "reconocimientoEmocion.py"])
    except FileNotFoundError:
        print("El archivo no fue encontrado.")
    except Exception as e:
        print("Error:", e)
    


# Lógica principal del chatbot
def Brain():
    sound3.play()
    talk("Hablame")
    while True:
        try:
            user_input = listen()
            if user_input is not None:
                found_response = False
                intent_tag = None
                for intent in intents['intents']:
                    patterns = intent.get('patterns', [])
                    responses = intent.get('responses', [])
                    for pattern in patterns:
                        if user_input.lower() in pattern.lower():
                            response = random.choice(responses)
                            intent_tag = intent["tag"]
                            talk(response, intent_tag)                    
                        if intent_tag == "Despedida":
                              sound3.play()
                              sys.exit()
                        if intent_tag == "escaneo":
                            abrir_script()
                            
                        break

        except KeyboardInterrupt:
            talk("Ups, lo lamento, algo salio mal en el procesamiento, intenta de nuevo mas tarde")
            break

if __name__ == '__main__':
    Brain()
