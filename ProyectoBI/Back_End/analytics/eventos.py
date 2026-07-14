import streamlit as st
import requests
import uuid

def enviar_evento(nombre_evento):

    ga4_id = st.secrets.get("GA4_ID")
    ga4_secret = st.secrets.get("GA4_SECRET")

    if not ga4_id or not ga4_secret:
        print("ERROR: No se encontraron GA4_ID o GA4_SECRET en Streamlit Secrets.")
        return None

    url = (
        "https://www.google-analytics.com/mp/collect"
        f"?measurement_id={ga4_id}"
        f"&api_secret={ga4_secret}"
    )

    datos = {
        "client_id": str(uuid.uuid4()),
        "events": [
            {
                "name": nombre_evento
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

    return respuesta.status_code
