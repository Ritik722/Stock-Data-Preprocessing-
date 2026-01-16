import pandas as pd
import numpy as np


def load_data(file1: str, file2: str) -> pd.DataFrame:
    """Load two stock files and concatenate them."""
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2, sep=",")
    return pd.concat([df1, df2], ignore_index=True)


def preprocess_stock_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate OHLCV stock data.
    Assumes columns: Date, Open, High, Low, Close, Volume
    """
    df = df.copy()

    # Standardize Volume
    df["Volume"] = df["Volume"].replace("zero", 0)
    df["Volume"] = pd.to_numeric(df["Volume"], errors="coerce").fillna(0).astype("int64")

    # Parse dates (example format: 05-Jan-24)
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%y", errors="coerce")
    df = df.dropna(subset=["Date"])  # remove malformed/unparseable dates

    # Remove rows where market likely closed:
    # Open = High = Low = Close AND Volume = 0
    closed_mask = (
        (df["Volume"] == 0)
        & (df["Open"] == df["High"])
        & (df["High"] == df["Low"])
        & (df["Low"] == df["Close"])
    )
    df = df.loc[~closed_mask].copy()

    # Fill missing OHLC with median (simple baseline strategy)
    for col in ["Open", "High", "Low", "Close"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(df[col].median())

    # Cap extreme Volume outliers (basic robust handling)
    vol_median = int(df["Volume"].median())
    df["Volume"] = np.where(df["Volume"] >= 150000, vol_median, df["Volume"]).astype("int64")

    # Logical validation: Open and Close should lie between Low and High
    logical_mask = (
        (df["Low"] <= df["Open"]) & (df["Open"] <= df["High"])
        & (df["Low"] <= df["Close"]) & (df["Close"] <= df["High"])
    )
    df = df.loc[logical_mask].copy()

    # Sort + reset index
    df = df.sort_values("Date").reset_index(drop=True)
    return df


def main():
    # Keep paths relative for GitHub
    file1 = "data/Stock_File_1.csv"
    file2 = "data/Stock_File_2.txt"

    df = load_data(file1, file2)
    cleaned = preprocess_stock_data(df)

    # Save output
    out_path = "output/cleaned_stock_data.csv"
    cleaned.to_csv(out_path, index=False)

    # Minimal summary (helps reviewers)
    print(f"Rows after cleaning: {len(cleaned)}")
    print(f"Date range: {cleaned['Date'].min().date()} to {cleaned['Date'].max().date()}")
    print(f"Saved to: {out_path}")


if __name__ == "__main__":
    main()
