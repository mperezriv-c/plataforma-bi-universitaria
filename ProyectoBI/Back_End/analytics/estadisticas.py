import pandas as pd
from Back_End.BD.conexion import get_engine


def registrar_evento(nombre):

    engine = get_engine()

    datos = pd.DataFrame([
        {
            "nombre_evento": nombre
        }
    ])

    datos.to_sql(
        "analitica_eventos",
        engine,
        if_exists="append",
        index=False
    )
