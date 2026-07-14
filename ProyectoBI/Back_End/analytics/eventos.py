import streamlit as st
import requests
import uuid
from Back_End.analytics.estadisticas import registrar_evento

def enviar_evento(nombre_evento):

    ga4_id = st.secrets.get("GA4_ID")
    ga4_secret = st.secrets.get("GA4_SECRET")

    if not ga4_id or not ga4_secret:
        print("ERROR: No se encontraron GA4_ID o GA4_SECRET.")
        return None

    # Mantener el mismo client_id durante toda la sesión
    if "ga_client_id" not in st.session_state:
        st.session_state["ga_client_id"] = str(uuid.uuid4())

    client_id = st.session_state["ga_client_id"]

    url = (
        "https://www.google-analytics.com/mp/collect"
        f"?measurement_id={ga4_id}"
        f"&api_secret={ga4_secret}"
    )

    datos = {
        "client_id": client_id,
        "events": [
            {
                "name": nombre_evento,
                "params": {
                    "engagement_time_msec": 100
                }
            }
        ]
    }
    respuesta = requests.post(
        url,
        json=datos
    )

    print("EVENTO:", nombre_evento)
    print("GA4 STATUS:", respuesta.status_code)
    print("GA4 RESPONSE:", respuesta.text)

    registrar_evento(nombre_evento)
    return respuesta.status_code
