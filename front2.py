import streamlit as st
from gtts import gTTS
import io
import nltk
import speech_recognition as sr
from chat_base import predict_class, get_response, intents

# Descarga el tokenizador de NLTK si no está disponible
nltk.download('punkt', quiet=True)

# Funciones
def speak(text):
    tts = gTTS(text=text, lang='es')
    audio_file = io.BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    st.audio(audio_file, format='audio/mp3')

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Escuchando...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="es-ES")
            return text
        except sr.UnknownValueError:
            st.error("No entendí lo que dijiste")
            return None
        except sr.RequestError:
            st.error("Error al conectarse al servicio de reconocimiento de voz")
            return None

# Interfaz de Streamlit
st.title("AI")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "first_message" not in st.session_state:
    st.session_state.first_message = True

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    if message["role"] == "Bot":
        with st.chat_message("Bot"):
            st.markdown(message["content"])
    else:
        with st.chat_message("user"):
            st.markdown(message["content"])

# Primer mensaje del bot
if st.session_state.first_message:
    initial_message = "Te doy la bienvenida, estoy aquí para ayudarte."
    with st.chat_message("Bot"):
        st.markdown(initial_message)
    st.session_state.messages.append({"role": "Bot", "content": initial_message})
    st.session_state.first_message = False
    speak(initial_message)

# Botón para hablar
if st.button("Hablar"):
    prompt = listen()
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Implementación del algoritmo de la IA
        insts = predict_class(prompt)
        res = get_response(insts, intents)

        with st.chat_message("Bot"):
            st.markdown(res)
        st.session_state.messages.append({"role": "Bot", "content": res})
        speak(res)

# Opción para ingresar texto manualmente si no se usa la voz
if prompt := st.chat_input("Estoy para ti, ¿qué necesitas?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Implementación del algoritmo de la IA
    insts = predict_class(prompt)
    res = get_response(insts, intents)

    with st.chat_message("Bot"):
        st.markdown(res)
    st.session_state.messages.append({"role": "Bot", "content": res})
    speak(res)
