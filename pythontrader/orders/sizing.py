def volatility_target(equity,price,vol,target_vol=.01,max_fraction=.1):
 if price<=0 or vol<=0:return 0.0
 notional=min(equity*max_fraction,equity*target_vol/vol);return max(0,notional/price)
