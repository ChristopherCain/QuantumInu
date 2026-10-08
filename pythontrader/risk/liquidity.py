def participation_cap(adv_or_liquidity,asset_class):
    p={"equity":.02,"etf":.03,"fx":.01,"crypto":.015,"memecoin":.0025,"perp":.01,"future":.015}.get(asset_class,.01)
    return max(0.0,adv_or_liquidity*p)
def impact_bps(order_notional,liquidity):
    if liquidity<=0:return 10_000.0
    return min(10_000.0,12.0*(order_notional/liquidity)**.5)
