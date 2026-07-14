import streamlit as st
import requests
import uuid
from Back_End.analytics.estadisticas import registrar_evento

def enviar_evento(nombre_evento):

    url = (
        "https://www.google-analytics.com/mp/collect"
        f"?measurement_id={st.secrets.get('GA4_ID')}"
        f"&api_secret={st.secrets['GA4_SECRET']}"
    )

    datos = {
        "client_id": str(uuid.uuid4()),
        "events": [
            {
                "name": nombre_evento,
                "params": {
                    "app": "Plataforma_BI_Universitaria"
                }
            }
        ]
    }

    respuesta = requests.post(url, json=datos)


    print("EVENTO:", nombre_evento)
    print("GA4 STATUS:", respuesta.status_code)
    print("GA4 RESPONSE:", respuesta.text)


    if "estadisticas" in st.session_state:
        if nombre_evento in st.session_state.estadisticas:
            st.session_state.estadisticas[nombre_evento] += 1


    return respuesta.status_code
