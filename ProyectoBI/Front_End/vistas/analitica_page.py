import streamlit as st
import streamlit.components.v1 as components

def mostrar():

    st.title("📈 Analítica Web")

    st.markdown("""
### Monitoreo del uso de la Plataforma Integral de Analítica Universitaria

Visualización de métricas obtenidas desde Google Analytics 4.
""")

    url_analitica = ""

    components.iframe(
        url_analitica,
        height=900,
        scrolling=True
    )

    st.success("✅ Analítica Web integrada correctamente.")