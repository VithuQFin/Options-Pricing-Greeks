import numpy as np

def simulate_gbm_paths(S0, T, r, sigma, n_simulations=100, n_steps=252):
    dt = T / n_steps
    Z = np.random.randn(n_simulations, n_steps)
    increments = (r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z
    log_paths = np.cumsum(increments, axis=1)
    paths = S0 * np.exp(log_paths)
    return np.hstack([S0 * np.ones((n_simulations, 1)), paths])
