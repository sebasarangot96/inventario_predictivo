# src/transform_template.py
from pathlib import Path
import pandas as pd
import re

# ---------- utilidades ----------
def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
                  .str.lower()
                  .str.replace(r"\s+", "_", regex=True)
                  .str.replace("[^a-z0-9_]", "", regex=True)
    )
    return df

def normalize_brand(s: pd.Series) -> pd.Series:
    return (s.astype(str)
              .str.strip()
              .str.replace(r"\s+", " ", regex=True)
              .str.upper())

def normalize_classification(s: pd.Series) -> pd.Series:
    return (s.astype(str)
              .str.strip()
              .str.replace(r"\s+", " ", regex=True)
              .str.upper())

def size_to_ml(val):
    if pd.isna(val):
        return None
    v = str(val).strip().lower().replace(" ", "")
    m = re.fullmatch(r"(\d+(\.\d+)?)l", v)
    if m:
        return float(m.group(1)) * 1000
    m = re.fullmatch(r"(\d+(\.\d+)?)ml", v)
    if m:
        return float(m.group(1))
    m = re.fullmatch(r"(\d+(\.\d+)?)oz", v)
    if m:
        return float(m.group(1)) * 29.57
    return None

# ---------- pipeline ----------
def main():
    root = Path(".")
    interim = root / "data" / "interim"
    processed = root / "data" / "processed"
    processed.mkdir(parents=True, exist_ok=True)

    # 1) leer dataset estandarizado por load_data
    src_file = interim / "sales.csv"
    if not src_file.exists():
        print(f"⚠️ No encontré {src_file}. ¿Corristes 'python -m src.load_data'?")
        return

    df = pd.read_csv(src_file)

    # 2) normalizar nombres
    df = normalize_columns(df)

    # 3) normalizar texto clave
    if "brand" in df.columns:
        df["brand"] = normalize_brand(df["brand"])
    if "classification" in df.columns:
        df["classification"] = normalize_classification(df["classification"])
    if "description" in df.columns:
        df["description"] = df["description"].astype(str).str.strip()

    # 4) size -> size_ml
    if "size" in df.columns:
        df["size_ml"] = df["size"].apply(size_to_ml)

    # 5) tipos numéricos seguros
    for c in ["salesquantity", "salesdollars", "salesprice", "volume"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # 6) fecha
    if "salesdate" in df.columns:
        df["salesdate"] = pd.to_datetime(df["salesdate"], errors="coerce")

    # 7) duplicados exactos fuera
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    dropped = before - after

    # 8) guardar
    out_csv = processed / "sales_clean.csv"
    df.to_csv(out_csv, index=False)
    try:
        df.to_parquet(processed / "sales_clean.parquet", index=False)
    except Exception as e:
        print("Parquet no disponible (ok):", e)

    # 9) mini data dictionary (útil para el README)
    dict_out = processed / "sales_clean_dictionary.csv"
    dd = pd.DataFrame({
        "column": df.columns,
        "dtype": [str(t) for t in df.dtypes],
        "nulls": df.isna().sum().values
    })
    dd.to_csv(dict_out, index=False)

    print("✅ Transform listo")
    print(f" - Filas antes/after: {before} -> {after} (quitadas {dropped})")
    print(f" - CSV: {out_csv}")
    print(f" - Diccionario: {dict_out}")

if __name__ == "__main__":
    main()