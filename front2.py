import streamlit as st
from gtts import gTTS
import io
from chat_base import predict_class, get_response, intents
# Funciones
#funcion  para hablar 
def speak(text):
    tts = gTTS(text=text, lang='es')
    audio_file = io.BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    st.audio(audio_file, format='audio/mp3')
# Lógica del chatbot
if "messages" not in st.session_state:
    st.session_state.messages = []
if "first_message" not in st.session_state:
    st.session_state.first_message = True
if "user_avatar" not in st.session_state:
    st.session_state.user_avatar = "https://cdn.icon-icons.com/icons2/3399/PNG/512/bot_icon_214984.png"  # URL de la imagen del usuario

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.first_message:
    initial_message = "Hola,selecciona la planeación que necesites."
    with st.chat_message("Bot"):
        st.markdown(initial_message)
    st.session_state.messages.append({"role": "Bot", "content": initial_message})
    st.session_state.first_message = False
    speak(initial_message)

if prompt := st.chat_input("¿Cómo puedo ayudarte?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    insts = predict_class(prompt)
    res = get_response(insts, intents)

    with st.chat_message("Bot"):
        st.markdown(res)
    st.session_state.messages.append({"role": "Bot", "content": res})
    speak(res)