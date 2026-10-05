"""Run the whole pipeline: Extract -> Load -> Transform -> Simulate -> Visualize.

Usage:  python pipeline.py
"""
import sqlite3

import pandas as pd

import clt_simulation as clt
import extract_load
import transform
import visualize
from config import DB_PATH


def run_simulations() -> None:
    all_scores = {}

    visualize.plot_source_distributions()
    for name, dist in clt.SYNTHETIC_DISTRIBUTIONS.items():
        mu, sigma = dist.mean(), dist.std()
        results = clt.simulate_distribution(dist)
        rows = clt.summarize(results, mu, sigma)
        all_scores[name] = {r["n"]: r["ks_distance"] for r in rows}
        safe = name.split("(")[0].lower()
        visualize.plot_clt(results, mu, sigma, f"CLT: sample means of {name}", f"clt_{safe}.png")
        print(pd.DataFrame(rows).round(4).to_string(index=False), "\n")

    # Real data: monthly charges are not normal either.
    with sqlite3.connect(DB_PATH) as conn:
        charges = pd.read_sql("SELECT MonthlyCharges FROM clean_customers", conn)["MonthlyCharges"].to_numpy()
    mu, sigma = charges.mean(), charges.std()
    results = clt.simulate_data(charges)
    visualize.plot_clt(results, mu, sigma, "CLT on real data: Telco MonthlyCharges", "clt_real_monthly_charges.png")
    all_scores["Telco MonthlyCharges"] = {r["n"]: r["ks_distance"] for r in clt.summarize(results, mu, sigma)}

    visualize.plot_normality(all_scores)


def run() -> None:
    print("--- PIPELINE START ---")
    extract_load.run()
    transform.run()
    run_simulations()
    visualize.plot_churn_by_contract()
    print("--- PIPELINE COMPLETE (charts in reports/) ---")


if __name__ == "__main__":
    run()
