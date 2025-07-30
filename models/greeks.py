import numpy as np
from scipy.stats import norm

def d1(S, K, T, r, sigma):
    return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

def d2(S, K, T, r, sigma):
    return d1(S, K, T, r, sigma) - sigma * np.sqrt(T)

def delta(S, K, T, r, sigma, option_type):
    d_1 = d1(S, K, T, r, sigma)
    if option_type == "call":
        return norm.cdf(d_1)
    else:
        return -norm.cdf(-d_1)

def gamma(S, K, T, r, sigma):
    d_1 = d1(S, K, T, r, sigma)
    return norm.pdf(d_1) / (S * sigma * np.sqrt(T))

def vega(S, K, T, r, sigma):
    d_1 = d1(S, K, T, r, sigma)
    return S * norm.pdf(d_1) * np.sqrt(T) / 100

def theta(S, K, T, r, sigma, option_type):
    d_1 = d1(S, K, T, r, sigma)
    d_2 = d2(S, K, T, r, sigma)
    if option_type == "call":
        return (-S * norm.pdf(d_1) * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d_2)) / 365
    else:
        return (-S * norm.pdf(d_1) * sigma / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d_2)) / 365

def rho(S, K, T, r, sigma, option_type):
    d_2 = d2(S, K, T, r, sigma)
    if option_type == "call":
        return K * T * np.exp(-r * T) * norm.cdf(d_2) / 100
    else:
        return -K * T * np.exp(-r * T) * norm.cdf(-d_2) / 100
