from pythontrader.features.microprice import microprice
from pythontrader.features.volatility import realized_vol

def test_microprice_weights_opposite_side():assert microprice(99,101,3,1)==100.5
def test_volatility_nonnegative():assert realized_vol([.1,.2,.1,.05])>=0
