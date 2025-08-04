import streamlit as st
import numpy as np
import pandas as pd
from simulations.monte_carlo import monte_carlo_digital
from simulations.gbm import simulate_gbm_paths
from utils.payoffs import digital_payoff
from utils.plot import plot_terminal_distribution
import matplotlib.pyplot as plt
from sidebar import render_sidebar

st.title("Digital Options")

# 📥 User Parameters
st.sidebar.header("Digital Option Parameters")
S = st.sidebar.number_input("Initial Price (S)", value=100.0)
K = st.sidebar.number_input("Strike Price (K)", value=100.0)
T = st.sidebar.number_input("Maturity (T in years)", value=1.0)
r = st.sidebar.number_input("Risk-Free Rate (r)", value=0.05)
sigma = st.sidebar.number_input("Volatility (σ)", value=0.2)
option_type = st.sidebar.selectbox("Option Type", ["call", "put"])
payout = st.sidebar.number_input("Payout (if ITM)", value=1.0)
n_simulations = st.sidebar.slider("Number of Simulations", 1000, 50000, 10000, step=1000)

# 🎯 Price Computation
price = monte_carlo_digital(S, K, T, r, sigma, option_type, payout, n_simulations)
st.subheader(f"Monte Carlo Price (cash-or-nothing digital): **{price:.4f}**")

# 🧮 Data Generation for Analysis
Z = np.random.randn(n_simulations)
ST = S * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)
payoffs = digital_payoff(ST, K, option_type, payout)

# 📊 Histogram of Terminal Prices
if st.checkbox("Show $S_T$ Distribution"):
    st.pyplot(plot_terminal_distribution(ST, title="Distribution of $S_T$ for Digital Option"))

# 📊 Histogram of Payoffs
if st.checkbox("Show Payoff Distribution"):
    fig, ax = plt.subplots()
    ax.hist(payoffs, bins=np.unique(payoffs).size, edgecolor="black", color="mediumseagreen")
    ax.set_xticks([0, payout])
    ax.set_title("Payoff Distribution (0 / payout)")
    ax.set_xlabel("Payoff")
    ax.set_ylabel("Number of Simulations")
    st.pyplot(fig)

# 📤 Export CSV
df = pd.DataFrame({
    "S_T": ST,
    "Payoff": payoffs
})
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download Results (CSV)", csv, "digital_option_simulation.csv", "text/csv")

render_sidebar()