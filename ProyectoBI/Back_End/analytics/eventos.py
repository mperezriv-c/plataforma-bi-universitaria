import streamlit as st
import requests
import uuid
import time


def enviar_evento(nombre_evento):

    url = (
        "https://www.google-analytics.com/mp/collect"
        f"?measurement_id={st.secrets['GA4_ID']}"
        f"&api_secret={st.secrets['GA4_SECRET']}"
    )

    datos = {
        "client_id": str(uuid.uuid4()),
        "events": [
            {
                "name": nombre_evento,
                "params": {
                    "debug_mode": 1,
                    "session_id": int(time.time()),
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
    print("STATUS:", respuesta.status_code)
    print("RESPUESTA:", respuesta.text)

    return respuesta.status_code
