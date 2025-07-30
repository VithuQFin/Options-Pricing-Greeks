from simulations.monte_carlo import (
    monte_carlo_asian_arithmetic,
    monte_carlo_asian_geometric
)

def price_asian_arithmetic_mc(*args, **kwargs):
    return monte_carlo_asian_arithmetic(*args, **kwargs)

def price_asian_geometric_mc(*args, **kwargs):
    return monte_carlo_asian_geometric(*args, **kwargs)
