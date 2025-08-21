# src/transform_template.py
from pathlib import Path
from shutil import copyfile
import re
import pandas as pd

# ===================== utilidades comunes =====================

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
                  .str.lower()
                  .str.replace(r"\s+", "_", regex=True)
                  .str.replace("[^a-z0-9_]", "", regex=True)
    )
    return df

def normalize_text(s: pd.Series) -> pd.Series:
    return (s.astype(str)
              .str.strip()
              .str.replace(r"\s+", " ", regex=True))

def normalize_brand(s: pd.Series) -> pd.Series:
    return normalize_text(s).str.upper()

def normalize_classification(s: pd.Series) -> pd.Series:
    return normalize_text(s).str.upper()

def size_to_ml(val):
    """Convierte '750mL','1.5L','12oz' -> mililitros. Si no reconoce, None."""
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

def safe_to_numeric_series(s: pd.Series) -> pd.Series:
    s = normalize_text(s)
    s = s.str.replace(r"[,$]", "", regex=True)
    return pd.to_numeric(s, errors="coerce")

def coerce_numeric_by_name(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte a numérico columnas que 'parecen' numéricas por nombre."""
    num_hints = ("qty", "quantity", "units", "price", "cost", "amount",
                 "total", "volume", "onhand", "on_hand", "cases", "unitprice")
    for c in df.columns:
        if any(h in c for h in num_hints):
            try:
                df[c] = safe_to_numeric_series(df[c])
            except Exception:
                pass
    return df

def parse_possible_dates(df: pd.DataFrame) -> pd.DataFrame:
    for c in df.columns:
        if "date" in c:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    return df

def write_outputs(df: pd.DataFrame, out_base: Path, base_name: str):
    out_csv = out_base / f"{base_name}.csv"
    df.to_csv(out_csv, index=False)
    try:
        df.to_parquet(out_base / f"{base_name}.parquet", index=False)
    except Exception:
        pass
    dd = pd.DataFrame({
        "column": df.columns,
        "dtype": [str(t) for t in df.dtypes],
        "nulls": df.isna().sum().values
    })
    dd.to_csv(out_base / f"{base_name}_dictionary.csv", index=False)
    return out_csv

def ensure_interim_file(interim: Path, raw: Path, raw_name: str, interim_name: str) -> Path | None:
    """
    Devuelve la ruta en interim. Si no existe, intenta copiar desde raw con el nombre estandarizado.
    """
    dst = interim / interim_name
    if dst.exists():
        return dst
    src = raw / raw_name
    if src.exists():
        interim.mkdir(parents=True, exist_ok=True)
        copyfile(src, dst)
        print(f"ℹ️ Copié {src} → {dst}")
        return dst
    print(f"⚠️ No encontré ni {dst} ni {src}")
    return None

# ===================== transforms =====================

def transform_sales(interim: Path, processed: Path):
    src = interim / "sales.csv"
    if not src.exists():
        print(f"⚠️ No encontré {src} (salto ventas)")
        return
    df = pd.read_csv(src)
    before = len(df)

    df = normalize_columns(df)
    if "brand" in df.columns: df["brand"] = normalize_brand(df["brand"])
    if "classification" in df.columns: df["classification"] = normalize_classification(df["classification"])
    if "description" in df.columns: df["description"] = normalize_text(df["description"])
    if "size" in df.columns: df["size_ml"] = df["size"].apply(size_to_ml)

    df = coerce_numeric_by_name(df)
    df = parse_possible_dates(df)
    df = df.drop_duplicates()
    dropped = before - len(df)

    out_csv = write_outputs(df, processed, "sales_clean")
    print(f"✅ sales: {before} -> {len(df)} (quitadas {dropped}) | {out_csv}")

def transform_purchases(interim: Path, processed: Path):
    src = interim / "purchases.csv"
    if not src.exists():
        print(f"⚠️ No encontré {src} (salto compras)")
        return
    df = pd.read_csv(src)
    before = len(df)

    df = normalize_columns(df)
    for col in ("brand", "classification", "description", "vendorname"):
        if col in df.columns:
            if col == "brand":
                df[col] = normalize_brand(df[col])
            elif col == "classification":
                df[col] = normalize_classification(df[col])
            else:
                df[col] = normalize_text(df[col])
    if "size" in df.columns: df["size_ml"] = df["size"].apply(size_to_ml)

    df = coerce_numeric_by_name(df)
    df = parse_possible_dates(df)
    df = df.drop_duplicates()
    dropped = before - len(df)

    out_csv = write_outputs(df, processed, "purchases_clean")
    print(f"✅ purchases: {before} -> {len(df)} (quitadas {dropped}) | {out_csv}")

def transform_invoice_purchases(interim: Path, processed: Path, raw: Path):
    # Estándar: data/interim/invoice_purchases.csv
    src = ensure_interim_file(
        interim=interim,
        raw=raw,
        raw_name="InvoicePurchases12312016.csv",
        interim_name="invoice_purchases.csv",
    )
    if not src:
        print("⚠️ Salto invoice_purchases (no hay fuente)")
        return

    print(f"→ Ejecutando transform_invoice_purchases. Fuente: {src}")
    df = pd.read_csv(src)
    before = len(df)

    df = normalize_columns(df)
    for col in ("brand", "classification", "description", "vendorname"):
        if col in df.columns:
            if col == "brand":
                df[col] = normalize_brand(df[col])
            elif col == "classification":
                df[col] = normalize_classification(df[col])
            else:
                df[col] = normalize_text(df[col])

    df = coerce_numeric_by_name(df)
    df = parse_possible_dates(df)
    df = df.drop_duplicates()
    dropped = before - len(df)

    out_csv = write_outputs(df, processed, "invoice_purchases_clean")
    print(f"✅ invoice_purchases: {before} -> {len(df)} (quitadas {dropped}) | {out_csv}")

def transform_inventory(interim: Path, processed: Path, kind: str):
    """
    kind: 'beg' o 'end'
    Lee 'inventory_beg.csv' / 'inventory_end.csv'
    """
    fname = f"inventory_{kind}.csv"
    src = interim / fname
    if not src.exists():
        print(f"⚠️ No encontré {src} (salto inventario {kind})")
        return
    df = pd.read_csv(src)
    before = len(df)

    df = normalize_columns(df)
    # textos suaves
    for col in ("brand", "description", "classification", "vendorname"):
        if col in df.columns:
            df[col] = normalize_text(df[col])

    df = coerce_numeric_by_name(df)
    df = parse_possible_dates(df)
    df = df.drop_duplicates()
    dropped = before - len(df)

    out_csv = write_outputs(df, processed, f"inventory_{kind}_clean")
    print(f"✅ inventory_{kind}: {before} -> {len(df)} (quitadas {dropped}) | {out_csv}")

def transform_prices(interim: Path, processed: Path, raw: Path):
    """
    Precios de compra. Estandar: 'prices.csv' en interim.
    Si no existe, intenta copiar de raw '2017PurchasePricesDec.csv'.
    """
    src = ensure_interim_file(
        interim=interim,
        raw=raw,
        raw_name="2017PurchasePricesDec.csv",
        interim_name="prices.csv",
    )
    if not src:
        print("⚠️ Salto prices (no hay fuente)")
        return

    df = pd.read_csv(src)
    before = len(df)

    df = normalize_columns(df)
    for col in ("brand", "description", "classification", "vendorname"):
        if col in df.columns:
            df[col] = normalize_text(df[col])

    df = coerce_numeric_by_name(df)   # price, cost, unitprice, etc.
    df = parse_possible_dates(df)
    df = df.drop_duplicates()
    dropped = before - len(df)

    out_csv = write_outputs(df, processed, "prices_clean")
    print(f"✅ prices: {before} -> {len(df)} (quitadas {dropped}) | {out_csv}")

# ===================== main =====================

def main():
    root = Path(".")
    raw = root / "data" / "raw"
    interim = root / "data" / "interim"
    processed = root / "data" / "processed"
    processed.mkdir(parents=True, exist_ok=True)

    transform_sales(interim, processed)
    transform_purchases(interim, processed)
    transform_invoice_purchases(interim, processed, raw)
    transform_inventory(interim, processed, "beg")
    transform_inventory(interim, processed, "end")
    transform_prices(interim, processed, raw)

if __name__ == "__main__":
    main()