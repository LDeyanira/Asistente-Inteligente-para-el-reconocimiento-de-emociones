import cv2
import os
import numpy as np

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

dataPath = 'C:/Users/Deyanira LS/Documents/Asistant/MetodoEigenFaces_EmotionDetector/Emocion' # Cambia a la ruta donde hayas almacenado Data
imagePaths = os.listdir(dataPath)
print('imagePaths=', imagePaths)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    if ret == False:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = gray.copy()

    nFrame = cv2.hconcat([frame, np.zeros((480, 300, 3), dtype=np.uint8)])

    faces = faceClassif.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        rostro = auxFrame[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
        result = emotion_recognizer.predict(rostro)

        cv2.putText(frame, '{}'.format(result), (x, y-5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)

        # EigenFaces método (actualmente comentado)
         if method == 'EigenFaces':
             if result[1] < 5700:
                 cv2.putText(frame, '{}'.format(imagePaths[result[0]]), (x, y-25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                 cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                 image = emotionImage(imagePaths[result[0]])
            
             else:
                 cv2.putText(frame, 'Emocion no identificada', (x, y-20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                 cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                 

        # FisherFaces método (actualmente comentado)
         if method == 'FisherFaces':
            if result[1] < 500:
                 cv2.putText(frame, '{}'.format(imagePaths[result[0]]), (x, y-25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                 cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                 image = emotionImage(imagePaths[result[0]])
                 nFrame = cv2.hconcat([frame, image])
             else:
                 cv2.putText(frame, 'Emocion no identificada', (x, y-20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                 cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                 nFrame = cv2.hconcat([frame, np.zeros((480, 300, 3), dtype=np.uint8)])

        # LBPHFace método
        if method == 'LBPH':
            if result[1] < 60:
                cv2.putText(frame, '{}'.format(imagePaths[result[0]]), (x, y-25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                 image = emotionImage(imagePaths[result[0]])  # No está siendo utilizada, comentada temporalmente
                # nFrame = cv2.hconcat([frame, image])
            else:
                cv2.putText(frame, 'Emocion no identificada', (x, y-20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                nFrame = cv2.hconcat([frame, np.zeros((480, 300, 3), dtype=np.uint8)])

    cv2.imshow('nFrame', nFrame)
    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
