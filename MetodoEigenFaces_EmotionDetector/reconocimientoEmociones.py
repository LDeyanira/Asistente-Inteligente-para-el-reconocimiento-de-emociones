import cv2
import os
import subprocess
import speech_recognition as sr
import pyttsx3
import pygame
from nltk.chat.util import Chat, reflections
import sys

listener = sr.Recognizer()
pygame.init()
engine = pyttsx3.init()

#configuracion de voz
engine = pyttsx3.init()


voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine. setProperty('rate', 178)
engine.setProperty('volume', 0.7)

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

pares = [
    ["termina", ["terminando"]]
]
    

# ----------- Métodos usados para el entrenamiento y lectura del modelo ----------
method = 'LBPH'
if method == 'EigenFaces':
    emotion_recognizer = cv2.face.EigenFaceRecognizer_create()
if method == 'FisherFaces':
    emotion_recognizer = cv2.face.FisherFaceRecognizer_create()
if method == 'LBPH':
    emotion_recognizer = cv2.face.LBPHFaceRecognizer_create()

emotion_recognizer.read('modelo'+method+'.xml')
# --------------------------------------------------------------------------------

dataPath = 'MetodoEigenFaces_EmotionDetector/Emocion'
imagePaths = os.listdir(dataPath)
print('imagePaths=', imagePaths)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
####################################################################################################
#abrir otro proceso de python
def abrir_script2():
    try:
        subprocess.run(["python", "chatbot/chatbot2.py"])
    except FileNotFoundError:
        print("El archivo no fue encontrado.")
    except Exception as e:
        print("Error:", e)

#################################################################################
while True:
    ret, frame = cap.read()
    if ret == False: break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = gray.copy()
    
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        rostro = auxFrame[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
        result = emotion_recognizer.predict(rostro)
        
        detected_emotion = imagePaths[result[0]]
        #cv2.putText(frame, '{}'.format(detected_emotion), (x, y-25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, '{}'.format(imagePaths[result[0]]), (x, y-25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # Síntesis de voz
        #engine.say("Tu emoción es {}".format(detected_emotion))
        #engine.runAndWait()
        

    cv2.imshow('Ejecutando Analisis', frame)
    k = cv2.waitKey(1)
    if k == 27:
        break
    # Comprobando si se dijo "termina"
    #user_input = listen()
    #if user_input is not None:
       # for pattern, responses in pares:
           # if user_input.lower() in pattern:
               # talk(responses[0])  
                #sys.exit()
  
cap.release()
cv2.destroyAllWindows()
abrir_script2()