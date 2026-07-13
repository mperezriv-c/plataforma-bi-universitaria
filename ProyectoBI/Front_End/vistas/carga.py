import streamlit as st
import pandas as pd

def mostrar_carga():

    st.title("📂 Carga Inteligente de Datos")

    if "archivos" not in st.session_state:
        st.session_state.archivos = {}

    archivos = st.file_uploader(
        "Subir Excel o CSV",
        type=["xlsx","xls","csv"],
        accept_multiple_files=True
    )

    if archivos:

        for archivo in archivos:

            if archivo.name.endswith(".csv"):
                df = pd.read_csv(archivo)
            else:
                df = pd.read_excel(
                    archivo,
                    engine="openpyxl"
                )

            nombre = archivo.name.replace(".xlsx","")

            st.session_state.archivos[nombre] = df

        st.success("✅ Archivos cargados")

        for nombre, df in st.session_state.archivos.items():

            st.subheader(nombre)

            st.dataframe(df.head())

        dataset = st.selectbox(
            "Dataset principal",
            list(st.session_state.archivos.keys())
        )

        st.session_state.dataset_actual = dataset
        st.session_state.df = st.session_state.archivos[dataset]