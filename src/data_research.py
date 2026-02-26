import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

DATA_PATH = "data/processed/income_by_region_clean.csv"

def main():
    df = pd.read_csv(DATA_PATH)

    df = df.dropna(subset=["data"]).copy()


    ua = df[df["attributes"] == "Україна"].sort_values("period")
    print("Ukraine years:", ua["period"].min(), "-", ua["period"].max())


    last_year = df["period"].max()
    regions = df[df["attributes"] != "Україна"]

    top = (
        regions[regions["period"] == last_year]
        .sort_values("data", ascending=False)
        .head(10)
    )
    print("\nTop-10 regions by income for", last_year)
    print(top.to_string(index=False))

  
    X = ua[["period"]]
    y = ua["data"]
    model = LinearRegression()
    model.fit(X, y)

    pred = model.predict(X)
    print("\nModel: LinearRegression for Ukraine trend")
    print("coef:", model.coef_[0], "intercept:", model.intercept_)
    print("R2:", r2_score(y, pred))


    next_year = int(ua["period"].max()) + 1
    next_pred = model.predict(pd.DataFrame({"period": [next_year]}))[0]
    print("Prediction for", next_year, ":", next_pred)

if __name__ == "__main__":
    main()