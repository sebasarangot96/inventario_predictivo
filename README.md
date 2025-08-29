<p align="center">
  <img src="docs/assets/image00.png" alt="Licores Andinos" width="220">
</p>

<h1 align="center">Inventario Predictivo — Licores Andinos</h1>

<p align="center">
  <a href="https://github.com/sebasarangot96/inventario_predictivo"><img src="https://img.shields.io/github/last-commit/sebasarangot96/inventario_predictivo" alt="last commit"></a>
  <a href="https://github.com/sebasarangot96/inventario_predictivo/issues"><img src="https://img.shields.io/github/issues/sebasarangot96/inventario_predictivo" alt="issues"></a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="python">
  <img src="https://img.shields.io/badge/pandas-yes-150458" alt="pandas">
  <img src="https://img.shields.io/badge/BigQuery-ready-4285F4" alt="bigquery">
  <img src="https://img.shields.io/badge/Power%20BI-dashboard-F2C811" alt="powerbi">
  <img src="https://img.shields.io/badge/scikit--learn-ML-FF9F1C" alt="sklearn">
  <img src="https://img.shields.io/badge/Streamlit-app-FF4B4B" alt="streamlit">
</p>

---

## 📌 Descripción

Proyecto de **limpieza, estandarización y preparación de datos** para una empresa ficticia de distribución de licores.  
El pipeline termina en **BigQuery**, desde donde se alimenta un **dashboard en Power BI**.  
Como **extra**, se incluye un **pronóstico de demanda** (scikit-learn) publicado con **Streamlit**.

**Entregables**
- CSVs limpios en `data/processed/` (ventas, compras, inventario, precios, invoices)
- Script de ingesta incremental/sincronización: **Google Drive → BigQuery**
- Dataset en BigQuery (tablas por archivo)
- Dashboard en Power BI conectado a BigQuery
- App de pronóstico (Streamlit) + notebook de entrenamiento (scikit-learn)

---

## 🗺️ Roadmap del Proyecto

Limpieza (Python + Pandas)

Automatización de carga (Google Drive → BigQuery)

Visualización (Power BI)

Extra: ML (scikit-learn) + Streamlit

markdown
Copiar código

---

## 📚 Tabla de contenidos
- [Stack](#-stack)
- [Estructura del repositorio](#-estructura-del-repositorio)
- [Instalación rápida](#-instalación-rápida)
- [1) Limpieza y estandarización](#1-limpieza-y-estandarización)
- [2) Automatización Drive → BigQuery](#2-automatización-drive--bigquery)
- [3) Dashboard en Power BI](#3-dashboard-en-power-bi)
- [4) Extra: Pronóstico ML + Streamlit](#4-extra-pronóstico-ml--streamlit)
- [KPIs y análisis avanzados](#kpis-y-análisis-avanzados)
- [Notas sobre datos y permisos](#notas-sobre-datos-y-permisos)

---

## 🧰 Stack
- **Python**: pandas, numpy, pyarrow, google-cloud-bigquery, pydrive2
- **BigQuery (GCP)**: dataset `inventory`
- **Power BI**: conexión directa a BigQuery
- **ML**: scikit-learn (forecast base), joblib
- **App**: Streamlit

---

## 🗂️ Estructura del repositorio

inventario_predictivo/
├─ data/
│ ├─ raw/ # CSV originales (no versionados completos)
│ ├─ interim/ # resultados intermedios
│ ├─ processed/ # CSV limpios (artefactos finales)
│ └─ sample/ # muestras (head1000 / sample1000)
├─ notebooks/
│ ├─ 00_eda.ipynb
│ ├─ 01_cleaning.ipynb
│ └─ 02_ml_forecast.ipynb
├─ src/
│ ├─ transform_template.py # limpieza y estandarización
│ ├─ drive_to_bq.py # ingesta/sync Drive → BigQuery
│ ├─ utils_io.py # helpers de IO y validación
│ └─ ml/
│ ├─ train.py # entrenamiento scikit-learn
│ └─ features.py # construcción de features
├─ app/
│ └─ streamlit_app.py # interfaz Streamlit (pronóstico)
├─ docs/
│ └─ assets/ # imágenes para README
├─ .env.example # variables de entorno (plantilla)
├─ requirements.txt
└─ README.md

yaml
Copiar código

---

## ⚙️ Instalación rápida

```bash
# 1) Clonar
git clone https://github.com/sebasarangot96/inventario_predictivo.git
cd inventario_predictivo

# 2) Entorno
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# 3) Dependencias
pip install -r requirements.txt
Configura credenciales:

key.json (Service Account GCP) → raíz del repo

client_secrets.json (OAuth para Drive) → raíz del repo

Copia .env.example a .env y completa (si aplica).

1) Limpieza y estandarización
Normalización de nombres de columnas (snake_case)

Cast de tipos, manejo de nulos y duplicados

Conformidad entre tablas (dimensiones y hechos)

Export a data/processed/

Ejecutar:

bash
Copiar código
python -m src.transform_template
Validación (opcional en notebooks):

bash
Copiar código
jupyter lab
# abrir notebooks/01_cleaning.ipynb
2) Automatización Drive → BigQuery
Objetivo: sincronizar automáticamente tus CSV de una carpeta de Google Drive con tablas en BigQuery (una tabla por archivo).

Si cambian filas (se agregan o se borran) → reemplaza la tabla completa (WRITE_TRUNCATE) para mantener espejo 1:1.

Registro local registro_ingesta.json para detectar cambios y evitar cargas innecesarias.

Ejecutar:

bash
Copiar código
python -m src.drive_to_bq
Automatización diaria

Windows Task Scheduler: ejecutar script cada 24h

Cloud Scheduler + Cloud Run/Functions (opcional en GCP)

3) Dashboard en Power BI
Conectar a BigQuery
Power BI Desktop → Obtener datos → Google BigQuery → seleccionar el proyecto/dataset

Modelo estrella (sugerido)

Hechos: ventas, compras, inventario

Dimensiones: productos, clientes, proveedores, calendario

KPIs recomendados

Ventas totales, Unidades, Margen, Rotación, Stock actual, Fill rate, On-time delivery, etc.

Páginas recomendadas

Executive: ventas, margen, rotación, top productos

Inventario: stock vs ROP, roturas, ABC

Logística: lead time, % entregas a tiempo

Finanzas: costo mantenimiento, GMROI

4) Extra: Pronóstico ML + Streamlit
4.1 Entrenamiento (scikit-learn)
Serie: ventas mensuales por producto/categoría

Features: lags, medias móviles, estacionalidad, dummies de mes

Modelo sugerido: RandomForestRegressor o XGBoost

Entrenar:

bash
Copiar código
python -m src.ml.train
4.2 App (Streamlit)
Input: Producto/Categoría, horizonte, escenario

Output: pronóstico + intervalo, curva histórica vs proyectada, métricas

Ejecutar:

bash
Copiar código
streamlit run app/streamlit_app.py
📈 KPIs y análisis avanzados
Ventas

Ventas Totales, Unidades Vendidas, Precio Promedio

Rentabilidad

Margen Bruto, % Margen

Inventario

Stock Actual, Valor de Inventario, Rotación

ABC (ventas por producto)
Clasificación A/B/C según % acumulado de ventas

Punto de Reorden (ROP)

𝑅
𝑂
𝑃
=
𝑑
𝑒
𝑚
𝑎
𝑛
𝑑
𝑎
_
𝑑
𝑖
𝑎
𝑟
𝑖
𝑎
×
𝑙
𝑒
𝑎
𝑑
_
𝑡
𝑖
𝑚
𝑒
+
seguridad
ROP=demanda_diaria×lead_time+seguridad
EOQ (Cantidad Económica de Pedido)

𝐸
𝑂
𝑄
=
2
𝐷
𝑆
𝐻
EOQ= 
H
2DS
​
 
​
 
🗒️ Notas sobre datos y permisos
Los CSV completos en data/processed/ no se versionan (tamaño)

En su lugar, se incluyen muestras en data/sample/:

*.head1000.csv (primeras 1000 filas)

*.sample1000.csv (1000 filas aleatorias)

BigQuery:

Dataset por defecto: inventory

Tablas creadas automáticamente a partir del nombre del archivo

Permisos de BigQuery:

Compartir con usuarios específicos (recomendado)

Público de solo lectura: añadir allUsers con rol BigQuery Data Viewer ⚠️

✅ Checklist de entrega
 Limpieza reproducible (src/transform_template.py) y artefactos en data/processed/

 Ingesta Drive → BigQuery funcionando (src/drive_to_bq.py)

 Automatización diaria (Task Scheduler/Cloud Scheduler)

 Dashboard en Power BI conectado a BigQuery

 Notebook y script ML (notebooks/02_ml_forecast.ipynb, src/ml/train.py)

 App Streamlit (app/streamlit_app.py) corriendo local
