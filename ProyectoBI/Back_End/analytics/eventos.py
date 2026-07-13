import streamlit as st
import requests
import uuid


def enviar_evento(nombre_evento):

    url = (
        "https://www.google-analytics.com/mp/collect"
        f"?measurement_id={st.secrets.get('GA4_ID')}"
        f"&api_secret={st.secrets.get('GA4_SECRET')}"
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
    st.write("GA4 STATUS:", respuesta.status_code)
    st.write("GA4 RESPONSE:", respuesta.text)

    return respuesta.status_code
