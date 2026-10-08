from .model import Observation, Assessment, Breakdown

def evaluate(o: Observation) -> Assessment:
    reasons:list[str]=[]
    b = dict(exposure_age=0,value_at_risk=0,frequency=0,key_reuse=0,legacy_signature=0,chain_latency=0,replay_surface=0,pq_credit=0,hybrid_credit=0)
    if o.public_key_exposed:
        reasons.append("PUBLIC_KEY_EXPOSED")
        b["exposure_age"]=14 if o.exposure_age_blocks>=100_000 else 7
        if o.exposure_age_blocks>=100_000: reasons.append("EXPOSURE_AGE_HIGH")
    else:
        reasons.append("PUBLIC_KEY_NOT_EXPOSED")
    if o.value_at_risk_usd>=1_000_000: b["value_at_risk"]=22; reasons.append("HIGH_VALUE_SUBJECT")
    elif o.value_at_risk_usd>=100_000: b["value_at_risk"]=12
    elif o.value_at_risk_usd>=10_000: b["value_at_risk"]=6
    if o.signatures_per_day>=1000: b["frequency"]=16; reasons.append("HIGH_SPEND_FREQUENCY")
    elif o.signatures_per_day>=100: b["frequency"]=8
    if o.key_reuse_detected: b["key_reuse"]=20; reasons.append("KEY_REUSE_DETECTED")
    if o.signature_family in {"secp256k1","ed25519"}: b["legacy_signature"]=12; reasons.append("LEGACY_SIGNATURE_ONLY")
    if o.chain_upgrade_latency_days>=365: b["chain_latency"]=8; reasons.append("CHAIN_UPGRADE_LATENCY_HIGH")
    if o.replay_surface_present: b["replay_surface"]=10; reasons.append("REPLAY_SURFACE_PRESENT")
    if o.pq_authorization_available: b["pq_credit"]=-14; reasons.append("PQ_AUTHORIZATION_AVAILABLE")
    if o.hybrid_authorization_available: b["hybrid_credit"]=-6; reasons.append("HYBRID_AUTH_AVAILABLE")
    score=max(0,min(100,sum(b.values())))
    urgency,action=("low","monitor") if score<20 else ("medium","prepare-migration") if score<45 else ("high","migrate") if score<70 else ("critical","isolate-and-migrate")
    return Assessment(score,urgency,action,tuple(reasons),Breakdown(**b))
