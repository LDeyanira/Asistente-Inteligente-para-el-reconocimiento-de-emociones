import cv2
import os
import subprocess
import speech_recognition as sr
import pyttsx3
import pygame
import threading

listener = sr.Recognizer()
pygame.init()
engine = pyttsx3.init()

# Configuración de voz
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 178)
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

# Métodos usados para el entrenamiento y lectura del modelo
method = 'LBPH'
if method == 'EigenFaces':
    emotion_recognizer = cv2.face.EigenFaceRecognizer_create()
if method == 'FisherFaces':
    emotion_recognizer = cv2.face.FisherFaceRecognizer_create()
if method == 'LBPH':
    emotion_recognizer = cv2.face.LBPHFaceRecognizer_create()

emotion_recognizer.read('modelo'+method+'.xml')

dataPath = 'MetodoEigenFaces_EmotionDetector/Emocion'
imagePaths = os.listdir(dataPath)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

# Función para abrir otro script en un hilo separado
def abrir_script2():
    try:
        subprocess.run(["python", "chatbot/chatbot2.py"])
    except FileNotFoundError:
        print("El archivo no fue encontrado.")
    except Exception as e:
        print("Error:", e)

# Función para mostrar recomendaciones basadas en la emoción detectada
# Función para mostrar recomendaciones basadas en la emoción detectada
def mostrar_recomendaciones(emocion):
    print("Emoción detectada:", emocion)  # Mensaje de depuración
    recomendaciones = {
        "Felicidad": "¡Sonrie y disfruta el momento!",
        "Tristeza": "Recuerda que siempre hay una razon para sonreir.",
        "enojado": "Intenta respirar profundamente y contar hasta 10 antes de reaccionar.",
        "Sorpresa" : "que te ha dejado asi."
    }
    if emocion in recomendaciones:
        print("Recomendación encontrada para", emocion)  # Mensaje de depuración
        return recomendaciones[emocion]
    else:
        print("No hay recomendaciones para", emocion)  # Mensaje de depuración
        return "No hay recomendaciones disponibles para esta emoción."



# Función para realizar el análisis de emociones en la cámara
def analizar_emociones():
    while True:
        ret, frame = cap.read()
        if ret == False: 
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = gray.copy()
        
        faces = faceClassif.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            rostro = auxFrame[y:y+h, x:x+w]
            rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
            result = emotion_recognizer.predict(rostro)
            
            detected_emotion = imagePaths[result[0]]
            cv2.putText(frame, '{}'.format(imagePaths[result[0]]), (x, y-25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            recomendacion = mostrar_recomendaciones(detected_emotion)
            cv2.putText(frame, recomendacion, (x, y+h+25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

        cv2.imshow('Ejecutando Analisis', frame)
        k = cv2.waitKey(1)
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# Función para ejecutar el reconocimiento de voz en un hilo separado
def ejecutar_reconocimiento_voz():
    while True:
        user_input = listen()
        if user_input is not None:
            for pattern, responses in pares:
                if user_input.lower() in pattern:
                    talk(responses[0])  
                    break
            #if user_input == "termina":
                #break

if __name__ == '__main__':
    hilo_emociones = threading.Thread(target=analizar_emociones)
    hilo_voz = threading.Thread(target=ejecutar_reconocimiento_voz)

    hilo_emociones.start()
    hilo_voz.start()

    hilo_emociones.join()
    hilo_voz.join()

    abrir_script2()
