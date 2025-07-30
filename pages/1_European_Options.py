import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import lognorm
from models.black_scholes import black_scholes_price
from models.crr import crr_price
from simulations.monte_carlo import monte_carlo_european
from simulations.gbm import simulate_gbm_paths
from utils.payoffs import european_payoff
from utils.plot import plot_gbm_paths, plot_terminal_distribution
import matplotlib.pyplot as plt

# --------------------------
# 🧭 Page Config
# --------------------------
st.set_page_config(page_title="European Options", layout="wide")
st.title("European Options")

# --------------------------
# 📥 Sidebar Parameters
# --------------------------
st.sidebar.header("European Option Parameters")
S = st.sidebar.number_input("Initial Price (S)", value=100.0)
K = st.sidebar.number_input("Strike Price (K)", value=100.0)
T = st.sidebar.number_input("Maturity (T in years)", value=1.0)
r = st.sidebar.number_input("Risk-Free Rate (r)", value=0.05)
sigma = st.sidebar.number_input("Volatility (σ)", value=0.2)
option_type = st.sidebar.selectbox("Option Type", ["call", "put"])
n_sim = st.sidebar.slider("Monte Carlo Simulations", 1000, 50000, 10000, step=1000)

# --------------------------
# 💸 Pricing Models
# --------------------------
bs_price = black_scholes_price(S, K, T, r, sigma, option_type)
mc_price = monte_carlo_european(S, K, T, r, sigma, n_sim, option_type)
crr_price_value = crr_price(S, K, T, r, sigma, N=100, option_type=option_type, american=False)

rel_diff_mc = abs(bs_price - mc_price) / bs_price * 100
rel_diff_crr = abs(bs_price - crr_price_value) / bs_price * 100

# --------------------------
# 📊 Pricing Results
# --------------------------
st.subheader("Pricing Results")
st.markdown(f"- **Black-Scholes (closed-form)**: `{bs_price:.4f}`")
st.markdown(f"- **Monte Carlo (n={n_sim})**: `{mc_price:.4f}`")
st.markdown(f"- **CRR (100 steps)**: `{crr_price_value:.4f}`")
st.markdown(f"Deviation from BS:")
st.markdown(f"  - Monte Carlo: `{rel_diff_mc:.2f}%`")
st.markdown(f"  - CRR: `{rel_diff_crr:.2f}%`")

# --------------------------
# 📘 Model Assumptions
# --------------------------
with st.expander("Model Assumptions"):
    st.markdown(r"""
    - No arbitrage
    - No transaction costs
    - Constant volatility \( \sigma \)
    - Constant interest rate \( r \)
    - Log-normal distribution of \( S_T \)
    - European-style (only exercisable at maturity)
    """)

# --------------------------
# 🧪 Monte Carlo Convergence
# --------------------------
with st.expander("Monte Carlo Convergence"):
    ns = [100, 500, 1000, 5000, 10000, 20000, 50000]
    estimates = [monte_carlo_european(S, K, T, r, sigma, n, option_type) for n in ns]

    fig, ax = plt.subplots()
    ax.plot(ns, estimates, label="MC Price", marker='o')
    ax.axhline(bs_price, color='red', linestyle='--', label="BS Price")
    ax.set_xlabel("Number of Simulations")
    ax.set_ylabel("Option Price")
    ax.set_title("Convergence of Monte Carlo Estimate")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# --------------------------
# 📉 Simulated GBM Paths
# --------------------------
if st.checkbox("Show Simulated GBM Paths"):
    paths = simulate_gbm_paths(S, T, r, sigma, n_simulations=n_sim)
    st.pyplot(plot_gbm_paths(paths, title="Simulated GBM Paths"))

    # Terminal distribution + lognormal overlay
    ST = paths[:, -1]
    fig, ax = plt.subplots()
    ax.hist(ST, bins=50, density=True, alpha=0.6, label="Simulated $S_T$")

    mu = (r - 0.5 * sigma ** 2) * T + np.log(S)
    sigma_log = sigma * np.sqrt(T)
    x = np.linspace(min(ST), max(ST), 1000)
    pdf = lognorm.pdf(x, s=sigma_log, scale=np.exp(mu))
    ax.plot(x, pdf, 'r--', label="Lognormal PDF")

    ax.set_title("Distribution of $S_T$ vs Theoretical PDF")
    ax.set_xlabel("$S_T$")
    ax.set_ylabel("Density")
    ax.legend()
    st.pyplot(fig)

    # Payoff comparison
    payoffs = european_payoff(ST, K, option_type)
    discounted_avg = np.mean(payoffs) * np.exp(-r * T)

    st.markdown(f"**Discounted Average Payoff**: `{discounted_avg:.4f}`")
    st.markdown(f"**Monte Carlo Estimate**: `{mc_price:.4f}`")

    # Downloadable results
    df = pd.DataFrame({"S_T": ST, "Payoff": payoffs})
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Payoff Results (CSV)", csv, "payoffs_european.csv", "text/csv")

# --------------------------
# ℹ️ Explanation Panel
# --------------------------
with st.expander("ℹMethod Comparison"):
    st.markdown("""
    - **Black-Scholes**: Closed-form solution derived under strict assumptions. Serves as benchmark.
    - **Monte Carlo**: Simulation-based pricing useful for exotic or path-dependent payoffs.
    - **CRR Tree**: Binomial tree approximation that becomes more accurate as steps increase. Versatile for American-style options.

    **Comparison Notes**:
    - Monte Carlo estimates converge with more simulations
    - CRR converges to Black-Scholes as number of steps increases
    - Useful to compare deviation from theoretical price
    """)
