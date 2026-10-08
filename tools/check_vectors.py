from pathlib import Path
import json,sys
ROOT=Path(__file__).parents[1]
sys.path.insert(0,str(ROOT/"sdk/python"))
from quantum_inu import Observation,evaluate
rows=json.loads((ROOT/"specs/test-vectors/observations.json").read_text())
for row in rows:
    o=row["observation"]
    obs=Observation(
      o["subject"],o["chain"],o["public_key_exposed"],o["exposure_age_blocks"],o["value_at_risk_usd"],
      o["signatures_per_day"],o["key_reuse_detected"],o["replay_surface_present"],o["signature_family"],
      o["pq_authorization_available"],o["hybrid_authorization_available"],o["chain_upgrade_latency_days"]
    )
    a=evaluate(obs)
    exp=row["expected"]
    assert a.urgency==exp["urgency"],(row["name"],a.urgency,exp["urgency"])
    assert a.action==exp["action"],(row["name"],a.action,exp["action"])
print(f"vectors: {len(rows)} OK")
