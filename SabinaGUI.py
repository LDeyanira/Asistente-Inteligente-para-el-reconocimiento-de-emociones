import speech_recognition as sr
import pyttsx3, pywhatkit
import datetime
import wikipedia
import subprocess
import webbrowser
from tkinter import *
from PIL import Image,ImageTk
import pygame
pygame.init()
sound = pygame.mixer.Sound("hello.wav")
main_window=Tk()
main_window.title("SABINA")
main_window.geometry("400x500")
main_window.resizable(0,0)
main_window.configure(background="black")

#label_title=Label(main_window,text="Sabina AI",bg="white",fg="yellow",font=('Arial',30,'bold'))
#label_title.pack(pady=10)
sabina_photo=ImageTk.PhotoImage(Image.open("sabina.jpg"))
window_photo=Label(main_window,image=sabina_photo)
window_photo.pack(pady=5)

name = "Sabina"
flag=1
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine. setProperty('rate', 178)
engine.setProperty('volume', 0.7)
# for i in voices:
#     print(i)


def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            
            talk("Te escucho")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc)
            rec = rec.lower()
            print("Dijiste:", rec) 
            if name in rec:
                rec = rec.replace(name, '')

    except:
        pass
    return rec

def run_Sabina():
    while True:
        try:
            rec = listen()
        except UnboundLocalError:
            talk("No te entendí, intenta de nuevo...")
            continue
        if 'reproduce' in rec:
            music = rec.replace('reproduce','')
        
            talk("Reproduciendo")
            pywhatkit.playonyt(music)
        elif 'hora' in rec:
            hora = datetime.datetime.now().strftime('%I:%M %p')
            talk("Son las " + hora)
        elif 'busca' in rec:
            order = rec.replace('busca', '')
            wikipedia.set_lang("es")
            info = wikipedia.summary(order, 1)
            talk(info)
        elif 'despierta mente' in rec:
         talk("claro...")
         main_window.iconify()  # Minimiza la ventana principal
         subprocess.run(["python", "Brain.py"])
         
        elif 'analisa me' in  rec:
         talk('Activando detector de emociones')
         subprocess.run(["python", r'C:\Users\Deyanira LS\Documents\Asistant\MetodoEigenFaces_EmotionDetector\reconocimientoEmociones.py'])
        elif 'termina' in rec:
            flag=0
            talk("Hasta luego")
            return 0
    
button_listen=Button(main_window,text="Escuchar",fg="white",bg="gray",font=("Arial",10,"bold"),width=20,height=3,command=run_Sabina)
button_listen.pack(pady=10)
main_window.mainloop()
#if __name__ == '__main__':
    #run_Sabina()