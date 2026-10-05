"""Central Limit Theorem simulation engine.

CLT: the mean of n independent samples becomes ~ Normal(mu, sigma / sqrt(n))
as n grows, no matter how non-normal the underlying distribution is.

For each distribution we draw many samples of size n, take each sample's mean,
and measure how close those means are to the normal curve the CLT predicts.
"""
import numpy as np
from scipy import stats

SAMPLE_SIZES = [1, 5, 30, 100]
N_TRIALS = 10_000
SEED = 42

# name -> (frozen scipy distribution). scipy gives us the true mean/std for free.
SYNTHETIC_DISTRIBUTIONS = {
    "Uniform(0, 1)": stats.uniform(0, 1),
    "Exponential(1)": stats.expon(scale=1),
    "Lognormal(0, 1)": stats.lognorm(s=1),
}


def sample_means(draw, n: int, trials: int = N_TRIALS) -> np.ndarray:
    """Take `trials` samples of size n using draw(size) and return each sample's mean."""
    return draw((trials, n)).mean(axis=1)


def simulate_distribution(dist, sample_sizes=SAMPLE_SIZES, seed=SEED) -> dict:
    """Return {n: sample means} for a scipy distribution."""
    rng = np.random.default_rng(seed)
    return {
        n: sample_means(lambda size: dist.rvs(size=size, random_state=rng), n)
        for n in sample_sizes
    }


def simulate_data(values: np.ndarray, sample_sizes=SAMPLE_SIZES, seed=SEED) -> dict:
    """Same idea on real data: resample (bootstrap) from observed values."""
    rng = np.random.default_rng(seed)
    return {
        n: sample_means(lambda size: rng.choice(values, size=size), n)
        for n in sample_sizes
    }


def clt_prediction(mu: float, sigma: float, n: int):
    """The normal distribution the CLT says the sample means should follow."""
    return stats.norm(mu, sigma / np.sqrt(n))


def normality_score(means: np.ndarray) -> float:
    """Kolmogorov-Smirnov distance to a fitted normal (0 = perfectly normal)."""
    mu, sigma = means.mean(), means.std(ddof=1)
    return stats.kstest(means, "norm", args=(mu, sigma)).statistic


def summarize(results: dict, mu: float, sigma: float) -> list[dict]:
    """Compare simulated mean/std of the sample means with CLT theory."""
    rows = []
    for n, means in results.items():
        rows.append({
            "n": n,
            "theory_mean": mu,
            "sim_mean": means.mean(),
            "theory_se": sigma / np.sqrt(n),
            "sim_se": means.std(ddof=1),
            "ks_distance": normality_score(means),
        })
    return rows
