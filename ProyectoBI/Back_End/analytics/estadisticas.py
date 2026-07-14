import streamlit as st

def registrar_evento(nombre):

    if "estadisticas" not in st.session_state:

        st.session_state.estadisticas = {
            "inicio_sesion": 0,
            "carga_datos": 0,
            "etl_ejecutado": 0,
            "consulta_kpis": 0,
            "prediccion_ia": 0,
            "dashboard_bi": 0,
            "salida_plataforma": 0
        }

    if nombre in st.session_state.estadisticas:
        st.session_state.estadisticas[nombre] += 1