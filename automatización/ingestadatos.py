from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from google.cloud import bigquery
import pandas as pd
import json, io, os, datetime

# -----------------------------
# CONFIGURACIÓN
# -----------------------------
CARPETA_ID = "1gCiGcKsAhE5M3qJeQzk3c0VZDNQYZqkT"    # Carpeta en Drive con los CSV
ARCHIVO_LOG = "registro_ingesta.json"               # Registro de última fila cargada por archivo
PROYECTO_ID = "cedar-freedom-437421-h8"             # ID del proyecto en Google Cloud
CONJUNTO_DATOS = "inventory"                        # Dataset en BigQuery
RUTA_CREDENCIALES = "key.json"                      # Credenciales de Service Account
# -----------------------------

# Autenticación con Google Drive
autenticacion = GoogleAuth()
autenticacion.LocalWebserverAuth()
drive = GoogleDrive(autenticacion)

# Cliente de BigQuery
cliente_bq = bigquery.Client.from_service_account_json(RUTA_CREDENCIALES, project=PROYECTO_ID)

# Cargar log de filas ya procesadas
if os.path.exists(ARCHIVO_LOG):
    with open(ARCHIVO_LOG, "r") as f:
        registro = json.load(f)
else:
    registro = {}

# Listar archivos CSV en la carpeta de Drive
archivos = drive.ListFile({'q': f"'{CARPETA_ID}' in parents and trashed=false"}).GetList()

for archivo in archivos:
    if not archivo['title'].endswith(".csv"):
        continue

    archivo_id = archivo['id']
    nombre_archivo = archivo['title']
    nombre_tabla = nombre_archivo.replace(".csv", "").lower()  # Nombre de tabla = nombre del archivo

    print(f"🔍 Revisando archivo: {nombre_archivo} → tabla: {nombre_tabla}")

    # Descargar contenido del archivo desde Drive
    contenido = archivo.GetContentString()
    df = pd.read_csv(io.StringIO(contenido))

    # Normalizar nombres de columnas
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Revisar cuántas filas ya cargamos
    filas_previas = registro.get(archivo_id, 0)

    if len(df) != filas_previas:
        print(f"🔄 Cambios detectados en {nombre_archivo} (antes {filas_previas} filas, ahora {len(df)})")

        # Reemplazar tabla completa en BigQuery
        tabla_ref = f"{PROYECTO_ID}.{CONJUNTO_DATOS}.{nombre_tabla}"

        job = cliente_bq.load_table_from_dataframe(
            df,
            tabla_ref,
            job_config=bigquery.LoadJobConfig(
                write_disposition="WRITE_TRUNCATE"  # Sobrescribir tabla completa
            )
        )
        job.result()  # Esperar a que termine
        print(f"✅ Tabla {tabla_ref} actualizada con {len(df)} filas")

        # Actualizar registro
        registro[archivo_id] = len(df)
    else:
        print(f"⏩ Sin cambios detectados en {nombre_archivo}")

# Guardar log actualizado
with open(ARCHIVO_LOG, "w") as f:
    json.dump(registro, f, indent=2)

print(f"[{datetime.datetime.now()}] Ingesta finalizada ✅")
