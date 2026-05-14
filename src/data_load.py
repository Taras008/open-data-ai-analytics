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
    if processed_csv_path.exists() and processed_csv_path.stat().st_size > 0:
        print(f"Using existing processed CSV: {processed_csv_path}")
        csv_df = pd.read_csv(processed_csv_path)
    else:
        download(XLSX_URL, raw_xlsx_path)

        csv_df = pd.read_excel(raw_xlsx_path, sheet_name=1)
        print(csv_df.columns.tolist())
        print(csv_df.head(5))

        if "period" in csv_df.columns:
            csv_df = csv_df[csv_df["period"].astype(str) != "період"].copy()

        csv_df["period"] = csv_df["period"].astype(int)
        csv_df["data"] = pd.to_numeric(csv_df["data"], errors="coerce")
        csv_df.to_csv(processed_csv_path, index=False)

    with sqlite3.connect(db_path) as conn:
        csv_df.to_sql("income_by_region", conn, if_exists="replace", index=False)

    print("Saved:", processed_csv_path, "rows:", len(csv_df))
    print("Saved database:", db_path, "table: income_by_region")
    print(csv_df.head())

if __name__ == "__main__":
    main()
