from quantum_inu import Observation, evaluate

def obs(**changes):
    d=dict(subject="x",chain="ethereum",public_key_exposed=False,exposure_age_blocks=0,value_at_risk_usd=0,signatures_per_day=1,key_reuse_detected=False,replay_surface_present=False,signature_family="secp256k1",pq_authorization_available=False,hybrid_authorization_available=False,chain_upgrade_latency_days=30)
    d.update(changes); return Observation(**d)

def test_low():
    assert evaluate(obs()).urgency=="low"

def test_critical():
    a=evaluate(obs(public_key_exposed=True,exposure_age_blocks=500000,value_at_risk_usd=2000000,signatures_per_day=5000,key_reuse_detected=True,replay_surface_present=True,chain_upgrade_latency_days=800))
    assert a.urgency=="critical"

def test_pq_credit():
    base=obs(public_key_exposed=True,value_at_risk_usd=500000)
    assert evaluate(obs(public_key_exposed=True,value_at_risk_usd=500000,pq_authorization_available=True)).score < evaluate(base).score
