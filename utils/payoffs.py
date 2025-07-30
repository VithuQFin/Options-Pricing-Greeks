# utils/payoffs.py

import numpy as np

def european_payoff(ST, K, option_type="call"):
    if option_type == "call":
        return np.maximum(ST - K, 0)
    elif option_type == "put":
        return np.maximum(K - ST, 0)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

def digital_payoff(ST, K, option_type="call", payout=1.0):
    if option_type == "call":
        return payout * (ST > K)
    elif option_type == "put":
        return payout * (ST < K)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

def asian_arithmetic_payoff(path, K, option_type="call"):
    avg_price = np.mean(path)
    return european_payoff(avg_price, K, option_type)

def asian_geometric_payoff(path, K, option_type="call"):
    geo_mean = np.exp(np.mean(np.log(path)))
    return european_payoff(geo_mean, K, option_type)
