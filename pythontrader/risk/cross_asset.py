from __future__ import annotations
from collections import defaultdict
class CrossAssetRisk:
    def __init__(self,limits=None):
        self.limits=limits or {"equity":.45,"etf":.35,"fx":.30,"crypto":.30,"memecoin":.08,"perp":.20,"future":.25,"commodity":.20,"index":.25,"option":.10}
    def class_exposure(self,positions,instruments,marks):
        out=defaultdict(float)
        for s,p in positions.items():
            if s not in marks:continue
            i=instruments.get(s);out[i.asset_class.value]+=abs(p.qty*marks[s]*i.multiplier)
        return dict(out)
    def concentration_breaches(self,positions,instruments,marks,equity):
        if equity<=0:return ["non-positive equity"]
        e=self.class_exposure(positions,instruments,marks);return [f"{k}:{v/equity:.2%}>{self.limits.get(k,1):.2%}" for k,v in e.items() if v/equity>self.limits.get(k,1)]
