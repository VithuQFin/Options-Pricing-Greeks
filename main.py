import numpy as np
from models.black_scholes import black_scholes_price
from models.crr import crr_price
from models import greeks
from simulations.monte_carlo import monte_carlo_european, monte_carlo_digital, monte_carlo_asian_arithmetic, monte_carlo_asian_geometric
from simulations.gbm import simulate_gbm_paths
from utils.payoffs import digital_payoff


def european_options():
    print("\n===== European Options Pricing =====")
    S, K, T, r, sigma, option_type = 100, 100, 1.0, 0.05, 0.2, "call"
    n_sim = 100000

    bs = black_scholes_price(S, K, T, r, sigma, option_type)
    mc = monte_carlo_european(S, K, T, r, sigma, n_sim, option_type)
    crr = crr_price(S, K, T, r, sigma, N=100, option_type=option_type, american=False)

    print(f"Black-Scholes Price: {bs:.4f}")
    print(f"Monte Carlo Price:   {mc:.4f} (n = {n_sim})")
    print(f"CRR Price:           {crr:.4f}")

def european_options_greeks():
    print("\n===== European Options Greeks =====")
    S, K, T, r, sigma, option_type = 100, 100, 1.0, 0.05, 0.2, "call"

    delta_val = greeks.delta(S, K, T, r, sigma, option_type)
    gamma_val = greeks.gamma(S, K, T, r, sigma)
    vega_val = greeks.vega(S, K, T, r, sigma)
    theta_val = greeks.theta(S, K, T, r, sigma, option_type)
    rho_val = greeks.rho(S, K, T, r, sigma, option_type)

    print(f"Delta : {delta_val:.4f}")
    print(f"Gamma : {gamma_val:.4F}")
    print(f"Vega : {vega_val:.4f}")
    print(f"Theta : {theta_val:.4f}")
    print(f"Rho : {rho_val:.4f}")


def american_options():
    print("\n===== American Options Pricing (CRR) =====")
    S, K, T, r, sigma, N, option_type = 100, 100, 1.0, 0.05, 0.2, 100, "put"

    crr_american = crr_price(S, K, T, r, sigma, N=N, option_type=option_type, american=True)
    crr_european = crr_price(S, K, T, r, sigma, N=N, option_type=option_type, american=False)

    print(f"CRR American Option Price: {crr_american:.4f}")
    print(f"CRR European Option Price: {crr_european:.4f}")


def asian_options():
    print("\n===== Asian Options Pricing (Monte Carlo) =====")
    S, K, T, r, sigma, option_type = 100, 100, 1.0, 0.05, 0.2, "call"
    n_sim, n_steps = 100000, 252

    price_arith = monte_carlo_asian_arithmetic(S, K, T, r, sigma, option_type, n_sim, n_steps)
    price_geo = monte_carlo_asian_geometric(S, K, T, r, sigma, option_type, n_sim, n_steps)

    print(f"Monte Carlo Arithmetic Average: {price_arith:.4f}")
    print(f"Monte Carlo Geometric Average:  {price_geo:.4f}")


def digital_options():
    print("\n===== Digital Options Pricing (Cash-or-Nothing) =====")
    S, K, T, r, sigma, option_type, payout = 100, 100, 1.0, 0.05, 0.2, "call", 1.0
    n_sim = 100000

    price = monte_carlo_digital(S, K, T, r, sigma, option_type, payout, n_sim)
    print(f"Monte Carlo Digital Option Price: {price:.4f}")

    Z = np.random.randn(n_sim)
    ST = S * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)
    payoffs = digital_payoff(ST, K, option_type, payout)
    proportion_ITM = np.mean(payoffs > 0)
    print(f"Probability ITM (estimated): {proportion_ITM:.2%}")


if __name__ == "__main__":
    european_options()
    european_options_greeks()
    american_options()
    asian_options()
    digital_options()
