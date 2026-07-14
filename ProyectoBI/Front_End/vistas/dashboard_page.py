import streamlit as st
import streamlit.components.v1 as components
from Back_End.analytics.eventos import enviar_evento

def mostrar_dashboard():
    enviar_evento("dashboard_bi")
        
    st.title("📊 Dashboard BI")


    st.markdown("""
### Cuadro de Mando Integral

Plataforma Integral de Analítica Universitaria para el análisis del bienestar físico, mental y rendimiento académico estudiantil.
""")

    url_looker = "https://datastudio.google.com/s/oHJek-0TIAY"

    components.iframe(
        url_looker,
        height=900,
        scrolling=True
    )

    st.success("✅ Dashboard BI integrado correctamente.")
