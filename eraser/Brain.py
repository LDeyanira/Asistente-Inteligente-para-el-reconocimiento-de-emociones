import nltk
import pyttsx3
import pygame
import time
from nltk.chat.util import Chat, reflections
import speech_recognition as sr
import subprocess
from tkinter import *
from PIL import Image,ImageTk

main_window=Tk()
main_window.title("SABINA SABIUS MODE ")
main_window.geometry("400x250")
main_window.resizable(0,0)
main_window.configure(background="black")

#label_title=Label(main_window,text="Sabina AI",bg="white",fg="yellow",font=('Arial',30,'bold'))
#label_title.pack(pady=10)
sabina_photo=ImageTk.PhotoImage(Image.open("sabinasabio.jpg"))
window_photo=Label(main_window,image=sabina_photo)
window_photo.pack(pady=5)

listener = sr.Recognizer()
nltk.download('punkt')
pygame.init()
sound = pygame.mixer.Sound("risa.wav")
sound2 = pygame.mixer.Sound("endmode.wav")
sound3 = pygame.mixer.Sound("hello.wav")
sound4=pygame.mixer.Sound("sing.wav")

# Ejemplos de patrones y respuestas para el chatbot  ,  ajustar el modelo
pares = [
    ["hola", ["hola, ¿en qué puedo ayudarte?", "hola, ¿qué necesitas?", "¡Hola!",
    "¡Hola! Estoy aquí, ¿cómo estás?"]],
    ["como te llamas", ["llámame Sabina.", "Me han nombrado Sabina"]],
    ["el tiempo de hoy", ["lo siento, no puedo proporcionar información sobre el clima."]],
    ["capital de canada",["Ottawa."]],
    ["capital de japon",["Tokyo."]],
    ["canta", ["escucha","no quiero"]],
    ["algo curioso", [" La miel es uno de los pocos alimentos que nunca se echan a perder. Se han encontrado tarros de miel en tumbas egipcias que tienen miles de años y aún están comestibles."]],
    ["como estas", ["estoy bien gracias, y tu?."]],
    ["alguna anecdota divertida", ["Claro, Había una vez un robot llamado BitBot. Un día, BitBot tropezó con un cubo de tornillos y... ¡se atornilló a sí mismo! Desde entonces, siempre revisa dos veces dónde pisa."]],
    ["un poco aburrida", ["Para desaburrirte, te recomendaría: leer un buen libro, escucha musica, sal a jugar afuera, juega videojuegos, es lo que se me ocurre que puede hacer"]],
    ["gracias por la platica.", ["Siempre estoy aquí para charlar contigo. Si tienes alguna otra pregunta o simplemente quieres conversar, ¡estaré encantado de hacerlo!"]],
    ["como pasas el tiempo", ["En realidad, estoy aquí para ayudarte, así que no tengo pasatiempos.."]],
     ["Cuales son tus funciones", ["entre el listado de mis funciones son: proporcionarte informacion de las busquedas , ademas de poder ver tu estado de animo"]],
    ["algo gracioso", ["claro, esto me hace reir mucho: ¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter"]],
]

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 178)
engine.setProperty('volume', 0.7)

def talk(message):
    engine.say(message)
    engine.runAndWait()

def listen():
    name = "sabina"
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            audio = listener.listen(source)
            #user_input = listener.recognize_google(audio).lower()
            try:
                user_input = listener.recognize_google(audio)
                print("Has dicho:", user_input)  # Imprime lo que has dicho
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                pass

            # Si no se obtiene una entrada válida con recognize_google, utiliza recognize_sphinx
            #if user_input is None:
              #  print("Usando recognize_sphinx...")
              #  user_input = listener.recognize_sphinx(audio)

            return user_input.lower() if user_input else None
    except:
        return None  # Devuelve None en caso de error

# Crea un objeto Chat con los patrones y respuestas
chatbot = Chat(pares, reflections)

# Lógica principal del chatbot
def Brain():
    sound3.play()
    talk("Hablame")

    sound_playing = True
    
    while True:
        try:
            user_input = listen()
            if user_input is None:
                talk("No te entendí, dime de nuevo.")
                continue

            if "regresa" in user_input:
                talk("Desactivando cerebro, regresando a modo normal")
                sound2.play()
                time.sleep(3)
                sound_playing = False  # Desactiva la bandera cuando se reproduce el sonido
                main_window.iconify()  # Minimiza la ventana principal
                subprocess.Popen(["python", "SabinaGUI.py"]) 
                
                break

            # Verifica si se debe reproducir un chiste
            for pattern, responses in pares:
                    if user_input.lower() in pattern and "algo gracioso" in pattern:
                         talk(responses[0])  # Utiliza responses[0] para obtener la primera respuesta
                         #time.sleep(1)
                         sound.play()
                         break  # 
                    elif user_input.lower() in pattern and "alguna anecdota divertida" in pattern:
                         talk(responses[0]) 
                         #time.sleep(1)
                         sound.play()
                         break
                    elif user_input.lower()in pattern and "canta"in pattern:
                        talk(responses[0])
                        sound4.play()
                        time.sleep(10)
                        break

            else:
                response = chatbot.respond(user_input)
                talk(response)

        except KeyboardInterrupt:
            talk("Un error inesperado a ocurrido, Desactivando mis hemisferios")
            break
button_listen=Button(main_window,text="Hablar",fg="white",bg="gray",font=("Arial",10,"bold"),width=20,height=3,command=Brain)
button_listen.pack(pady=10)
main_window.mainloop()