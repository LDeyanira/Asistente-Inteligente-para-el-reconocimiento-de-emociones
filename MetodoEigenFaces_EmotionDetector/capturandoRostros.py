import cv2
import os
import imutils

#emotionName = 'Enojo'
#emotionName = 'Felicidad'
#emotionName = 'Sorpresa'
emotionName = 'Tristeza'

<<<<<<< HEAD
dataPath = 'MetodoEigenFaces_EmotionDetector/Emocion'
=======
dataPath = 'C:/Users/Deyanira LS/Documents/Asistant/MetodoEigenFaces_EmotionDetector/Emocion' #Cambia a la ruta donde hayas almacenado Data
>>>>>>> 8712dad4832f45960c75a8dc4ae808722a58b5fa
emotionsPath = dataPath + '/' + emotionName

if not os.path.exists(emotionsPath):
	print('Carpeta creada: ',emotionsPath)
	os.makedirs(emotionsPath)

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
#url = "http://192.168.1.19:4747/video"  # Reemplaza con la URL de tu cámara IP
#cap = cv2.VideoCapture(url)
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
count = 0

while True:

	ret, frame = cap.read()
	if ret == False: break
	frame =  imutils.resize(frame, width=640)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	auxFrame = frame.copy()

	faces = faceClassif.detectMultiScale(gray,1.3,5)

	for (x,y,w,h) in faces:
		cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
		rostro = auxFrame[y:y+h,x:x+w]
		rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
		cv2.imwrite(emotionsPath + '/rotro_{}.jpg'.format(count),rostro)
		count = count + 1
	cv2.imshow('frame',frame)

	k =  cv2.waitKey(1)
<<<<<<< HEAD
	if k == 27 or count >= 25:
=======
	if k == 27 or count >= 200:
>>>>>>> 8712dad4832f45960c75a8dc4ae808722a58b5fa
		break

cap.release()
cv2.destroyAllWindows()