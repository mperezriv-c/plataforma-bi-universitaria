from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()


def get_engine():

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")


    conexion = (
        f"postgresql://{user}:{password}@{host}:{port}/{database}"
    )

    engine = create_engine(conexion)

    return engine