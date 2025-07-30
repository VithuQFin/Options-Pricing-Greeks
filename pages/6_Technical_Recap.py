import streamlit as st

st.title("Theoretical & Technical Recap")

st.markdown("## 1. Fundamental Definitions")

with st.expander("Click to read the section", expanded=False):
    st.markdown("""
    - **Option**: A financial contract granting the right, but not the obligation, to buy (Call) or sell (Put) an underlying asset at a specified strike price \\( K \\), on or before a specified maturity \\( T \\).
    - **Underlying Asset**: The asset on which the option is based (e.g., stock, index, commodity).
    - **Strike Price** \\( K \\): The agreed-upon price.
    - **Maturity** \\( T \\): Time until expiration (in years).
    - **Call Option**: Right to buy at \\( K \\)
    - **Put Option**: Right to sell at \\( K \\)
    """)
    
    st.markdown("### 💡 Moneyness (Position par rapport au strike)")
    st.latex(r"\text{Call (ITM): } S_T > K")
    st.latex(r"\text{Put (ITM): } S_T < K")
    st.latex(r"\text{Call (OTM): } S_T \leq K")
    st.latex(r"\text{Put (OTM): } S_T \geq K")
    st.latex(r"\text{ATM: } S_T \approx K")

    st.markdown("### 🔢 Payoffs")
    st.latex(r"\text{European Call} = \max(S_T - K, 0)")
    st.latex(r"\text{European Put} = \max(K - S_T, 0)")
    st.latex(r"\text{Digital Option} = \mathbb{1}_{S_T > K} \cdot \text{payout}")
    st.latex(r"\text{Asian Option} = \max(\bar{S} - K, 0)")

    st.markdown("### 🧠 Notation Rappel")
    st.latex(r"S_T: \text{ Terminal price of the asset}")
    st.latex(r"\bar{S}: \text{ Average price over time}")
    st.latex(r"\mathbb{1}_{\text{condition}}: \text{ Indicator function}")




# 2. Pricing Models
st.markdown("## 2. Pricing Models")

with st.expander("Click to read the section", expanded=False):

    # 🔷 Black-Scholes
    st.markdown("### 📘 Black-Scholes Model (Closed-Form)")

    st.markdown("**Assumptions**:")
    st.markdown(r"""
    - The underlying asset price \( S_t \) follows a **Geometric Brownian Motion (GBM)**:
    """)
    st.latex(r"dS_t = r S_t \, dt + \sigma S_t \, dW_t")
    st.markdown(r"""
    where:
    - \( r \) is the constant risk-free interest rate  
    - \( \sigma \) is the constant volatility  
    - \( W_t \) is a standard Brownian motion under the risk-neutral measure  
    """)

    st.markdown("**Solution (European Call Option)**:")
    st.latex(r"C = S_0 \mathcal{N}(d_1) - K e^{-rT} \mathcal{N}(d_2)")
    st.latex(r"d_1 = \frac{\log(S_0/K) + (r + \frac{1}{2} \sigma^2) T}{\sigma \sqrt{T}}, \quad d_2 = d_1 - \sigma \sqrt{T}")

    st.markdown("**Remarks**:")
    st.markdown("""
    - Only valid for European options (no early exercise).
    - No dividends, constant interest rate and volatility.
    - Provides a **benchmark** for pricing accuracy.
    """)

    # 🔷 Monte Carlo
    st.markdown("### 🎲 Monte Carlo Simulation")

    st.markdown("**Principle**:")
    st.markdown(r"""
    Used when a closed-form solution does not exist or is difficult to derive:
    1. Simulate \( N \) paths of the underlying asset \( S_t \) using GBM discretization.
    2. Compute the payoff on each path \( \text{payoff}_i \).
    3. Estimate the price as:
    """)
    st.latex(r"V_0 \approx e^{-rT} \cdot \frac{1}{N} \sum_{i=1}^N \text{payoff}_i")

    st.markdown("**GBM Discretization (Euler-Maruyama)**:")
    st.latex(r"S_T^{(i)} = S_0 \cdot \exp\left((r - \frac{1}{2} \sigma^2) T + \sigma \sqrt{T} Z_i\right), \quad Z_i \sim \mathcal{N}(0,1)")

    st.markdown("**Applications**:")
    st.markdown("""
    - European options (vanilla or exotic),
    - Asian options (path-dependent),
    - Digital options (binary payouts),
    - Barrier options (with modifications).
    """)

    st.markdown("**Pros & Cons**:")
    st.markdown("""
    - ✅ Very flexible, especially for path-dependent payoffs.
    - ❌ Computationally intensive, especially for high accuracy.
    - ❌ Not optimal for early-exercise options (e.g. American).
    """)

    # 🔷 CRR
    st.markdown("### 🌲 CRR Binomial Tree (Cox-Ross-Rubinstein)")

    st.markdown("**Construction of the Tree**:")
    st.markdown(r"""
    Discretize time into \( N \) steps of size \( \Delta t = T / N \), with:
    """)
    st.latex(r"u = e^{\sigma \sqrt{\Delta t}}, \quad d = \frac{1}{u}")
    st.latex(r"p = \frac{e^{r \Delta t} - d}{u - d}, \quad 1 - p = \text{prob. down}")

    st.markdown("At each node, asset price evolves as:")
    st.latex(r"S_{i,j} = S_0 \cdot u^j \cdot d^{i-j} \quad \text{(after } i \text{ steps, } j \text{ up moves)}")

    st.markdown("**Pricing Algorithm**:")
    st.markdown("""
    - Compute the payoff at each terminal node.
    - Perform **backward induction** to obtain the option price at each node:
      - For European options: use expected value.
      - For American options: check early exercise condition at each node.
    """)

    st.markdown("**Pros & Cons**:")
    st.markdown("""
    - ✅ Handles early exercise → American options.
    - ✅ Easy to implement and interpret.
    - ❌ Computational cost increases with \( N \).
    - ❌ Less accurate than BS for very high \( N \) unless refined (e.g., Jarrow-Rudd or Trigeorgis).
    """)


# 3. Numerical Methods
st.markdown("## 3. Numerical Techniques")

with st.expander("Click to read the section", expanded=False):

    # 🔹 European Monte Carlo
    st.markdown("### ✅ European Options via Monte Carlo")
    st.markdown(r"""
    - Objective: Estimate the discounted expected value under the risk-neutral measure:
    """)
    st.latex(r"V_0 = \mathbb{E} \left[ e^{-rT} \cdot \text{payoff}(S_T) \right]")
    st.markdown(r"""
    - Implementation:
        - Simulate \( N \) terminal prices \( S_T^{(i)} \sim \mathcal{N}(\cdot, \cdot) \)
        - Compute the payoff for each path
        - Average and discount the result
    """)

    # 🔹 Asian Options
    st.markdown("### 📉 Asian Options via Monte Carlo")
    st.markdown(r"""
    - Payoff depends on the **average price** over time (arithmetic or geometric):
    """)
    st.latex(r"\bar{S} = \frac{1}{M} \sum_{j=1}^{M} S_{t_j}")
    st.markdown(r"""
    - Design choices:
        - Use fine time discretization of the GBM path
        - Store full path history to compute running average
        - Then apply \( \max(\bar{S} - K, 0) \) or \( \max(K - \bar{S}, 0) \)
    """)

    # 🔹 Digital Options
    st.markdown("### 💡 Digital Options via Monte Carlo")
    st.markdown(r"""
    - Binary outcome based on condition:
    """)
    st.latex(r"\text{Payoff} = \mathbb{1}_{\{S_T > K\}} \times \text{payout} \quad \text{(call)}")
    st.markdown(r"""
    - Design:
        - Monte Carlo estimation of the **probability** of being in-the-money
        - Effectively estimates the discounted expected payout:
    """)
    st.latex(r"V_0 = e^{-rT} \cdot \mathbb{P}(S_T > K) \cdot \text{payout}")

    # 🔹 GBM Paths
    st.markdown("### 🌀 Geometric Brownian Motion Paths")
    st.markdown(r"""
    - Core simulation engine for Monte Carlo pricing:
    """)
    st.latex(r"S_{t+\Delta t} = S_t \cdot \exp\left( (r - \frac{1}{2} \sigma^2) \Delta t + \sigma \sqrt{\Delta t} \cdot Z \right)")
    st.markdown("""
    - Enables pricing for path-dependent options (e.g., Asian), and visualizing uncertainty.
    - Vectorized for performance (NumPy broadcasting).
    """)

    # 🔹 CRR Tree
    st.markdown("### 🌲 CRR (Binomial Tree)")
    st.markdown("""
    - Discrete approximation of price paths using up/down branching.
    - Backward induction allows early exercise (for American options).
    - Efficient for low number of steps, but becomes heavy as \( N \to \infty \).
    """)

    # 🔹 Monte Carlo Convergence
    st.markdown("### 📈 Monte Carlo Convergence Control")
    st.markdown("""
    - Accuracy improves with more simulations: \( \text{Error} \sim \mathcal{O}(1/\sqrt{N}) \)
    - We track:
        - **Absolute error** vs Black-Scholes
        - **Execution time** vs number of paths
        - **Variance** reduction optional (to be implemented)
    """)


# 4. Option Types
st.markdown("## 4. Option Types")

with st.expander("Click to read the section", expanded=False):
    st.markdown("""
    | Option Type        | Available Methods                    |
    |--------------------|--------------------------------------|
    | European (call/put)| Black-Scholes, Monte Carlo, CRR     |
    | American (call/put)| CRR                                  |
    | Digital            | Monte Carlo                          |
    | Asian              | Monte Carlo (arith., geom.)          |
    """, unsafe_allow_html=True)

# 5. Technical Architecture
st.markdown("## 5. Technical Architecture")

with st.expander("Click to read the section", expanded=False):
    st.markdown("""
    - `models/` : Analytical models (Black-Scholes, CRR)
    - `simulations/` : Numerical methods (Monte Carlo)
    - `options/` : Streamlit interface by option type
    - `utils/` : Utility functions (payoffs, plots)
    - `pages/` : Streamlit UI components
    """)

# 6. Modeling Assumptions
st.markdown("## 6. Modeling Assumptions")

with st.expander("Click to read the section", expanded=False):
    st.markdown("### 📘 Black-Scholes Assumptions")
    st.markdown(r"""
    The Black-Scholes model is built under the following assumptions:
    - The price of the underlying asset follows a **geometric Brownian motion** under the **risk-neutral measure**:
    """)
    st.latex(r"dS_t = r S_t dt + \sigma S_t dW_t")
    st.markdown(r"""
    - \( r \): constant, known risk-free interest rate  
    - \( \sigma \): constant, known volatility  
    - \( W_t \): standard Brownian motion  
    - Markets are **frictionless** (no transaction costs or bid-ask spreads)  
    - **No dividends** are paid during the life of the option  
    - **Short selling is allowed**  
    - Trading is **continuous** and possible at all times  
    - The asset is **perfectly divisible**, and arbitrage opportunities do not exist  
    - The option is **European style** (exercisable only at maturity)
    """)

    st.markdown("### 🎲 Monte Carlo Assumptions")
    st.markdown(r"""
    Monte Carlo simulations rely on:
    - The **same GBM assumption** for \( S_t \) as in Black-Scholes:
    """)
    st.latex(r"dS_t = r S_t dt + \sigma S_t dW_t")
    st.markdown(r"""
    - Risk-neutral valuation (expected discounted payoff)  
    - Discrete time approximation (Euler or exact simulation of GBM)  
    - A large number of simulations to reduce the **Monte Carlo error**  
    - Independent standard normal draws \( Z_i \sim \mathcal{N}(0, 1) \)
    """)

    st.markdown("### 🌲 CRR Binomial Tree Assumptions")
    st.markdown(r"""
    The CRR model assumes:
    - Price evolves in discrete time via up/down movements:
    """)
    st.latex(r"u = e^{\sigma \sqrt{\Delta t}}, \quad d = 1/u")
    st.latex(r"p = \frac{e^{r \Delta t} - d}{u - d}")
    st.markdown(r"""
    - Perfectly arbitrage-free and complete market  
    - No dividends during the option’s lifetime  
    - Recombining tree (no memory, Markov property)  
    - Option valuation by **backward induction**, using **risk-neutral probability**  
    - For American options: the holder can choose to exercise at each node
    """)
