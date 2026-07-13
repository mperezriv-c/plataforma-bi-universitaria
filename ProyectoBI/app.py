import streamlit as st
import os
from Back_End.analytics.eventos import enviar_evento

from Front_End.vistas import analitica_page
from Front_End.vistas.dashboard_page import mostrar_dashboard
from Back_End.BD.conexion import get_engine
from Front_End.vistas.inicio import mostrar_inicio
from Front_End.vistas.carga import mostrar_carga
from Front_End.vistas.etl_page import mostrar_etl
from Front_End.vistas.snowflake_page import mostrar_snowflake
from Front_End.vistas.ia_page import mostrar_ia_predictiva
from Front_End.vistas.kpi_page import mostrar_kpis

engine = get_engine()

st.set_page_config(
    page_title="BI Bienestar",
    layout="wide"
)
enviar_evento("inicio_sesion")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

css_path = os.path.join(
    BASE_DIR,
    "Front_End",
    "assets",
    "style.css"
)

with open(css_path, encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

if "df" not in st.session_state:
    st.session_state.df = None

with st.sidebar:

    menu = st.radio(
        "MENÚ",
        [
            "🏠 Inicio",
            "📂 Carga",
            "⚙️ ETL",
            "❄️ Snowflake",
            "🧠 IA",
            "📊 KPIs",
            "📊 Dashboard BI",
            "📈 Analítica Web"
        ]
    )

    st.divider()

    if st.button("🚪 Salir de la plataforma", use_container_width=True):
        enviar_evento("salida_plataforma")
        st.session_state.clear()
        st.rerun()

if menu == "🏠 Inicio":
    mostrar_inicio()

elif menu == "📂 Carga":
    mostrar_carga()

elif menu == "⚙️ ETL":
    mostrar_etl(engine)

elif menu == "❄️ Snowflake":
    mostrar_snowflake(engine)

elif menu == "🧠 IA":
    mostrar_ia_predictiva()

elif menu == "📊 KPIs":
    mostrar_kpis(engine)

elif menu == "📊 Dashboard BI":
    mostrar_dashboard()

elif menu == "📈 Analítica Web":
    analitica_page.mostrar()
