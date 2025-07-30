# 📘 Options Pricing

**Options Pricing** is a modular and extensible Python project for pricing and analyzing financial derivatives — including European, American, Asian, and Digital options — using closed-form formulas and numerical methods like Monte Carlo and binomial trees (CRR).

---

## 🚀 Features

- 📈 **Option Pricing Models**:
  - Black-Scholes for European options
  - Cox-Ross-Rubinstein (CRR) for American options
  - Monte Carlo simulation for Asian and Digital options

- 📐 **Greeks Visualizer**:
  - Closed-form computation of Delta, Gamma, Vega, Theta, Rho
  - Graphical visualizations (vs. spot price, volatility, maturity)
  - Interactive parameter tuning via Streamlit

- 🧠 **Modular Design**:
  - Separate modules for models, simulations, payoffs, and plotting
  - Easy to extend to exotic options and custom Greeks

---

## 🗂️ Project Structure

```bash
.
├── models/             # All pricing models & greeks
│   ├── black_scholes.py
│   ├── crr.py
│   ├── greeks.py (European)
│   ├── greeks_american.py
│   ├── greeks_asian.py
│   └── greeks_digital.py
│
├── options/            # Pricing functions by option type
│   ├── european.py
│   ├── american.py
│   ├── asian.py
│   └── digital.py
│
├── simulations/        # GBM and Monte Carlo simulations
│   ├── gbm.py
│   └── monte_carlo.py
│
├── utils/              # Helper functions for payoffs, plotting, etc.
│   ├── payoffs.py
│   └── plot.py
│
├── pages/              # Streamlit UI pages (excluded from Git)
│   ├── 1_European_Options.py
│   ├── 2_American_Options.py
│   └── ...
│
├── main.py             # Main launcher
├── Home.py             # Landing page (excluded from Git)
├── README.md
└── requirements.txt