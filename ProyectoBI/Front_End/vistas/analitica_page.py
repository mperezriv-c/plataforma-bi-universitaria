import streamlit as st
import pandas as pd
from Back_End.BD.conexion import get_engine

def mostrar():
    st.title("🌐 Analítica Web")

    st.write("Monitoreo del uso de la plataforma.")

    # Leer eventos guardados en Supabase/PostgreSQL
    try:

        engine = get_engine()

        df = pd.read_sql(
            "SELECT * FROM analitica_eventos",
            engine
        )


        if df.empty:
            st.warning("No hay eventos registrados")
            return


        eventos_bd = df["nombre_evento"].value_counts()


    except Exception as e:

        st.error(f"Error cargando analítica: {e}")
        return



    total = eventos_bd.sum()


    c1, c2, c3 = st.columns(3)


    c1.metric(
        "👥 Inicio de sesión",
        eventos_bd.get("inicio_sesion", 0)
    )


    c2.metric(
        "📊 Eventos registrados",
        total
    )


    c3.metric(
        "📈 Dashboard BI",
        eventos_bd.get("dashboard_bi", 0)
    )


    st.divider()


    eventos = {

        "Inicio":
            eventos_bd.get("inicio_sesion", 0),

        "Carga":
            eventos_bd.get("carga_datos", 0),

        "ETL":
            eventos_bd.get("etl_ejecutado", 0),

        "KPIs":
            eventos_bd.get("consulta_kpis", 0),

        "IA":
            eventos_bd.get("prediccion_ia", 0),

        "Dashboard":
            eventos_bd.get("dashboard_bi", 0),

        "Salida":
            eventos_bd.get("salida_plataforma", 0)

    }

    st.subheader("📊 Eventos registrados")

    st.bar_chart(eventos)

    st.subheader("📋 Resumen")


    st.table(
        {
            "Evento": list(eventos.keys()),
            "Cantidad": list(eventos.values())
        }
    )
