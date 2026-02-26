import pandas as pd

DATA_PATH = "data/processed/income_by_region_clean.csv"


def main():
    df = pd.read_csv(DATA_PATH)

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

if __name__ == "__main__":
    main()