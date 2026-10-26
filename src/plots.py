import sys
sys.path.append("..")
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import poisson


def plot_poisson_fit(corners, title, max_corners):
    empirical = corners.value_counts(normalize=True).sort_index()
    lam = corners.mean()
    k = range(0, max_corners + 1)
    theoretical = poisson.pmf(k, lam)

    plt.bar(empirical.index, empirical.values, alpha = 0.6, label = 'empirical distribution')
    plt.plot(k, theoretical, marker = "o", color = "red", label = f"Poisson (lambda = {lam:.2f}")
    plt.title(title)
    plt.xlabel("goals")
    plt.ylabel("frequency")
    plt.legend()
    plt.show()