"""Charts: CLT simulations on synthetic + real data, and the SQL result."""
import sqlite3

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

import clt_simulation as clt
from config import DB_PATH, REPORTS_DIR


def plot_clt(results: dict, mu: float, sigma: float, title: str, filename: str) -> None:
    """One histogram of sample means per sample size, with the CLT normal curve on top."""
    fig, axes = plt.subplots(1, len(results), figsize=(4 * len(results), 3.5))
    for ax, (n, means) in zip(axes, results.items()):
        ax.hist(means, bins=40, density=True, alpha=0.7, color="steelblue")
        pred = clt.clt_prediction(mu, sigma, n)
        x = np.linspace(means.min(), means.max(), 300)
        ax.plot(x, pred.pdf(x), "r-", lw=2, label="CLT normal")
        ax.set_title(f"n = {n}")
        ax.set_yticks([])
    axes[0].legend()
    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(REPORTS_DIR / filename, dpi=120)
    plt.close(fig)


def plot_source_distributions() -> None:
    fig, axes = plt.subplots(1, len(clt.SYNTHETIC_DISTRIBUTIONS), figsize=(11, 3))
    for ax, (name, dist) in zip(axes, clt.SYNTHETIC_DISTRIBUTIONS.items()):
        x = np.linspace(dist.ppf(0.001), dist.ppf(0.99), 300)
        ax.plot(x, dist.pdf(x), lw=2)
        ax.set_title(name)
    fig.suptitle("Starting distributions (none are normal)")
    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "source_distributions.png", dpi=120)
    plt.close(fig)


def plot_normality(all_scores: dict) -> None:
    """KS distance vs n: shrinking = converging to normal."""
    fig, ax = plt.subplots(figsize=(6, 4))
    for name, scores in all_scores.items():
        ax.plot(list(scores.keys()), list(scores.values()), marker="o", label=name)
    ax.set_xscale("log")
    ax.set_xlabel("sample size n")
    ax.set_ylabel("distance from normal (KS)")
    ax.set_title("Convergence to normality")
    ax.legend()
    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "clt_convergence.png", dpi=120)
    plt.close(fig)


def plot_churn_by_contract() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql("SELECT * FROM churn_by_contract", conn)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(df["Contract"], df["churn_rate"] * 100, color="indianred")
    ax.set_ylabel("churn rate (%)")
    ax.set_title("Churn rate by contract type (SQL transform output)")
    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "churn_by_contract.png", dpi=120)
    plt.close(fig)
