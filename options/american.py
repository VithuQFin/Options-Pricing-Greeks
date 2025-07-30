from models.crr import crr_price

def price_american_crr(*args, **kwargs):
    return crr_price(*args, american=True, **kwargs)
