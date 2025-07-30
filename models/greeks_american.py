import numpy as np
from models.crr import crr_price

def delta(S, K, T, r, sigma, N=100, option_type="call"):
    """
    Approximates Delta for an American option using finite difference on CRR tree.

    Δ ≈ (V(S+h) - V(S−h)) / (2h)
    """
    h = 0.01 * S  # Small change in spot
    V_plus = crr_price(S + h, K, T, r, sigma, N, option_type, american=True)
    V_minus = crr_price(S - h, K, T, r, sigma, N, option_type, american=True)
    return (V_plus - V_minus) / (2 * h)

def gamma(S, K, T, r, sigma, N=100, option_type="call"):
    """
    Approximates Gamma for an American option using central finite differences.

    Γ ≈ (V(S+h) - 2V(S) + V(S−h)) / h²
    """
    h = 0.01 * S
    V_plus = crr_price(S + h, K, T, r, sigma, N, option_type, american=True)
    V = crr_price(S, K, T, r, sigma, N, option_type, american=True)
    V_minus = crr_price(S - h, K, T, r, sigma, N, option_type, american=True)
    return (V_plus - 2 * V + V_minus) / (h ** 2)

def vega(S, K, T, r, sigma, N=100, option_type="call"):
    """
    Approximates Vega using finite differences on volatility.
    """
    h = 0.01
    V_plus = crr_price(S, K, T, r, sigma + h, N, option_type, american=True)
    V_minus = crr_price(S, K, T, r, sigma - h, N, option_type, american=True)
    return (V_plus - V_minus) / (2 * h) / 100  # scale per 1% change

def theta(S, K, T, r, sigma, N=100, option_type="call"):
    """
    Approximates Theta using backward finite difference on time.
    """
    h = 1/365  # One day
    if T - h <= 0:
        return np.nan  # avoid negative maturity
    V = crr_price(S, K, T, r, sigma, N, option_type, american=True)
    V_minus = crr_price(S, K, T - h, r, sigma, N, option_type, american=True)
    return (V_minus - V) / h

def rho(S, K, T, r, sigma, N=100, option_type="call"):
    """
    Approximates Rho using finite difference on interest rate.
    """
    h = 0.0001
    V_plus = crr_price(S, K, T, r + h, sigma, N, option_type, american=True)
    V_minus = crr_price(S, K, T, r - h, sigma, N, option_type, american=True)
    return (V_plus - V_minus) / (2 * h) / 100  # scale per 1% change
