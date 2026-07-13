import streamlit as st
import pandas as pd
from Back_End.analytics.eventos import enviar_evento
import plotly.express as px
import os
import numpy as np
from Back_End.BD.conexion import get_engine

engine = get_engine()
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sqlalchemy import create_engine
from datetime import datetime

def mostrar_ia_predictiva():
    # 1. LEER LA DATA EN TIEMPO REAL
    df = st.session_state.get("df", None)
    
    if df is None:
        st.warning("⚠️ Por favor, suba un archivo de datos (CSV o Excel) en la sección de carga para activar la IA.")
        st.stop()

    # --- CARGAR ESTILOS ---
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    css_path = os.path.join(base_dir, "assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # --- ENCABEZADO ---
    st.markdown("<h1 class='main-title'>🧠 Módulo Analítico Predictivo (IA)</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='subtitle'>Modelado en tiempo real con una muestra actual de <b>{df.shape[0]}</b> registros estudiantiles.</p>", unsafe_allow_html=True)

    # --- BOTÓN DE EJECUCIÓN ---
    col_btn, _ = st.columns([1, 3])
    with col_btn:
        # El botón ahora guarda un estado en la memoria de la app para que no se borre
        if st.button("🚀 Procesar y Reentrenar IA", use_container_width=True):
            enviar_evento("prediccion_ia")
            st.session_state["ia_entrenada"] = True

    # 2. PROCESAR SI EL USUARIO YA LE DIO CLIC AL BOTÓN
    if st.session_state.get("ia_entrenada", False):
        
        # Lógica de Machine Learning (Solo se ejecuta una vez o cuando cambies de archivo)
        df_ml = df.copy()
        columnas_ia = ["riesgo_emocional", "bienestar_general", "nivel_estres", "nivel_ansiedad", "promedio_general"]
        encontradas = [c for c in columnas_ia if c in df_ml.columns]
        
        if len(encontradas) == 0:
            st.error("❌ Los campos del archivo cargado no son compatibles con el pipeline de IA.")
            st.stop()
            
        objetivo = encontradas[0]
        columnas_a_eliminar = [objetivo, 'nombres', 'apellidos', 'codigo_universitario', 'id_estudiante', 'sexo', 'carrera', 'facultad']
        columnas_presentes = [c for c in columnas_a_eliminar if c in df_ml.columns]
        
        for c in df_ml.drop(columns=columnas_presentes, errors='ignore').select_dtypes(include="object"):
            df_ml[c] = LabelEncoder().fit_transform(df_ml[c].astype(str))

        X = df_ml.drop(columns=columnas_presentes, errors='ignore')
        y = df_ml[objetivo]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        modelo = RandomForestRegressor(random_state=42)
        modelo.fit(X_train, y_train)
        pred = modelo.predict(X_test)
        precision = r2_score(y_test, pred)

        predicciones = pd.DataFrame({
            "id_prediccion": range(1, len(pred)+1),
            "id_estudiante": df.loc[X_test.index, "id_estudiante"].values,
            "id_tiempo": [20260101]*len(pred),
            "prediccion_bienestar": pred,
            "nivel_riesgo": [
               1 if p >=4 else
               2 if p >=3 else
               3
               for p in pred
            ],
            "probabilidad_alerta": pred/100,
            "prediccion_nota_futura": df.loc[X_test.index,"promedio_general"].values,
            "perfil_cluster": np.random.randint(1,4,len(pred)),
            "precision_modelo": [precision]*len(pred),
            "fecha_prediccion": datetime.today().date(),
            "riesgo_emocional": pred,
            "probabilidad_abandono": pred/100,
            "alerta_temprana":[
                "BAJA" if p>=4 else
                "MEDIA" if p<=3 else
                "ALTA"
                for p in pred
           ],
          "prediccion_ia":[
              "Riesgo Bajo" if p>=4 else
              "Riesgo Medio" if p>=3 else
              "Riesgo Alto"
              for p in pred
            ]
        })
        try:
            predicciones.to_sql(
                  "fact_predicciones",
                  engine,
                  if_exists="append",
                  index=False
                  )
            st.success("✅ Predicciones guardadas")
        except Exception as e:
            st.error(f"Error: {e}")

        # --- FILA DE KPIs ---
        st.markdown("### 📊 Cuadro de Mando de Evaluación")
        c1, c2, c3 = st.columns(3)
        
        importancia = pd.DataFrame({"Variable": X.columns, "Importancia": modelo.feature_importances_}).sort_values(by="Importancia", ascending=False)
        top_var = importancia.iloc[0]['Variable'].replace('_', ' ').title() if not importancia.empty else "N/A"

        with c1:
            st.markdown(f"<div class='card-kpi' style='border-left: 6px solid #8B5CF6;'><p style='color: #64748B; margin:0; font-size:12px; font-weight:700;'>FACTOR CLAVE</p><h2 style='color: #4C1D95; margin:8px 0 0 0; font-size:18px;'>🔍 {top_var}</h2></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='card-kpi' style='border-left: 6px solid #3B82F6;'><p style='color: #64748B; margin:0; font-size:12px; font-weight:700;'>PRECISIÓN (R²)</p><h2 style='color: #1D4ED8; margin:8px 0 0 0; font-size:22px;'>{(precision * 100):.1f}%</h2></div>", unsafe_allow_html=True)
        with c3:
            color_txt, texto_semaforo = ("#15803D", "🟢 Excelente") if precision >= 0.70 else ("#B45309", "🟡 Aceptable") if precision >= 0.40 else ("#B91C1C", "🔴 Deficiente")
            st.markdown(f"<div class='card-kpi' style='border-left: 6px solid {color_txt};'><p style='color: #64748B; margin:0; font-size:12px; font-weight:700;'>CONFIANZA</p><h2 style='color: {color_txt}; margin:8px 0 0 0; font-size:18px;'>{texto_semaforo}</h2></div>", unsafe_allow_html=True)

        # --- GRÁFICOS ---
        col_graf1, col_graf2 = st.columns([1.3, 1])
        with col_graf1:
            st.markdown("<div class='card-graph'>", unsafe_allow_html=True)
            grafico_linea = pd.DataFrame({"Real": y_test.values, "Predicción": pred}).head(50)
            fig = px.line(grafico_linea, title="📈 Real vs Predicción del Nuevo Lote", color_discrete_sequence=["#3B82F6", "#10B981"])
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_family="DM Sans", margin=dict(l=10, r=10, t=50, b=10))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_graf2:
            st.markdown("<div class='card-graph'>", unsafe_allow_html=True)
            fig2 = px.bar(importancia.head(5), x="Importancia", y="Variable", orientation="h", title="🎯 Factores de Impacto del Nuevo Lote", color_continuous_scale=["#3B82F6", "#8B5CF6"])
            fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_family="DM Sans", showlegend=False, coloraxis_showscale=False, margin=dict(l=10, r=10, t=50, b=10))
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # --- TABLA DE ALERTA TEMPRANA DINÁMICA ---
        st.write("")
        st.markdown("### 🚨 Módulo de Intervención y Prescripción")
        media_y = y.mean()
        riesgo_total = ["🔴 Alto" if p >= media_y * 1.2 else "🟡 Medio" if p >= media_y * 0.8 else "🟢 Bajo" for p in pred]
        
        col_tabla, col_reco = st.columns([1.2, 1])
        with col_tabla:
            st.markdown("<div class='card-graph'>", unsafe_allow_html=True)
            st.markdown("<p style='font-weight:700; color:#0F172A; margin-top:0; margin-bottom:15px;'>📋 Diagnóstico Automatizado de Nuevos Alumnos</p>", unsafe_allow_html=True)
            tabla_riesgo = pd.DataFrame({
                "Código": df.loc[X_test.index, 'codigo_universitario'].values[:10] if 'codigo_universitario' in df.columns else range(10),
                "Valor Real": y_test.values[:10], 
                "Predicción IA": [round(p, 2) for p in pred[:10]], 
                "Nivel Riesgo": riesgo_total[:10]
            })
            st.dataframe(tabla_riesgo, use_container_width=True, height=200)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_reco:
            st.markdown("<div class='card-graph'>", unsafe_allow_html=True)
            st.markdown("<p style='font-weight:700; color:#8B5CF6; margin-top:0; margin-bottom:15px;'>🤖 Recomendaciones de IA Ética</p>", unsafe_allow_html=True)
            if precision >= 0.50:
                st.markdown(f"<div style='background-color: #EFF6FF; padding: 15px; border-radius: 12px; border-left: 5px solid #3B82F6; font-size:14px; color:#1E3A8A;'><b>Análisis Confiable:</b><br>Tras procesar los nuevos registros ingresados, la IA determina que la variable <b>{top_var.lower()}</b> lidera el impacto de riesgo. Se sugiere coordinar con tutoría académica.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='background-color: #FFFBEB; padding: 15px; border-radius: 12px; border-left: 5px solid #D97706; font-size:14px; color:#78350F;'><b>Alerta de Consistencia:</b><br>La nueva muestra ingresada presenta alta variabilidad. No tome acciones punitivas automáticas basados en esta simulación.</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
