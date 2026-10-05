"""EXTRACT + LOAD: get the raw CSV and land it, untouched, in a SQLite table."""
import sqlite3

import pandas as pd
import requests

from config import DB_PATH, RAW_CSV_PATH, SOURCE_URL


def extract() -> pd.DataFrame:
    if not RAW_CSV_PATH.exists():
        print(f"[EXTRACT] Downloading {SOURCE_URL}")
        response = requests.get(SOURCE_URL, timeout=30)
        response.raise_for_status()
        RAW_CSV_PATH.write_bytes(response.content)
    return pd.read_csv(RAW_CSV_PATH)


def load(df: pd.DataFrame) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql("raw_customers", conn, if_exists="replace", index=False)
    print(f"[LOAD] {len(df)} rows -> raw_customers")


def run() -> None:
    load(extract())


if __name__ == "__main__":
    run()
