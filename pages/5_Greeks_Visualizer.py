import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from models import greeks

# ===============================
# 🎛️ Configuration de la page
# ===============================
st.set_page_config(page_title="Greeks Visualizer", layout="wide")
st.title("Greeks Visualizer (European Options)")

# ===============================
# 📊 Paramètres utilisateur
# ===============================
st.sidebar.header("⚙️ Option Parameters")

S = st.sidebar.slider("Spot Price (S)", 50, 150, 100)
K = st.sidebar.slider("Strike Price (K)", 50, 150, 100)
T = st.sidebar.slider("Maturity T (in years)", 0.01, 2.0, 1.0, step=0.01)
r = st.sidebar.slider("Risk-Free Rate (r)", 0.0, 0.2, 0.05, step=0.005)
sigma = st.sidebar.slider("Volatility (σ)", 0.05, 1.0, 0.2, step=0.01)
option_type = st.sidebar.selectbox("Option Type", ["call", "put"])

# ===============================
# 📍 Calcul des greeks (formules fermées)
# ===============================
delta_val = greeks.delta(S, K, T, r, sigma, option_type)
gamma_val = greeks.gamma(S, K, T, r, sigma)
vega_val  = greeks.vega(S, K, T, r, sigma)
theta_val = greeks.theta(S, K, T, r, sigma, option_type)
rho_val   = greeks.rho(S, K, T, r, sigma, option_type)

# ===============================
# 📊 Affichage des valeurs instantanées
# ===============================
st.write(f"**Delta**: {delta_val:.4f}")
st.write(f"**Gamma**: {gamma_val:.4f}")
st.write(f"**Vega**: {vega_val:.4f}")
st.write(f"**Theta**: {theta_val:.4f}")
st.write(f"**Rho**: {rho_val:.4f}")

st.markdown("---")

# ===============================
# 📈 Graphe des sensibilités
# ===============================
with st.expander("Greeks vs Spot Price") :

    S_range = np.linspace(0.5 * K, 1.5 * K, 200)
    delta_vals = [greeks.delta(s, K, T, r, sigma, option_type) for s in S_range]
    gamma_vals = [greeks.gamma(s, K, T, r, sigma) for s in S_range]
    vega_vals  = [greeks.vega(s, K, T, r, sigma) for s in S_range]
    theta_vals = [greeks.theta(s, K, T, r, sigma, option_type) for s in S_range]
    rho_vals   = [greeks.rho(s, K, T, r, sigma, option_type) for s in S_range]

    fig, axs = plt.subplots(3, 2, figsize=(12, 10))
    axs = axs.flatten()
    all_vals = [delta_vals, gamma_vals, vega_vals, theta_vals, rho_vals]
    titles = ["Delta", "Gamma", "Vega", "Theta", "Rho"]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    descriptions = [
        "Delta mesure la variation du prix de l’option par rapport au prix du sous-jacent. Il varie entre 0 et 1 pour un call, -1 et 0 pour un put.",
        "Gamma mesure la convexité de l’option. Il est élevé lorsque l’option est at-the-money, faible en deep ITM ou OTM.",
        "Vega mesure la sensibilité à la volatilité. Il est plus important lorsque l’option est proche du strike et avec une longue maturité.",
        "Theta mesure l’érosion temporelle. Il est généralement négatif, plus marqué pour les ATM et les échéances courtes.",
        "Rho mesure la sensibilité aux taux d’intérêt. Il est positif pour les calls et négatif pour les puts."
    ]

    for ax, values, title, color in zip(axs, all_vals, titles, colors):
        ax.plot(S_range, values, color=color)
        ax.axvline(x=S, linestyle='--', color='gray', alpha=0.6)
        ax.set_title(f"{title} vs Spot Price", fontsize=14)
        ax.set_xlabel("Spot Price (S)", fontsize=12)
        ax.set_ylabel(title, fontsize=12)
        ax.grid(True)

    fig.delaxes(axs[-1])
    fig.tight_layout(pad=6.0)
    st.pyplot(fig)

# ===============================
# 📉 Greeks vs Volatility (σ)
# ===============================
with st.expander("Greeks vs Volatility (σ)"):
    st.markdown("This section visualizes how the Greeks behave as volatility increases, with all other parameters fixed.")

    vol_range = np.linspace(0.05, 1.0, 200)
    delta_vals_sigma = [greeks.delta(S, K, T, r, sigma_val, option_type) for sigma_val in vol_range]
    gamma_vals_sigma = [greeks.gamma(S, K, T, r, sigma_val) for sigma_val in vol_range]
    vega_vals_sigma  = [greeks.vega(S, K, T, r, sigma_val) for sigma_val in vol_range]
    theta_vals_sigma = [greeks.theta(S, K, T, r, sigma_val, option_type) for sigma_val in vol_range]
    rho_vals_sigma   = [greeks.rho(S, K, T, r, sigma_val, option_type) for sigma_val in vol_range]

    fig_sigma, axs_sigma = plt.subplots(3, 2, figsize=(12, 10))
    axs_sigma = axs_sigma.flatten()
    all_vals_sigma = [delta_vals_sigma, gamma_vals_sigma, vega_vals_sigma, theta_vals_sigma, rho_vals_sigma]
    titles_sigma = ["Delta", "Gamma", "Vega", "Theta", "Rho"]

    for ax, values, title in zip(axs_sigma, all_vals_sigma, titles_sigma):
        ax.plot(vol_range, values)
        ax.set_title(f"{title} vs Volatility")
        ax.set_xlabel("Volatility (σ)")
        ax.set_ylabel(title)

    fig_sigma.delaxes(axs_sigma[-1])
    fig_sigma.tight_layout(pad=4.0)
    st.pyplot(fig_sigma)

    st.info("""
**Quick Interpretation**:

- **Delta**: Slightly affected for ATM, more stable otherwise.
- **Gamma**: Typically decreases with higher σ (flatter curve).
- **Vega**: Increases strongly with σ up to a point, then stabilizes.
- **Theta**: Becomes more negative for ATM options as σ increases.
- **Rho**: Relatively stable but can vary slightly with high σ.
    """)

# ===============================
# ⏳ Greeks vs Maturity (T)
# ===============================
with st.expander("Greeks vs Maturity (T)"):
    st.markdown("This section visualizes how Greeks evolve with time to maturity, keeping other parameters fixed.")

    T_range = np.linspace(0.01, 2.0, 200)
    delta_vals_T = [greeks.delta(S, K, T_val, r, sigma, option_type) for T_val in T_range]
    gamma_vals_T = [greeks.gamma(S, K, T_val, r, sigma) for T_val in T_range]
    vega_vals_T  = [greeks.vega(S, K, T_val, r, sigma) for T_val in T_range]
    theta_vals_T = [greeks.theta(S, K, T_val, r, sigma, option_type) for T_val in T_range]
    rho_vals_T   = [greeks.rho(S, K, T_val, r, sigma, option_type) for T_val in T_range]

    fig_T, axs_T = plt.subplots(3, 2, figsize=(12, 10))
    axs_T = axs_T.flatten()
    all_vals_T = [delta_vals_T, gamma_vals_T, vega_vals_T, theta_vals_T, rho_vals_T]
    titles_T = ["Delta", "Gamma", "Vega", "Theta", "Rho"]

    for ax, values, title in zip(axs_T, all_vals_T, titles_T):
        ax.plot(T_range, values)
        ax.set_title(f"{title} vs Maturity")
        ax.set_xlabel("Maturity (T in years)")
        ax.set_ylabel(title)

    fig_T.delaxes(axs_T[-1])
    fig_T.tight_layout(pad=4.0)
    st.pyplot(fig_T)

    st.info("""
**Quick Interpretation**:

- **Delta**: Tends to converge toward 0 or 1 as maturity increases.
- **Gamma**: Decreases with time (most sensitive near expiry).
- **Vega**: Peaks at intermediate maturities, flattens with long maturity.
- **Theta**: Becomes more negative near expiration, especially for ATM options.
- **Rho**: Increases with time, as interest rate impact grows over time.
    """)


# ===============================
# 📘 Detailed Interpretation of Greeks
# ===============================
with st.expander("ℹ️ Detailed Interpretation of Greeks"):
    st.markdown("### Delta")
    st.write("""
- **Definition**: Measures the sensitivity of the option’s price to a small change in the underlying asset's price.
- **Call Options**: Delta ∈ [0, 1] — Deep ITM ≈ 1, ATM ≈ 0.5, Deep OTM ≈ 0
- **Put Options**: Delta ∈ [-1, 0] — Deep ITM ≈ -1, ATM ≈ -0.5, Deep OTM ≈ 0
- **Intuition**: Represents the equivalent position in the underlying. A delta of 0.5 means holding the option is like holding 0.5 units of the stock.
- **Use case**: Useful for hedging (Δ-hedging) and estimating the probability the option will expire in-the-money (under risk-neutral measure).
    """)

    st.markdown("### Gamma")
    st.write("""
- **Definition**: Measures the rate of change of Delta with respect to the underlying’s price (second derivative).
- **Behavior**: Highest when the option is ATM and close to maturity.
- **Significance**: Indicates the curvature of the option's price — a high gamma implies that delta can change rapidly, requiring frequent re-hedging.
- **Use case**: Gamma helps assess the stability of a hedge — high gamma means more dynamic risk.
    """)

    st.markdown("### Vega")
    st.write("""
- **Definition**: Sensitivity of the option’s price to changes in volatility.
- **Behavior**: Increases with time to maturity and peaks for ATM options.
- **Call and Put**: Both are positively sensitive to volatility → Vega > 0
- **Significance**: Important for options on volatile assets, or for volatility trading strategies (vega-neutral portfolios).
- **Use case**: Traders use Vega to manage exposure to implied volatility changes.
    """)

    st.markdown("### Theta")
    st.write("""
- **Definition**: Measures the rate of decline in the option’s price with the passage of time (time decay).
- **Call & Put**: Generally negative (options lose value over time).
- **Behavior**: Steeper for ATM options and as maturity nears.
- **Use case**: Short option positions benefit from time decay (positive theta), while long positions suffer (negative theta).
- **Warning**: Theta increases sharply as expiry approaches, especially for ATM options.
    """)

    st.markdown("### Rho")
    st.write("""
- **Definition**: Sensitivity of the option’s price to changes in the risk-free interest rate.
- **Call Options**: Rho > 0 → Increase in rates increases the value of call options.
- **Put Options**: Rho < 0 → Increase in rates decreases the value of put options.
- **Behavior**: More relevant for long-dated options (almost negligible for short-term).
- **Use case**: Important in environments with changing monetary policies or for fixed income / structured products desks.
    """)
