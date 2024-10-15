import cv2
import os
from gtts import gTTS
import pygame
import tempfile
import threading
import time

# ----------- Métodos usados para el entrenamiento y lectura del modelo ----------
method = 'LBPH'
if method == 'LBPH':
    emotion_recognizer = cv2.face.LBPHFaceRecognizer_create()

emotion_recognizer.read('modelo' + method + '.xml')
# --------------------------------------------------------------------------------

dataPath = 'C:/Users/avrup/Asistente-Inteligente-para-el-reconocimiento-de-emociones-1/Emocion'
imagePaths = os.listdir(dataPath)
print('imagePaths=', imagePaths)

# Cargar imágenes para cada emoción
emotion_images = {
    'Felicidad': cv2.imread('imagenes/felicidad.jpg'),
    'Tristeza': cv2.imread('imagenes/tristeza.jpg'),
    'Enojo': cv2.imread('imagenes/enojo.png'),
    'Sorpresa': cv2.imread('imagenes/sorpresa.png')
}

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Función para hablar las recomendaciones (en un hilo separado)
def speak(text):
    temp_audio_file = None
    try:
        temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts = gTTS(text=text, lang='es')
        tts.save(temp_audio_file.name)
        temp_audio_file_path = temp_audio_file.name
        temp_audio_file.close()

        pygame.mixer.init()
        pygame.mixer.music.load(temp_audio_file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    finally:
        if temp_audio_file:
            try:
                os.unlink(temp_audio_file_path)
            except PermissionError:
                pass

# Función para obtener la recomendación hablada en función de la emoción detectada
def get_emotion_recommendation(emotion_label):
    recommendations = {
        'Felicidad': 'Me alegro mucho de que estés feliz, sigue disfrutando tu día.',
        'Tristeza': 'Busca siempre el equilibrio entre tus responsabilidades y tu bienestar personal.',
        'Enojo': 'Respira hondo y relájate, es importante mantener la calma. La ira puede provocar que hagas cosas de las que luego te arrepientas.',
        'Sorpresa': 'Tomate un momento para analizar  lo inesperado antes de tu accionar',
        
    }
    return recommendations.get(emotion_label, "Ya que cuento con las cuatro emociones básicas, actualmente no puedo procesar tu emoción.")

# Variable para almacenar la emoción previamente hablada
last_spoken_emotion = ""

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
        emotion = imagePaths[result[0]]

        cv2.putText(frame, '{}'.format(emotion), (x, y-25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Verificar si la emoción detectada es diferente de la última hablada
        if emotion != last_spoken_emotion:
            last_spoken_emotion = emotion  # Actualiza la última emoción hablada
            recommendation = get_emotion_recommendation(emotion)
            threading.Thread(target=speak, args=(recommendation,)).start()  # Lanza un hilo para hablar
        # Mostrar la imagen de la emoción encima de la leyenda y centrada
        if emotion in emotion_images:
            emotion_img = cv2.resize(emotion_images[emotion], (100, 100))  # Tamaño fijo para la imagen
            img_height, img_width, _ = emotion_img.shape

        # Calcular posición centrada de la imagen respecto a la cara detectada
        img_x = x + (w // 2) - (img_width // 2)  # Centrar en X
        img_y = y - img_height - 35  # Colocar encima de la leyenda (ajustar -35 si es necesario)

        # Verificar si la imagen se sale del frame superior
        if img_y < 0:
            img_y = 0

        # Mostrar la imagen en el frame
        frame[img_y:img_y + img_height, img_x:img_x + img_width] = emotion_img


    cv2.imshow('Ejecutando Análisis', frame)
    k = cv2.waitKey(1)
    if k == 27:  # Presiona ESC para salir
        break

cap.release()
cv2.destroyAllWindows()
