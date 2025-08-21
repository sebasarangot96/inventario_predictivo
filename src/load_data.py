import pandas as pd
from pathlib import Path
from src.config import RAW_DIR, INTERIM_DIR, FILES

INTERIM_DIR.mkdir(parents=True, exist_ok=True)

# -------- helpers --------
def _to_datetime_safe(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, errors="coerce")

def _to_numeric_safe(s: pd.Series) -> pd.Series:
    return pd.to_numeric(
        s.astype(str).str.replace(r"[,$]", "", regex=True), errors="coerce"
    )

def read_csv_safe(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8", low_memory=False)

def save_interim(df: pd.DataFrame, name: str):
    df.to_parquet(INTERIM_DIR / f"{name}.parquet", index=False)
    df.to_csv(INTERIM_DIR / f"{name}.csv", index=False)

# -------- estandarización --------
def _standardize_sales(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "SalesDate": "InvoiceDate",
        "SalesQuantity": "Quantity",
        "SalesPrice": "UnitPrice",
        "SalesDollars": "TotalAmount",
        # opcionales: mantiene consistencia
        "InventoryId": "InventoryId",
        "Store": "Store",
        "Brand": "Brand",
        "Description": "ProductName",
        "Size": "Size",
        "Volume": "Volume",
        "Classification": "Classification",
        "ExciseTax": "ExciseTax",
        "VendorNo": "VendorId",
        "VendorName": "VendorName",
    }
    df = df.rename(columns=rename_map)

    # tipados
    if "InvoiceDate" in df: df["InvoiceDate"] = _to_datetime_safe(df["InvoiceDate"])
    for col in ("Quantity", "UnitPrice", "TotalAmount"):
        if col in df: df[col] = _to_numeric_safe(df[col])

    return df


def _standardize_purchases(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "InvoiceDate": "InvoiceDate",
        "Quantity": "Quantity",
        "PurchasePrice": "UnitPrice",
        "Dollars": "TotalAmount",
        "PONumber": "InvoiceNo",   # usamos PONumber como ID de factura
        # extras para consistencia
        "InventoryId": "InventoryId",
        "Store": "Store",
        "Brand": "Brand",
        "Description": "ProductName",
        "Size": "Size",
        "VendorNumber": "VendorId",
        "VendorName": "VendorName",
        "PODate": "PODate",
        "ReceivingDate": "ReceivingDate",
        "PayDate": "PayDate",
        "Classification": "Classification",
    }
    df = df.rename(columns=rename_map)

    # tipados
    if "InvoiceDate" in df: df["InvoiceDate"] = _to_datetime_safe(df["InvoiceDate"])
    for col in ("Quantity", "UnitPrice", "TotalAmount"):
        if col in df: df[col] = _to_numeric_safe(df[col])

    return df

# -------- main --------
def main():
    # PRICES
    prices = read_csv_safe(RAW_DIR / FILES["prices"])
    save_interim(prices, "prices")

    # INVENTARIOS
    inv_beg = read_csv_safe(RAW_DIR / FILES["inv_beg"])
    inv_end = read_csv_safe(RAW_DIR / FILES["inv_end"])
    save_interim(inv_beg, "inventory_beg")
    save_interim(inv_end, "inventory_end")

    # INVOICES (purchases header)
    invoices = read_csv_safe(RAW_DIR / FILES["invoices"])
    invoices = _standardize_purchases(invoices)
    save_interim(invoices, "invoice_purchases")

    # PURCHASES (purchases detail)
    purchases = read_csv_safe(RAW_DIR / FILES["purchases"])
    purchases = _standardize_purchases(purchases)
    save_interim(purchases, "purchases")

    # SALES
    sales = read_csv_safe(RAW_DIR / FILES["sales"])
    sales = _standardize_sales(sales)
    save_interim(sales, "sales")

    print("✅ Todos los datos cargados, estandarizados y guardados en data/interim/")

if __name__ == "__main__":
    main()