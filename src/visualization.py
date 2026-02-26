from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "data/processed/income_by_region_clean.csv"
FIG_DIR = Path("reports/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)

def main():
    df = pd.read_csv(DATA_PATH).dropna(subset=["data"])

    # 1) Тренд України
    ua = df[df["attributes"] == "Україна"].sort_values("period")
    plt.figure()
    plt.plot(ua["period"], ua["data"])
    plt.title("Income trend (Ukraine)")
    plt.xlabel("Year")
    plt.ylabel("Income (mln UAH)")
    plt.savefig(FIG_DIR / "ua_trend.png", bbox_inches="tight")

    regions = df[df["attributes"] != "Україна"]
    last_year = regions["period"].max()

    top = (
        regions[regions["period"] == last_year]
        .sort_values("data", ascending=False)
        .head(10)
    )
    plt.figure()
    plt.bar(top["attributes"], top["data"])
    plt.title(f"Top-10 regions by income ({last_year})")
    plt.xticks(rotation=60, ha="right")
    plt.ylabel("Income (mln UAH)")
    plt.savefig(FIG_DIR / "top10_regions.png", bbox_inches="tight")

    print("Saved figures to:", FIG_DIR)

if __name__ == "__main__":
    main()