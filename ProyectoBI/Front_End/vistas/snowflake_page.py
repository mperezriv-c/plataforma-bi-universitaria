import streamlit as st
import pandas as pd
from graphviz import Digraph

def mostrar_snowflake(engine):
    st.title("❄️ Snowflake Schema Automático")
    
    query_tablas = """
    SELECT table_name AS TABLE_NAME
    FROM information_schema.tables
    WHERE table_schema = 'public'
    AND table_type = 'BASE TABLE'
    """
    tablas = pd.read_sql(query_tablas, engine)

    dot = Digraph()
    
    # 🌟 PARÁMETROS MAESTROS DE ESCALA Y TAMAÑO 🌟
    # Usamos size="12,7!" para darle una dimensión horizontal grande nativa
    # ratio="fill" obliga a que el contenido llene todo el cuadro sin dejar bordes enormes
    dot.attr(
        rankdir="LR", 
        splines="polyline", 
        nodesep="0.25", 
        ranksep="0.7", 
        bgcolor="#F8FAFC",
        size="12,7!",       # Define un tamaño base canvas grande
        ratio="fill"        # Fuerza el autoajuste al contenedor
    )

    for tabla in tablas["table_name"]:
        query_columnas = f"""SELECT column_name AS COLUMN_NAME FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name = '{tabla}'
        """
        columnas = pd.read_sql(query_columnas, engine)

        if "fact" in tabla.lower():
            bg_header, border_color = "#0EA5E9", "#0369A1"
        else:
            bg_header, border_color = "#8B5CF6", "#5B21B6"

        # Construcción de la tabla HTML interna con letras claras y estilizadas
        # Subimos levemente el tamaño a 9 para que sea cómodo de leer sin tocar nada
        html_label = f'''<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="3" STYLE="ROUNDED" COLOR="{border_color}">
            <TR><TD BGCOLOR="{bg_header}"><FONT COLOR="white" FACE="Helvetica" POINT-SIZE="10.5"><B>{tabla.upper()}</B></FONT></TD></TR>
        '''
        
        for col in columnas["column_name"]:
            html_label += f'<TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#1E293B" FACE="Helvetica" POINT-SIZE="9"> • {col}</FONT></TD></TR>'
        
        html_label += '</TABLE>>'

        dot.node(
            tabla, 
            label=html_label, 
            shape="none",
            margin="0"
        )

    query_fk = """
    SELECT
        tc.constraint_name AS fk_name,
        tc.table_name AS parent_table,
        ccu.table_name AS referenced_table
    FROM information_schema.table_constraints AS tc
    JOIN information_schema.constraint_column_usage AS ccu
    ON tc.constraint_name = ccu.constraint_name
    WHERE tc.constraint_type = 'FOREIGN KEY';
    """
    
    relaciones = pd.read_sql(query_fk, engine)

    for _, row in relaciones.iterrows():
        dot.edge(
            row["referenced_table"], 
            row["parent_table"], 
            arrowsize="0.6",
            color="#94A3B8",
            penwidth="1.3"
        )

    # El parámetro use_container_width=True estirará este nuevo lienzo grande al ancho total de tu web
    st.graphviz_chart(dot, use_container_width=True)
    st.success("✅ Snowflake Schema generado automáticamente")