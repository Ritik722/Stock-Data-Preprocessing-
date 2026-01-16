# Stock OHLCV Data Preprocessing (Python)

A small Python project that merges two stock price files and prepares a clean, analysis-ready OHLCV dataset.  
The pipeline focuses on practical data cleaning + logical validation that is useful before time-series analysis or ML workflows.

## What this project does
- Loads two stock price files and concatenates them
- Parses and validates `Date`
- Standardizes `Volume` (e.g., handles `"zero"` and type issues)
- Removes market-closed style rows (`Open = High = Low = Close` and `Volume = 0`)
- Fills missing OHLC values using median imputation
- Handles extreme `Volume` outliers by capping to the median (simple robust baseline)
- Applies logical validation: `Low ≤ Open/Close ≤ High`
- Exports cleaned data to CSV

## Tech stack
- Python
- pandas, numpy

## Expected input columns
The script expects these columns:
- `Date, Open, High, Low, Close, Volume`

## How to run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt

