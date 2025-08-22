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

Proyecto de **limpieza, estandarización y preparación de datos** para una empresa ficticia de distribución de **licores**.  
El objetivo es dejar datasets **confiables y reproducibles** para análisis, dashboard y modelos de **pronóstico de demanda / optimización de inventario**.

**Entregables principales**
- CSVs limpios en `data/processed/` (ventas, compras, invoices, inventarios, precios)
- Diccionarios de datos por cada tabla procesada
- Notebooks de validación y EDA
- Pipeline de transformación en `src/transform_template.py`

---

## 📚 Tabla de contenidos
- [Descripción](#-descripción)
- [Stack](#-stack)
- [Estructura del repositorio](#-estructura-del-repositorio)
- [Instalación y uso (rápido)](#-instalación-y-uso-rápido)
- [Generación de datos limpios](#-generación-de-datos-limpios)
- [Notas sobre los datos](#-notas-sobre-los-datos)

---

## 🧰 Stack
- **Python** (pandas, numpy, jupyter)
- **Git/GitHub**
- **Power BI** (o herramienta BI equivalente para dashboard)

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
│  └─ transform_template.py
├─ README.md
└─ requirements.txt

---

⚙️ Instalación y uso (rápido)

```bash
1) Clonar
git clone https://github.com/sebasarangot96/inventario_predictivo.git
cd inventario_predictivo

2) Entorno
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

🧹 Generación de datos limpios

El proyecto incluye un **pipeline de limpieza y estandarización** que transforma los archivos crudos en `data/raw/` hacia archivos procesados en `data/processed/`.

Pasos principales

### Generación de datos limpios

El proyecto incluye un **pipeline de limpieza y estandarización** que transforma los archivos crudos en `data/raw/` hacia archivos procesados en `data/processed/`.

#### Pasos principales
1. **Activar el entorno virtual**
   ```bash
   source .venv/bin/activate    # en Mac/Linux
   .venv\Scripts\activate       # en Windows

Ejecutar el pipeline de transformación
python -m src.transform_template

Ejecutar el generador de muestras
python -m src.make_samples

📂 Importante sobre los datos
	•	Los archivos completos en data/processed/ no se versionan en GitHub (por su tamaño).
	•	En su lugar, incluimos muestras reducidas en data/sample/ para que cualquier persona pueda explorar el contenido rápidamente.
	•	Estas muestras contienen:
	•	Las primeras 1000 filas (*.head1000.csv)
	•	1000 filas aleatorias (*.sample1000.csv)






