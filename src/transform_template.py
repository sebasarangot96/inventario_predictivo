# src/transform_template.py
from pathlib import Path
import pandas as pd

def main():
    # carpetas de entrada y salida
    interim = Path("data/interim")
    out = Path("data/processed")
    out.mkdir(parents=True, exist_ok=True)

    # ejemplo: tomar un archivo de ventas ya estandarizado
    src_file = interim / "sales.csv"
    if not src_file.exists():
        print(f"⚠️ No encontré {src_file}, revisa los nombres en data/interim/")
        return

    # 1) Leer el archivo
    df = pd.read_csv(src_file)

    # 2) Limpieza sencilla
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]  # normaliza nombres
    df = df.drop_duplicates()  # elimina duplicados

    # 3) Guardar resultados
    df.to_csv(out / "sales_clean.csv", index=False)
    try:
        df.to_parquet(out / "sales_clean.parquet", index=False)
    except Exception as e:
        print("No se pudo guardar en parquet:", e)

    print("✅ Transform listo. Archivos creados en data/processed/")

if __name__ == "__main__":
    main()