import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from simulations.monte_carlo import monte_carlo_asian_arithmetic, monte_carlo_asian_geometric
from simulations.gbm import simulate_gbm_paths
from utils.plot import plot_gbm_paths
from sidebar import render_sidebar

# --------------------------
# 🌏 Page Config
# --------------------------
st.set_page_config(page_title="Asian Options", layout="wide")
st.title("Asian Options")

# --------------------------
# 📅 Sidebar Parameters
# --------------------------
st.sidebar.header("Asian Option Parameters")
S = st.sidebar.number_input("Initial Price (S)", value=100.0)
K = st.sidebar.number_input("Strike Price (K)", value=100.0)
T = st.sidebar.number_input("Maturity (T in years)", value=1.0)
r = st.sidebar.number_input("Risk-Free Rate (r)", value=0.05)
sigma = st.sidebar.number_input("Volatility (σ)", value=0.2)
option_type = st.sidebar.selectbox("Option Type", ["call", "put"])
avg_type = st.sidebar.selectbox("Averaging Type", ["arithmetic", "geometric"])
n_simulations = st.sidebar.slider("Monte Carlo Simulations", 1000, 50000, 10000, step=1000)
n_steps = st.sidebar.slider("Time Steps (n_steps)", 10, 365, 252)

# --------------------------
# 📈 Simulate GBM Paths
# --------------------------
paths = simulate_gbm_paths(S, T, r, sigma, n_simulations=n_simulations, n_steps=n_steps)

# --------------------------
# 💸 Pricing via Monte Carlo
# --------------------------
if avg_type == "arithmetic":
    avg_prices = np.mean(paths[:, 1:], axis=1)  # exclude S0
    price = monte_carlo_asian_arithmetic(S, K, T, r, sigma, option_type, n_simulations, n_steps)
else:
    avg_prices = np.exp(np.mean(np.log(paths[:, 1:]), axis=1))
    price = monte_carlo_asian_geometric(S, K, T, r, sigma, option_type, n_simulations, n_steps)

# --------------------------
# 💰 Payoff Calculation
# --------------------------
if option_type == "call":
    payoffs = np.maximum(avg_prices - K, 0)
else:
    payoffs = np.maximum(K - avg_prices, 0)

# --------------------------
# 📊 Display Results
# --------------------------
st.subheader(f"MC Price (Asian {avg_type})")
st.markdown(f"- **Simulated Price**: `{price:.4f}`")
st.markdown(f"- **Average Payoff (undiscounted)**: `{np.mean(payoffs):.4f}`")

# --------------------------
# 📉 Show Simulated GBM Paths
# --------------------------
if st.checkbox("Show Simulated GBM Paths"):
    st.pyplot(plot_gbm_paths(paths, title="Simulated GBM Paths"))

# --------------------------
# 📈 Histogram of Averages
# --------------------------
if st.checkbox("Show Histogram of Average Prices"):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(avg_prices, bins=50, alpha=0.7, edgecolor="black", color="orange")
    ax.axvline(K, color='red', linestyle='--', label='Strike K')
    ax.set_title(f"Distribution of Average Prices ({avg_type})")
    ax.set_xlabel("Average Price")
    ax.set_ylabel("Frequency")
    ax.legend()
    st.pyplot(fig)

# --------------------------
# 📄 Export CSV
# --------------------------
df = pd.DataFrame({"Average Price": avg_prices, "Payoff": payoffs})
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download Results (CSV)", csv, f"asian_{avg_type}_simulations.csv", "text/csv")

# --------------------------
# ℹ️ Explanation Panel
# --------------------------
with st.expander("ℹUnderstanding the Methods"):
    st.markdown("""
    - **Arithmetic Averaging**: Uses the average of the asset prices over the path. Common in real markets, but no closed-form pricing formula exists, hence Monte Carlo simulation is required.
    - **Geometric Averaging**: Uses the geometric mean of asset prices. A closed-form solution exists in some cases, making it analytically more tractable and often used for benchmarking.

    **Comparison**:
    - Arithmetic > Geometric (generally), due to Jensen’s inequality
    - Geometric mean is always lower or equal to the arithmetic mean

    **Use Cases**:
    - Useful for reducing manipulation risk compared to vanilla options
    - Often applied in commodities or Asian equity derivatives
    """)

render_sidebar()