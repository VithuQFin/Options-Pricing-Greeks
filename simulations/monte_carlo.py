import numpy as np
from utils.payoffs import european_payoff
from utils.payoffs import asian_arithmetic_payoff
from utils.payoffs import asian_geometric_payoff
from utils.payoffs import digital_payoff

# -------------------------------
# Monte Carlo pour Option Européenne
# -------------------------------

def monte_carlo_european(S, K, T, r, sigma, n_simulations=10000, option_type="call"):
    """
    Calculate the price of a European option using Monte Carlo simulation.

    Parameters:
    S : float : Current stock price
    K : float : Strike price
    T : float : Time to expiration in years
    r : float : Risk-free interest rate (annualized)
    sigma : float : Volatility of the underlying asset (annualized)
    n_simulations : int : Number of Monte Carlo simulations to run
    option_type : str : 'call' for call option, 'put' for put option

    Returns:
    float : The estimated price of the option
    """
    np.random.seed(0)  # For reproducibility
    dt = T  # Time step is the total time to expiration for European options
    Z = np.random.normal(size=n_simulations)  # Standard normal random variables
    ST = S * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z)  # Simulated end stock prices

    payoffs = european_payoff(ST, K, option_type)  # Calculate payoffs

    discounted_payoff = np.exp(-r * T) * payoffs  # Discounted payoffs
    return np.mean(discounted_payoff)  # Return the average payoff as the option price

# -------------------------------
# Monte Carlo pour Option Digitale
# -------------------------------

def monte_carlo_digital(S0, K, T, r, sigma, option_type="call", payout=1.0, n_simulations=10000):
    Z = np.random.randn(n_simulations)
    ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

    payoff = digital_payoff(ST, K, option_type, payout)
    return np.exp(-r * T) * np.mean(payoff)


# -------------------------------
# Monte Carlo pour Option Asiatique Arithmétique
# -------------------------------

def monte_carlo_asian_arithmetic(S0, K, T, r, sigma, option_type="call", n_simulations=10000, n_steps=252):
    dt = T / n_steps
    discount_factor = np.exp(-r * T)

    payoffs = []

    for _ in range(n_simulations):
        prices = [S0]
        for _ in range(n_steps):
            z = np.random.randn()
            S_t = prices[-1] * np.exp((r - 0.5 * sigma**2)*dt + sigma*np.sqrt(dt)*z)
            prices.append(S_t)

        payoff = asian_arithmetic_payoff(prices, K, option_type)
        payoffs.append(payoff)

    return discount_factor * np.mean(payoffs)

# -------------------------------
# Monte Carlo pour Option Asiatique Géométrique
# -------------------------------

def monte_carlo_asian_geometric(S0, K, T, r, sigma, option_type="call", n_simulations=10000, n_steps=252):
    dt = T / n_steps
    discount_factor = np.exp(-r * T)

    payoffs = []

    for _ in range(n_simulations):
        prices = [S0]
        for _ in range(n_steps):
            z = np.random.randn()
            S_t = prices[-1] * np.exp((r - 0.5 * sigma**2)*dt + sigma*np.sqrt(dt)*z)
            prices.append(S_t)

        payoff = asian_geometric_payoff(prices, K, option_type)
        payoffs.append(payoff)

    return discount_factor * np.mean(payoffs)
