import streamlit as st
from gtts import gTTS
import pygame
import os
import tempfile
from chat_base import predict_class, get_response, intents

def speak(text):
    temp_audio_file = None
    try:
        # Crear archivo temporal
        temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts = gTTS(text=text, lang='es')
        tts.save(temp_audio_file.name)
        temp_audio_file_path = temp_audio_file.name
        temp_audio_file.close()

        # Inicializar pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load(temp_audio_file_path)
        pygame.mixer.music.play()

        # Esperar a que termine de reproducir
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    finally:
        if temp_audio_file:
            try:
                os.unlink(temp_audio_file_path)
            except PermissionError:
                pass  # Manejo de excepción si el archivo aún está en uso

# Ruta de la imagen
#user_avatar = "ruta/a/tu/avatar.png"  # Asegúrate de que la ruta es correcta

# Asegúrate de que la imagen existe

# Título con avatar usando HTML y CSS
st.title("AI")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "first_message" not in st.session_state:
    st.session_state.first_message = True
 

for message in st.session_state.messages:
    if message["role"] == "Bot":
        with st.chat_message("Bot"):  # Ruta del avatar del bot
            st.markdown(message["content"])
    else:
        with st.chat_message("user"):
            st.markdown(message["content"])

if st.session_state.first_message:
    initial_message = "Te doy la bienvenida, estoy aqui para ayudarte."
    with st.chat_message("Bot"):
        st.markdown(initial_message)
    st.session_state.messages.append({"role": "Bot", "content": initial_message})
    st.session_state.first_message = False
    speak(initial_message)  # Hablar el mensaje inicial

if prompt := st.chat_input("Estoy para ti, que necesitas?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Implementación del algoritmo de la IA
    insts = predict_class(prompt)
    res = get_response(insts, intents)

    with st.chat_message("Bot"):
        st.markdown(res)
    st.session_state.messages.append({"role": "Bot", "content": res})
    speak(res)  # Hablar la respuesta
    
