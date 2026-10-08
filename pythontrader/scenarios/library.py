SCENARIOS={"flash_crash":{"equity":-.12,"crypto":-.20,"fx":.015},"risk_on":{"equity":.05,"crypto":.09,"fx":-.005},"vol_shock":{"equity":-.04,"crypto":-.08,"fx":.01}}
def shock_for(name:str,asset_class:str)->float:return SCENARIOS.get(name,{}).get(asset_class,0.0)
