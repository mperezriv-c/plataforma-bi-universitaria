from sqlalchemy import create_engine
import streamlit as st


def get_engine():

    host = st.secrets["DB_HOST"]
    port = st.secrets["DB_PORT"]
    database = st.secrets["DB_NAME"]
    user = st.secrets["DB_USER"]
    password = st.secrets["DB_PASSWORD"]

    conexion = (
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    )

    engine = create_engine(conexion)

    return engine
