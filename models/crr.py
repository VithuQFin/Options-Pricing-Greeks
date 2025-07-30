import numpy as np

def crr_price(S, K, T, r, sigma, N=100, option_type="call", american=False):
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)

    # Arbre des prix
    prices = np.zeros((N + 1, N + 1))
    for i in range(N + 1):
        for j in range(i + 1):
            prices[j, i] = S * (u ** (i - j)) * (d ** j)

    # Arbre des payoffs
    values = np.zeros_like(prices)
    if option_type == "call":
        values[:, N] = np.maximum(prices[:, N] - K, 0)
    else:
        values[:, N] = np.maximum(K - prices[:, N], 0)

    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            continuation = np.exp(-r * dt) * (p * values[j, i+1] + (1 - p) * values[j+1, i+1])
            if american:
                intrinsic = max(0, prices[j, i] - K) if option_type == "call" else max(0, K - prices[j, i])
                values[j, i] = max(continuation, intrinsic)
            else:
                values[j, i] = continuation

    return values[0, 0]
