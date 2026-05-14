import json
from pathlib import Path

import pandas as pd

DATA_PATH = "data/processed/income_by_region_clean.csv"
REPORT_PATH = Path("reports/data_quality_report.json")


def main():
    df = pd.read_csv(DATA_PATH)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    print("Dataset shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicates:")
    print(df.duplicated().sum())

    print("\nData types:")
    print(df.dtypes)

    print("\nYears range:")
    print(df["period"].min(), "-", df["period"].max())

    print("\nUnique regions:")
    print(df["attributes"].nunique())

    missing = df[df["data"].isna()][["code", "attributes", "period", "data"]]
    print("\nRows with missing data:")
    print(missing.head(20))
    print("Total missing:", len(missing))

    report = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": df.columns.tolist(),
        "missing_values": {column: int(value) for column, value in df.isnull().sum().items()},
        "duplicates": int(df.duplicated().sum()),
        "data_types": {column: str(dtype) for column, dtype in df.dtypes.items()},
        "years_range": {
            "min": int(df["period"].min()),
            "max": int(df["period"].max()),
        },
        "unique_regions": int(df["attributes"].nunique()),
        "rows_with_missing_data": int(len(missing)),
    }

    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\nSaved quality report:", REPORT_PATH)

if __name__ == "__main__":
    main()
