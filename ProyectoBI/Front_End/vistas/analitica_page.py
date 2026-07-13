import streamlit as st
from Back_End.analytics.ga4 import obtener_metricas_ga4
def mostrar():

    st.title("🌐 Analítica Web - Google Analytics 4")

    st.markdown("""
    ### Monitoreo del uso de la Plataforma Integral de Analítica Universitaria

    Datos obtenidos directamente desde Google Analytics 4.
    """)

    try:

        datos = obtener_metricas_ga4()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "👥 Usuarios activos",
                datos.get("usuarios_activos", 0)
            )

        with col2:
            st.metric(
                "📄 Vistas de página",
                datos.get("vistas_pagina", 0)
            )

        with col3:
            st.metric(
                "📊 Total de eventos",
                datos.get("eventos", 0)
            )


        st.divider()
        st.subheader("📌 Eventos registrados en GA4")

        eventos = {
            "Inicio de sesión": 0,
            "Carga de datos": 0,
            "ETL ejecutado": 0,
            "Consulta de KPIs": 0,
            "Predicción IA": 0,
            "Descarga de reporte": 0,
            "Cierre de sesión": 0
        }

        st.bar_chart(eventos)


    except Exception as e:
        st.error(f"Error conectando con Google Analytics 4: {e}")
