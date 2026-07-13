# Plataforma Integral de Analítica Universitaria

## Descripción

Proyecto desarrollado como una plataforma de analítica universitaria que integra Business Intelligence (BI), Big Data e Inteligencia Artificial Ética para mejorar el análisis del bienestar físico y mental estudiantil.

La plataforma permite:

- Carga de datos académicos y de bienestar.
- Procesamiento ETL para limpieza y transformación de información.
- Modelo dimensional Snowflake para análisis multidimensional.
- Visualización de KPIs universitarios.
- Predicciones mediante modelos de Inteligencia Artificial.
- Dashboard de analítica con Looker Studio.
- Preparación de métricas para Analítica Web con Google Analytics 4.

## Tecnologías utilizadas

- Python
- Streamlit
- PostgreSQL
- SQLAlchemy
- Pandas
- Plotly
- Scikit-learn
- Looker Studio
- Google Analytics 4

## Estructura del proyecto
assets/
Recursos visuales de la aplicación

backend/
Conexión y lógica de acceso a datos

vistas/
Módulos de la plataforma

app.py
Archivo principal de ejecución

requirements.txt
Librerías necesarias

## Configuración

Las credenciales de conexión a la base de datos se gestionan mediante variables de entorno (`.env`) y no se publican en el repositorio.