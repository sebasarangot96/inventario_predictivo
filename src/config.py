from pathlib import Path

# Ruta raíz del proyecto (carpeta que contiene /data y /src)
ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"

FILES = {
    "prices": "2017PurchasePricesDec.csv",
    "inv_beg": "BegInvFINAL12312016.csv",
    "inv_end": "EndInvFINAL12312016.csv",
    "invoices": "InvoicePurchases12312016.csv",
    "purchases": "PurchasesFINAL12312016.csv",
    "sales": "SalesFINAL12312016.csv",
}