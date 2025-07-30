import numpy as np
from simulations.monte_carlo import monte_carlo_digital

def delta(S, K, T, r, sigma, n_simulations=100000, option_type="call"):
    h = 0.01 * S
    V_plus = monte_carlo_digital(S + h, K, T, r, sigma, n_simulations, option_type)
    V_minus = monte_carlo_digital(S - h, K, T, r, sigma, n_simulations, option_type)
    return (V_plus - V_minus) / (2 * h)

def gamma(S, K, T, r, sigma, n_simulations=100000, option_type="call"):
    h = 0.01 * S
    V_plus = monte_carlo_digital(S + h, K, T, r, sigma, n_simulations, option_type)
    V = monte_carlo_digital(S, K, T, r, sigma, n_simulations, option_type)
    V_minus = monte_carlo_digital(S - h, K, T, r, sigma, n_simulations, option_type)
    return (V_plus - 2 * V + V_minus) / (h ** 2)

def vega(S, K, T, r, sigma, n_simulations=100000, option_type="call"):
    h = 0.01
    V_plus = monte_carlo_digital(S, K, T, r, sigma + h, n_simulations, option_type)
    V_minus = monte_carlo_digital(S, K, T, r, sigma - h, n_simulations, option_type)
    return (V_plus - V_minus) / (2 * h) / 100

def theta(S, K, T, r, sigma, n_simulations=100000, option_type="call"):
    h = 1 / 365
    if T - h <= 0:
        return np.nan
    V = monte_carlo_digital(S, K, T, r, sigma, n_simulations, option_type)
    V_minus = monte_carlo_digital(S, K, T - h, r, sigma, n_simulations, option_type)
    return (V_minus - V) / h

def rho(S, K, T, r, sigma, n_simulations=100000, option_type="call"):
    h = 0.0001
    V_plus = monte_carlo_digital(S, K, T, r + h, sigma, n_simulations, option_type)
    V_minus = monte_carlo_digital(S, K, T, r - h, sigma, n_simulations, option_type)
    return (V_plus - V_minus) / (2 * h) / 100
