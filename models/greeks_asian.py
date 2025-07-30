import numpy as np
from simulations.monte_carlo import monte_carlo_asian_arithmetic, monte_carlo_asian_geometric

def price_asian_option(S, K, T, r, sigma, n_simulations, option_type, average_type):
    if average_type == "arithmetic":
        return monte_carlo_asian_arithmetic(S, K, T, r, sigma, n_simulations, option_type)
    elif average_type == "geometric":
        return monte_carlo_asian_geometric(S, K, T, r, sigma, n_simulations, option_type)
    else:
        raise ValueError("average_type must be either 'arithmetic' or 'geometric'.")

def delta(S, K, T, r, sigma, n_simulations=100000, option_type="call", average_type="arithmetic"):
    h = 0.01 * S
    V_plus = price_asian_option(S + h, K, T, r, sigma, n_simulations, option_type, average_type)
    V_minus = price_asian_option(S - h, K, T, r, sigma, n_simulations, option_type, average_type)
    return (V_plus - V_minus) / (2 * h)

def gamma(S, K, T, r, sigma, n_simulations=100000, option_type="call", average_type="arithmetic"):
    h = 0.01 * S
    V_plus = price_asian_option(S + h, K, T, r, sigma, n_simulations, option_type, average_type)
    V = price_asian_option(S, K, T, r, sigma, n_simulations, option_type, average_type)
    V_minus = price_asian_option(S - h, K, T, r, sigma, n_simulations, option_type, average_type)
    return (V_plus - 2 * V + V_minus) / (h ** 2)

def vega(S, K, T, r, sigma, n_simulations=100000, option_type="call", average_type="arithmetic"):
    h = 0.01
    V_plus = price_asian_option(S, K, T, r, sigma + h, n_simulations, option_type, average_type)
    V_minus = price_asian_option(S, K, T, r, sigma - h, n_simulations, option_type, average_type)
    return (V_plus - V_minus) / (2 * h) / 100

def theta(S, K, T, r, sigma, n_simulations=100000, option_type="call", average_type="arithmetic"):
    h = 1 / 365
    if T - h <= 0:
        return np.nan
    V = price_asian_option(S, K, T, r, sigma, n_simulations, option_type, average_type)
    V_minus = price_asian_option(S, K, T - h, r, sigma, n_simulations, option_type, average_type)
    return (V_minus - V) / h

def rho(S, K, T, r, sigma, n_simulations=100000, option_type="call", average_type="arithmetic"):
    h = 0.0001
    V_plus = price_asian_option(S, K, T, r + h, sigma, n_simulations, option_type, average_type)
    V_minus = price_asian_option(S, K, T, r - h, sigma, n_simulations, option_type, average_type)
    return (V_plus - V_minus) / (2 * h) / 100
