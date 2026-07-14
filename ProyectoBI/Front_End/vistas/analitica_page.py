import streamlit as st


def mostrar():

    st.title("🌐 Analítica Web")

    st.write("Monitoreo del uso de la plataforma.")


    datos = st.session_state.get("estadisticas", {})


    total = sum(datos.values())


    c1, c2, c3 = st.columns(3)


    c1.metric(
        "👥 Inicio de sesión",
        datos.get("inicio_sesion", 0)
    )


    c2.metric(
        "📊 Eventos registrados",
        total
    )


    c3.metric(
        "📈 Dashboard BI",
        datos.get("dashboard_bi", 0)
    )


    st.divider()


    eventos = {

        "Inicio":
            datos.get("inicio_sesion", 0),

        "Carga":
            datos.get("carga_datos", 0),

        "ETL":
            datos.get("etl_ejecutado", 0),

        "KPIs":
            datos.get("consulta_kpis", 0),

        "IA":
            datos.get("prediccion_ia", 0),

        "Dashboard":
            datos.get("dashboard_bi", 0),

        "Salida":
            datos.get("salida_plataforma", 0)

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
