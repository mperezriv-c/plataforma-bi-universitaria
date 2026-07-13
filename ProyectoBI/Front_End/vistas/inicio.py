import streamlit as st
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

imagen_path = os.path.join(
    BASE_DIR,
    "assets",
    "principal1.png"
)
def mostrar_inicio():

    col1, col2 = st.columns([1.3,1])

    with col1:
        st.markdown("""
        <div class='titulo'>
        Plataforma BI Integrada -<br>
        Bienestar Físico<br>
        y Mental<br>
        Estudiantil
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='subtitulo'>
        Plataforma Integral de Analítica Universitaria
        con <b style='color:#2563EB;'>BI</b>,
        <b style='color:#7C3AED;'>Big Data</b> e
        <b style='color:#14B8A6;'>IA Ética</b>
        para la mejora del Bienestar Físico y Mental Estudiantil
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.image(imagen_path, width=400)
