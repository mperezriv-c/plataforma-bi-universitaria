from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Metric,
    Dimension
)
from google.oauth2 import service_account
import streamlit as st


def get_ga4_client():

    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )

    client = BetaAnalyticsDataClient(
        credentials=credentials
    )

    return client



def obtener_metricas_ga4():

    client = get_ga4_client()

    # CAMBIAR ESTE ID DESPUÉS
    PROPERTY_ID = "545269653"


    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        date_ranges=[
            DateRange(
                start_date="30daysAgo",
                end_date="today"
            )
        ],
        metrics=[
            Metric(name="activeUsers"),
            Metric(name="screenPageViews"),
            Metric(name="eventCount")
        ]
    )


    response = client.run_report(request)


    datos = {}

    for row in response.rows:
        datos["usuarios_activos"] = row.metric_values[0].value
        datos["vistas_pagina"] = row.metric_values[1].value
        datos["eventos"] = row.metric_values[2].value


    return datos

if __name__ == "__main__":
    datos = obtener_metricas_ga4()
    print(datos)
