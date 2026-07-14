import streamlit as st
import streamlit.components.v1 as components
from Back_End.analytics.eventos import enviar_evento

def mostrar_dashboard():

    st.title("📊 Dashboard BI")
if "dashboard_registrado" not in st.session_state:
    enviar_evento("dashboard_bi")
    st.session_state.dashboard_registrado = True

    st.markdown("""
### Cuadro de Mando Integral

Plataforma Integral de Analítica Universitaria para el análisis del bienestar físico, mental y rendimiento académico estudiantil.
""")

    url_looker = "https://datastudio.google.com/embed/reporting/68ce8c05-14b1-4fdb-a151-78ca88d48d07/page/p_abgadnwa5d"

    components.iframe(
        url_looker,
        height=900,
        scrolling=True
    )

    st.success("✅ Dashboard BI integrado correctamente.")
