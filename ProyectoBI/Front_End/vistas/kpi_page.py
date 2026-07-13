import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from sqlalchemy import text
from Back_End.analytics.eventos import enviar_evento

def mostrar_kpis(engine):
    enviar_evento("consulta_kpis")
    query = """
    SELECT 
        fb.bienestar_general,
        fb.nivel_estres_num,
        fb.nivel_ansiedad_num,
        fb.horas_sueno,
        fr.promedio_general,
        fr.riesgo_academico
    FROM fact_bienestar fb
    INNER JOIN fact_rendimiento fr
    ON fb.id_estudiante = fr.id_estudiante
    """
    df = pd.read_sql(query, engine)

    st.title("📊 KPIs Empresariales")
    
    total_registros = len(df)
    total_columnas = len(df.columns)
    total_nulos = df.isnull().sum().sum()
    columnas_numericas = len(df.select_dtypes(include=np.number).columns)
    columnas_texto = len(df.select_dtypes(include="object").columns)
    calidad = round((1 - (total_nulos / (df.shape[0] * df.shape[1]))) * 100, 1)

    st.markdown("### 📊 Indicadores Inteligentes BI")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.markdown(f"<div class='card' style='text-align:center;'><p style='color:#64748B;font-size:12px;margin:0;font-weight:600;'>REGISTROS</p><h3 style='margin:5px 0 0 0;color:#1E293B;'>{total_registros}</h3></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='card' style='text-align:center;'><p style='color:#64748B;font-size:12px;margin:0;font-weight:600;'>COLUMNAS</p><h3 style='margin:5px 0 0 0;color:#1E293B;'>{total_columnas}</h3></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='card' style='text-align:center;'><p style='color:#64748B;font-size:12px;margin:0;font-weight:600;'>CALIDAD DATA</p><h3 style='margin:5px 0 0 0;color:#10B981;'>{calidad}%</h3></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='card' style='text-align:center;'><p style='color:#64748B;font-size:12px;margin:0;font-weight:600;'>VAR. NUMÉRICAS</p><h3 style='margin:5px 0 0 0;color:#2563EB;'>{columnas_numericas}</h3></div>", unsafe_allow_html=True)
    with c5: st.markdown(f"<div class='card' style='text-align:center;'><p style='color:#64748B;font-size:12px;margin:0;font-weight:600;'>VAR. TEXTO</p><h3 style='margin:5px 0 0 0;color:#7C3AED;'>{columnas_texto}</h3></div>", unsafe_allow_html=True)

    st.write("")
    df_numerico_real = df.select_dtypes(include=np.number).drop(columns=[c for c in df.columns if any(p in c.lower() for p in ["id", "codigo", "dni"])], errors='ignore')

    if "bienestar_general" in df.columns:
        promedio_general = round(df["bienestar_general"].mean(), 1)
    elif not df_numerico_real.empty:
        promedio_general = round(df_numerico_real.mean().mean() * 10, 1) if df_numerico_real.max().max() <= 10 else round(df_numerico_real.mean().mean(), 1)
    else:
        promedio_general = 50.0

    riesgo = round(100 - promedio_general, 1)
    color_est, estado = ("#10B981", "🟢 Saludable") if promedio_general >= 70 else ("#F59E0B", "🟡 Estable / Alerta") if promedio_general >= 45 else ("#EF4444", "🔴 Crítico")

    st.markdown("### 🧠 KPIs de Bienestar Estudiantil")
    k1, k2, k3 = st.columns(3)
    with k1: st.markdown(f"<div class='card' style='border-left: 5px solid #10B981;'><p style='color:#64748B; font-size:13px; margin:0; font-weight:600;'>💚 ÍNDICE BIENESTAR GENERAL</p><h2 style='margin:5px 0 0 0; color:#10B981;'>{promedio_general} / 100</h2></div>", unsafe_allow_html=True)
    with k2: st.markdown(f"<div class='card' style='border-left: 5px solid #EF4444;'><p style='color:#64748B; font-size:13px; margin:0; font-weight:600;'>🚨 NIVEL RIESGO COLECTIVO</p><h2 style='margin:5px 0 0 0; color:#EF4444;'>{riesgo}%</h2></div>", unsafe_allow_html=True)
    with k3: st.markdown(f"<div class='card' style='border-left: 5px solid {color_est};'><p style='color:#64748B; font-size:13px; margin:0; font-weight:600;'>📌 ESTADO GENERAL DE LA MUESTRA</p><h2 style='margin:5px 0 0 0; color:{color_est};'>{estado}</h2></div>", unsafe_allow_html=True)

    st.write("")
    col_izq, col_der = st.columns([1.3, 1])

    with col_izq:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<p style='font-weight:700; margin-top:0;'>📈 Distribución Dinámica de Datos</p>", unsafe_allow_html=True)
        columnas_visibles = [c for c in df.columns if not any(p in c.lower() for p in ["id", "codigo", "dni"])]
        columna = st.selectbox("Selecciona una variable:", columnas_visibles if columnas_visibles else df.columns)

        if df[columna].dtype == "object":
            grafico = df[columna].value_counts().head(10).reset_index()
            grafico.columns = [columna, "Cantidad"]
            fig = px.bar(grafico, x=columna, y="Cantidad", color="Cantidad", color_continuous_scale=["#2563EB", "#7C3AED"])
        else:
            fig = px.histogram(df, x=columna, color_discrete_sequence=["#2563EB"], nbins=20)
            
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=10, t=10, b=10), coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_der:
        st.markdown("<div class='card' style='height: 100%; min-height:430px;'><h4 style='color:#2563EB; margin-top:0;'>📈 Análisis Estadístico Inteligente</h4><div style='background-color:#F8FAFC; padding:12px; border-radius:8px; border-left:4px solid #7C3AED;'>🔹 <b>Métricas Control:</b> Monitoreo de nulos.<br><br>🔹 <b>Normalización:</b> Descarte de IDs.<br><br>🔹 <b>Frecuencias:</b> Desglose adaptativo.</div></div>", unsafe_allow_html=True)

    st.write("")
    st.markdown("### 📋 Resumen Estadístico Descriptivo")
    traducciones = {"count": "Total Registros", "mean": "Promedio", "std": "Desviación Estándar", "min": "Mínimo", "max": "Máximo"}

    cols_numericas = [c for c in df.select_dtypes(include=np.number).columns if not any(p in c.lower() for p in ["id", "codigo", "dni"])]
    if cols_numericas:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.dataframe(df[cols_numericas].describe().rename(index=traducciones).style.format("{:.2f}"), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
