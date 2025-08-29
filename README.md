<p align="center">
  <img src="docs/assets/image00.png" alt="Prueba" width="200">
</p>

<h1 align="center">Inventario Predictivo — Licores Andinos</h1>

<p align="center">
  <a href="https://github.com/sebasarangot96/inventario_predictivo"><img src="https://img.shields.io/github/last-commit/sebasarangot96/inventario_predictivo" alt="last commit"></a>
  <a href="https://github.com/sebasarangot96/inventario_predictivo/issues"><img src="https://img.shields.io/github/issues/sebasarangot96/inventario_predictivo" alt="issues"></a>
  <a href="#"><img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="python"></a>
  <a href="#"><img src="https://img.shields.io/badge/pandas-yes-150458" alt="pandas"></a>
</p>

---

## 📌 Descripción

Proyecto de análisis y optimización de inventarios para la empresa ficticia **Licores Andinos**.  
El flujo de trabajo integra **limpieza de datos, automatización de ingesta en BigQuery, dashboards interactivos en Power BI** y un **módulo de proyección con Machine Learning**.

---

## 📚 Tabla de contenidos
- [Stack](#-stack)
- [Estructura del repositorio](#-estructura-del-repositorio)
- [Procesos](#-procesos)
  - [1. Limpieza y estandarización de datos](#1-limpieza-y-estandarización-de-datos)
  - [2. Automatización de carga a BigQuery](#2-automatización-de-carga-a-bigquery)
  - [3. Creación de dashboard en Power BI](#3-creación-de-dashboard-en-power-bi)
  - [4. Proyección con Machine Learning + Streamlit](#4-proyección-con-machine-learning--streamlit)
- [Notas sobre los datos](#-notas-sobre-los-datos)

---

## 🧰 Stack
- **Python** (pandas, numpy, scikit-learn, jupyter)
- **Google Cloud BigQuery**
- **Power BI**
- **Streamlit**
- **Git/GitHub**

---

## 🗂️ Estructura del repositorio

inventario_predictivo/  
├─ data/  
│  ├─ raw/         # CSV originales (no versionados completos)  
│  ├─ interim/     # resultados intermedios  
│  └─ processed/   # CSV limpios + diccionarios (artefactos finales)  
├─ notebooks/  
│  ├─ 00_check.ipynb  
│  └─ 01_cleaning.ipynb  
├─ src/  
│  ├─ load_data.py  
│  ├─ transform_template.py  
│  └─ ml_forecast.py  
├─ README.md  
└─ requirements.txt  

---

## ⚙️ Procesos

### 1. Limpieza y estandarización de datos
- Revisión de consistencia y duplicados.  
- Estandarización de nombres de columnas y formatos de fecha.  
- Generación de diccionarios de datos por tabla.  
- Creación de datasets procesados en `data/processed/`.  

### 2. Automatización de carga a BigQuery
- Implementación de un script en Python que conecta Google Drive con BigQuery.  
- Actualización automática de tablas (detección de nuevas filas y cambios).  
- Uso de `pydrive2`, `pandas` y `google-cloud-bigquery`.  

### 3. Creación de dashboard en Power BI
- Conexión a BigQuery como fuente de datos.  
- Definición de KPIs:  
  - Rotación de inventario  
  - Cobertura de inventario  
  - Margen bruto  
  - Tiempo de entrega promedio  
  - Clasificación ABC de productos  
- Visualizaciones interactivas para soporte en decisiones de compra y distribución.  

### 4. Proyección con Machine Learning + Streamlit
- Modelos de predicción de demanda usando **scikit-learn** (ejemplo: regresión, ARIMA o Random Forest).  
- Generación de escenarios futuros de ventas e inventario.  
- Aplicación web en **Streamlit** para explorar resultados y simulaciones.  

---

## 📂 Notas sobre los datos
- Los archivos completos en `data/processed/` no se versionan en GitHub (por su tamaño).  
- Se incluyen muestras reducidas en `data/sample/` para exploración rápida:  
  - Primeras 1000 filas (`*.head1000.csv`)  
  - 1000 filas aleatorias (`*.sample1000.csv`)  

---
