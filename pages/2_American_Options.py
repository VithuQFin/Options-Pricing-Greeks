import streamlit as st
import numpy as np
import pandas as pd
from models.crr import crr_price
from sidebar import render_sidebar

# --------------------------
# 🧭 Page Config
# --------------------------
st.set_page_config(page_title="American Options", layout="wide")
st.title("American Options")

# --------------------------
# 📅 Sidebar Parameters
# --------------------------
st.sidebar.header("American Option Parameters")
S = st.sidebar.number_input("Initial Price (S)", value=100.0)
K = st.sidebar.number_input("Strike Price (K)", value=100.0)
T = st.sidebar.number_input("Maturity (T in years)", value=1.0)
r = st.sidebar.number_input("Risk-Free Rate (r)", value=0.05)
sigma = st.sidebar.number_input("Volatility (σ)", value=0.2)
option_type = st.sidebar.selectbox("Option Type", ["call", "put"])
N = st.sidebar.slider("CRR Tree Steps (N)", min_value=10, max_value=200, value=100)

# --------------------------
# 💸 Pricing via CRR Tree
# --------------------------
american_price = crr_price(S, K, T, r, sigma, N, option_type, american=True)
european_price = crr_price(S, K, T, r, sigma, N, option_type, american=False)
diff = american_price - european_price

# --------------------------
# 📊 Pricing Results
# --------------------------
st.subheader("Pricing Results")
st.markdown(f"- **CRR Price (American Option)**: `{american_price:.4f}`")
st.markdown(f"- **CRR Price (European Option)**: `{european_price:.4f}`")
st.markdown(f"- **Difference (Early Exercise Premium)**: `{diff:.4f}`")

# --------------------------
# 🔔 Special Case Note
# --------------------------
if option_type == "call" and np.isclose(american_price, european_price, atol=1e-3):
    st.info("For an **American call without dividends**, early exercise is usually **not optimal**, hence the price ≈ European call.")

# --------------------------
# 🗒 Tree Export & Visualization
# --------------------------
with st.expander("Export Terminal Node Prices"):
    u = np.exp(sigma * np.sqrt(T / N))
    d = 1 / u
    prices = [S * (u ** (N - i)) * (d ** i) for i in range(N + 1)]
    df = pd.DataFrame({"Node": range(N + 1), "Terminal Price $S_T$": prices})
    st.dataframe(df)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "crr_terminal_prices.csv", "text/csv")

# --------------------------
# ℹ️ Explanation Panel
# --------------------------
with st.expander("ℹAmerican vs European Options"):
    st.markdown("""
    - **American options** allow for **early exercise** at any point up to maturity.
    - **Put options** often benefit from early exercise due to time-value and payout asymmetry.
    - **Call options** without dividends usually do **not** benefit from early exercise.
    - **CRR Tree** method is well-suited for American options due to its ability to capture early exercise features.

    **Key Differences**:
    - American options are more flexible, but also more complex to price.
    - European options are simpler and often have closed-form pricing.
    - The early exercise premium is the value added by the ability to exercise early.
    """)

render_sidebar()