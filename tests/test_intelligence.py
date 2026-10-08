from pythontrader.intelligence.brain import TradingBrain
def test_brain_emits_complete_decision():
    d=TradingBrain().infer({"momentum":.02,"imbalance":.6,"volatility":.01,"zscore":.5})
    assert d.action in {"buy","sell","hold"};assert len(d.votes)==4;assert 0<d.confidence<=1
