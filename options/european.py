from simulations.monte_carlo import monte_carlo_european
from models.black_scholes import black_scholes_price

def price_european_mc(*args, **kwargs):
    return monte_carlo_european(*args, **kwargs)

def price_european_bs(*args, **kwargs):
    return black_scholes_price(*args, **kwargs)
