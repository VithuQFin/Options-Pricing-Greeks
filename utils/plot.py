# utils/plot.py

import matplotlib.pyplot as plt
import numpy as np

# ✅ Plot GBM simulated paths
def plot_gbm_paths(paths, title="Simulated GBM Paths", max_paths=20):
    fig, ax = plt.subplots(figsize=(10, 4))
    for i in range(min(len(paths), max_paths)):
        ax.plot(paths[i], lw=0.7, alpha=0.7)
    ax.set_title(title)
    ax.set_xlabel("Steps")
    ax.set_ylabel("Simulated Price")
    ax.grid(True)
    return fig

# ✅ Histogram of terminal asset prices S_T
def plot_terminal_distribution(ST, title="Terminal Price Distribution ($S_T$)"):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(ST, bins=50, alpha=0.7, color="skyblue", edgecolor="black")
    ax.set_title(title)
    ax.set_xlabel("$S_T$")
    ax.set_ylabel("Frequency")
    return fig

# ✅ Monte Carlo convergence plot
def plot_mc_convergence(x, y, reference=None, title="Monte Carlo Convergence"):
    fig, ax = plt.subplots()
    ax.plot(x, y, marker='o', label="Monte Carlo Estimate")
    if reference is not None:
        ax.axhline(reference, color="red", linestyle="--", label="Reference Value")
    ax.set_xscale("log")
    ax.set_title(title)
    ax.set_xlabel("Number of Simulations")
    ax.set_ylabel("Estimated Price")
    ax.legend()
    return fig
