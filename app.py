import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64


st.markdown("""
    <style>
        body {
            background-color: #1e2a47;  /* Fondo azul oscuro */
            color: #ffffff;  /* Texto en color blanco */
        }
        .stTitle {
            color: #f4a261;  /* Título con un color cálido */
        }
        .stHeader {
            color: #ffb703;  /* Cabecera en un tono dorado */
        }
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: #4c6a92;  /* Fondo del campo de texto */
            color: white;  /* Texto en el campo de texto en blanco */
            border-radius: 10px;
        }
        .stImage>div>img {
            border-radius: 15px;  /* Bordes redondeados para la imagen */
        }
        .stButton>button {
            background-color: #ffb703;  /* Color amarillo en los botones */
            color: #1e2a47;  /* Texto oscuro en el botón */
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)


st.title("Medusas en el Mar: Fábula Sonora y Conversión de Texto a Audio")


image = Image.open('medu.png')  
st.image(image, width=350)

with st.sidebar:
    st.subheader("Escribe o selecciona texto para escuchar sobre las medusas.")


try:
    os.mkdir("temp")
except:
    pass


st.subheader("Una pequeña fábula sobre el mar.")
st.write('En un rincón del océano, una medusa se lamentaba por la rapidez con la que el mar se reducía. '
         'Al principio el océano parecía interminable, lleno de corrientes y coloridas criaturas. '
         'Pero a medida que las aguas se estrechaban, sentía que su libertad se desvanecía. '
         'En su camino se encontró con un pez sabio que le dijo: "Todo lo que debes hacer es adaptarte, no resistirte." '
         'Y entonces, la medusa siguió nadando, encontrando nuevas corrientes. '
         'Una enseñanza sobre adaptarse al cambio.'
         ' — Anónimo')


text = st.text_area("Escribe el texto a escuchar:")


tld = 'com'
option_lang = st.selectbox(
    "Selecciona el idioma",
    ("Español", "English"))
if option_lang == "Español":
    lg = 'es'
if option_lang == "English":
    lg = 'en'


def text_to_speech(text, tld, lg):
    tts = gTTS(text, lang=lg)  
    try:
        my_file_name = text[0:20]  
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text


if st.button("Convertir a Audio"):
    result, output_text = text_to_speech(text, 'com', lg)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    
    
    st.markdown(f"## Tu Audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    
    with open(f"temp/{result}.mp3", "rb") as f:
        data = f.read()

    def get_binary_file_downloader_html(bin_file, file_label='Archivo'):
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Descargar {file_label}</a>'
        return href

    st.markdown(get_binary_file_downloader_html(f"temp/{result}.mp3", file_label="Audio"), unsafe_allow_html=True)


def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Eliminado ", f)

remove_files(7)
