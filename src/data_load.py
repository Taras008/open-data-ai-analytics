from pathlib import Path
import sqlite3
import pandas as pd
import urllib.request

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
DB_DIR = Path("db")

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
DB_DIR.mkdir(parents=True, exist_ok=True)

XLSX_URL = "https://data.gov.ua/dataset/d2e7708a-e121-4607-b600-525117cdca6c/resource/d8a12813-3b88-47f8-8b05-06e3a008553e/download/95-naiavnii-dokhid-naselennia-po-regionakh-mln-grn.xlsx"
raw_xlsx_path = RAW_DIR / "income_by_region.xlsx"
processed_csv_path = PROCESSED_DIR / "income_by_region_clean.csv"
db_path = DB_DIR / "income.db"

def download(url: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        print(f"Already downloaded: {dest}")
        return
    print(f"Downloading -> {dest}")
    urllib.request.urlretrieve(url, dest)

def main():
    download(XLSX_URL, raw_xlsx_path)

    df = pd.read_excel(raw_xlsx_path, sheet_name=1)
    print(df.columns.tolist())
    print(df.head(5))
    
    if "period" in df.columns:
        df = df[df["period"].astype(str) != "період"].copy()

    df["period"] = df["period"].astype(int)
    df["data"] = pd.to_numeric(df["data"], errors="coerce")

    df.to_csv(processed_csv_path, index=False)
    csv_df = pd.read_csv(processed_csv_path)
    with sqlite3.connect(db_path) as conn:
        csv_df.to_sql("income_by_region", conn, if_exists="replace", index=False)

    print("Saved:", processed_csv_path, "rows:", len(df))
    print("Saved database:", db_path, "table: income_by_region")
    print(df.head())

if __name__ == "__main__":
    main()
