import streamlit as st

def mostrar():

    st.title("🌐 Analítica Web")

    estadisticas = st.session_state.get(
        "estadisticas",
        {}
    )

    total = sum(estadisticas.values()) if estadisticas else 0

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "👥 Inicio de sesión",
            estadisticas.get("inicio_sesion",0)
        )

    with c2:
        st.metric(
            "📊 Eventos registrados",
            total
        )

    with c3:
        st.metric(
            "📈 Dashboard BI",
            estadisticas.get("dashboard_bi",0)
        )

    st.divider()

    eventos = {
        "Inicio": estadisticas.get("inicio_sesion",0),
        "Carga": estadisticas.get("carga_datos",0),
        "ETL": estadisticas.get("etl_ejecutado",0),
        "KPIs": estadisticas.get("consulta_kpis",0),
        "IA": estadisticas.get("prediccion_ia",0),
        "Dashboard": estadisticas.get("dashboard_bi",0),
        "Salida": estadisticas.get("salida_plataforma",0)
    }

    st.subheader("📊 Eventos registrados")

    st.bar_chart(eventos)

    st.divider()

    st.subheader("📋 Resumen")

    st.table({
        "Evento": list(eventos.keys()),
        "Cantidad": list(eventos.values())
    })
