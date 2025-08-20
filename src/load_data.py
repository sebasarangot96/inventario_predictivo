import pandas as pd
from pathlib import Path
from src.config import RAW_DIR, INTERIM_DIR, FILES

INTERIM_DIR.mkdir(parents=True, exist_ok=True)

def read_csv_safe(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8", low_memory=False)

def save_interim(df: pd.DataFrame, name: str):
    df.to_parquet(INTERIM_DIR / f"{name}.parquet", index=False)
    df.to_csv(INTERIM_DIR / f"{name}.csv", index=False)

def main():
    # PRICES
    prices = read_csv_safe(RAW_DIR / FILES["prices"])
    save_interim(prices, "prices")

    # INVENTARIO INICIAL / FINAL
    inv_beg = read_csv_safe(RAW_DIR / FILES["inv_beg"])
    inv_end = read_csv_safe(RAW_DIR / FILES["inv_end"])
    save_interim(inv_beg, "inventory_beg")
    save_interim(inv_end, "inventory_end")

    # INVOICES
    invoices = read_csv_safe(RAW_DIR / FILES["invoices"])
    save_interim(invoices, "invoice_purchases")

    # PURCHASES
    purchases = read_csv_safe(RAW_DIR / FILES["purchases"])
    save_interim(purchases, "purchases")

    # SALES
    sales = read_csv_safe(RAW_DIR / FILES["sales"])
    save_interim(sales, "sales")

    print("✅ Todos los datos cargados y guardados en data/interim/")


if __name__ == "__main__":
    main()