import streamlit as st
import pandas as pd
from Back_End.analytics.eventos import enviar_evento

def mostrar_etl(engine):
    st.markdown("""
    <h1 style='color:#2563EB; font-size:55px; font-weight:800;'>
    ⚙️ ETL Inteligente Unificado
    </h1>
    """, unsafe_allow_html=True)

    if len(st.session_state.archivos) == 0:
        st.warning("⚠️ Primero carga el archivo Excel de Estudiantes")
        st.stop()

    st.write("")
    st.subheader("📂 Archivos Detectados")

    for nombre, df in st.session_state.archivos.items():
        st.markdown(f"""
        <div class='card'>
        <h3>📄 {nombre}</h3>
        <p>Registros detectados: {len(df)}</p>
        <p>Columnas detectadas: {len(df.columns)}</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    ejecutar = st.button("🚀 Ejecutar ETL Completo (Mapeo Multidimensional)", use_container_width=True)

    if ejecutar:
        enviar_evento("etl_ejecutado") 
        barra = st.progress(0)
        
        for nombre, df in st.session_state.archivos.items():
            st.info(f"📥 Limpiando y Transformando datos de: {nombre}")
            
            # --- TRANSFORMACIÓN BÁSICA ---
            df.columns = df.columns.str.strip()
            df = df.drop_duplicates(subset=["id_estudiante"], keep="first")
            df = df.dropna(subset=["id_estudiante"])
            mapa_actividad = {
                 1: "Sedentario",
                 2: "Caminata",
                 3: "Trote",
                 4: "Gimnasio",
                 5: "Deporte"
                 }
            df["actividad_fisica"] = df["actividad_fisica"].replace(mapa_actividad)

            import random
            from datetime import datetime, timedelta
            def generar_fecha_dinamica():
                 f_inicio = datetime(2025,1,1)
                 f_fin = datetime.now()
                 dias = (f_fin-f_inicio).days
                 return f_inicio + timedelta(days=random.randint(0,dias))
            
            fechas_aleatorias = [generar_fecha_dinamica() for _ in range(len(df))]
            ids_tiempo = [int(f.strftime("%Y%m%d")) for f in fechas_aleatorias]
            
            # ----------------------------------------------------------------------
            # 1. CARGA DE DIM_ESTUDIANTE (Paso 25%)
            # ----------------------------------------------------------------------
            try:
                st.text("➡️ Mapeando: dim_estudiante...")
                columnas_est = [
                    'id_estudiante', 'codigo_universitario', 'nombres', 'apellidos', 
                    'edad', 'sexo', 'carrera', 'facultad', 'ciclo', 
                    'fecha_nacimiento', 'estado_matricula'
                ]
                df_estudiante = df[columnas_est].copy()
                df_estudiante.to_sql('dim_estudiante', engine, if_exists='append', index=False)
                st.success("🗄️ Tabla cargada con éxito: dim_estudiante")
            except Exception as e:
                st.error(f"❌ Error en dim_estudiante: {e}")
            barra.progress(0.25)

            # =========================
            # DIM_TIEMPO
            # =========================
            df_tiempo = pd.DataFrame({
                 "id_tiempo": ids_tiempo,
                 "fecha": fechas_aleatorias,
                 "anio":[f.year for f in fechas_aleatorias],
                 "mes":[f.month for f in fechas_aleatorias],
                 "dia":[f.day for f in fechas_aleatorias],
                 "semestre":["I" if f.month<=6 else "II" for f in fechas_aleatorias],
                 "periodo_academico":[f"{f.year}-I" if f.month<=6 else f"{f.year}-II" for f in fechas_aleatorias]
                 })
            df_tiempo=df_tiempo.drop_duplicates()
            
            df_tiempo.to_sql(
                 "dim_tiempo",
                 engine,
                 if_exists="append",
                 index=False
                 )
            st.success("✅ dim_tiempo cargada")

            # =========================
            # DIM_SALUD
            # =========================
            df_salud=pd.DataFrame({
                 "id_salud":[1,2,3,4,5],
                 "estado_emocional":[
                      "Estable","Estresado","Ansioso","Depresivo","Agotado"
                      ],
                "nivel_estres":[
                     "Bajo","Alto","Alto","Muy Alto","Muy Alto"
                     ],
                "nivel_ansiedad":["Bajo","Medio","Alto","Alto","Muy Alto"
                                  ],
                "nivel_depresion":["Bajo","Bajo","Medio","Alto","Muy Alto"
                                   ],
                "motivacion":["Alta","Media","Media","Baja","Muy Baja"
                              ]
                })
            df_salud.to_sql(
                 "dim_salud",
                 engine,
                 if_exists="append",
                 index=False
                 )
            st.success("✅ dim_salud cargada")

            # ----------------------------------------------------------------------
            # 2. CARGA DE FACT_BIENESTAR (Paso 50%) - ¡FECHAS DINÁMICAS AUTOMÁTICAS!
            # ----------------------------------------------------------------------
            try:
                st.text("➡️ Mapeando: fact_bienestar...")
                
                import random
                from datetime import datetime, timedelta

                # Función rápida para inventar fechas entre 2025 y hoy
                def generar_fecha_dinamica():
                    f_inicio = datetime(2025, 1, 1)
                    f_fin = datetime.now()
                    dias_totales = (f_fin - f_inicio).days
                    return f_inicio + timedelta(days=random.randint(0, dias_totales))

                # Generamos una lista de fechas e IDs de tiempo (uno para cada alumno)
                fechas_aleatorias = [generar_fecha_dinamica() for _ in range(len(df))]
                ids_tiempo = [int(f.strftime('%Y%m%d')) for f in fechas_aleatorias]

                mapeo_salud = {
                    'Estable': 1, 'Estresado': 2, 'Ansioso': 3, 
                    'Optimista': 1, 'Depresivo': 4, 'Agotado': 5
                }
                id_salud_serie = df['estado_emocional'].map(mapeo_salud).fillna(1).astype(int)

                df_bienestar = pd.DataFrame({
                    'id_bienestar': range(1, len(df)+1),
                    'id_estudiante': df['id_estudiante'],
                    'nivel_estres_num': df['nivel_estres_num'],
                    'nivel_ansiedad_num': df['nivel_ansiedad_num'],
                    'bienestar_general': df['bienestar_general'],
                    'horas_sueno': df['horas_sueno'],
                    'actividad_fisica': df['actividad_fisica'],
                    'estado_emocional': df['estado_emocional'],
                    'id_salud': id_salud_serie,
                    'id_tiempo': ids_tiempo  # <-- Python le asigna su fecha dinámica aquí
                })
                df_bienestar.to_sql('fact_bienestar', engine, if_exists='append', index=False)
                st.success("🗄️ Tabla cargada con éxito: fact_bienestar")
            except Exception as e:
                st.error(f"❌ Error en fact_bienestar: {e}")
            barra.progress(0.50)

            # ----------------------------------------------------------------------
            # 3. CARGA DE FACT_RENDIMIENTO (Paso 75%) - ¡FECHAS DINÁMICAS AUTOMÁTICAS!
            # ----------------------------------------------------------------------
            try:
                st.text("➡️ Mapeando: fact_rendimiento...")
                
                # Creamos los ciclos académicos (2025-I, 2025-II, etc.) basados en las fechas de arriba
                ciclos_academicos = [
                    f"{f.year}-I" if f.month <= 6 else f"{f.year}-II" 
                    for f in fechas_aleatorias
                ]
                
                df_rendimiento = pd.DataFrame({
                    'id_rendimiento': range(1, len(df)+1),
                    'id_estudiante': df['id_estudiante'],
                    'promedio_general': df['promedio_general'],
                    'asistencia': df['asistencia'],
                    'cursos_aprobados': df['cursos_aprobados'],
                    'cursos_desaprobados': df['cursos_desaprobados'],
                    'creditos_aprobados': df['creditos_aprobados'],
                    'ciclo_academico': ciclos_academicos, # <-- Ciclo real según su fecha
                    'riesgo_academico': df['riesgo_academico'],
                    'id_tiempo': ids_tiempo  # <-- El mismo ID de tiempo para mantener consistencia
                })
                df_rendimiento.to_sql('fact_rendimiento', engine, if_exists='append', index=False)
                st.success("🗄️ Tabla cargada con éxito: fact_rendimiento")
            except Exception as e:
                st.error(f"❌ Error en fact_rendimiento: {e}")
            barra.progress(0.75)
            # ----------------------------------------------------------------------
            # 4. CARGA DE FACT_ACTIVIDAD_FISICA - ¡FECHAS DINÁMICAS!
            # ----------------------------------------------------------------------
            try:
                st.text("➡️ Mapeando: fact_actividad_fisica...")
                
                df_actividad = pd.DataFrame({
                    'id_actividad': range(1, len(df)+1),
                    'id_estudiante': df['id_estudiante'],
                    'tipo_actividad': df['actividad_fisica'],
                    'horas_ejercicio': df['horas_ejercicio'],
                    'frecuencia_semanal': df['frecuencia_semanal'],
                    'id_tiempo': ids_tiempo  # <--- ¡ASEGÚRATE DE QUE ESTA LÍNEA ESTÉ AQUÍ!
                })
                
                df_actividad.to_sql('fact_actividad_fisica', engine, if_exists='append', index=False)
                st.success("🗄️ Tabla cargada con éxito: fact_actividad_fisica")
            except Exception as e:
                st.error(f"❌ Error en fact_actividad_fisica: {e}")
            barra.progress(1.0)

        st.success("🏆 ¡ETL MULTIDIMENSIONAL PROCESADO CON ÉXITO!")
        st.balloons()
        st.session_state.etl_done = True

    if st.button("🗑️ Vaciar Tablas SQL"):
        tablas = ["fact_predicciones", "fact_actividad_fisica", "fact_rendimiento", "fact_bienestar", "dim_salud", "dim_tiempo", "dim_estudiante"]
        try:
            with engine.begin() as conn:
                for tabla in tablas:
                    conn.exec_driver_sql(
                        f"TRUNCATE TABLE {tabla} CASCADE;"
                    )
                
            st.success("✅ Todas las tablas fueron limpiadas correctamente.")
        except Exception as e:
            st.error(f"❌ Error al vaciar base de datos: {e}")
