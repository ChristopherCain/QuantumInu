from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Observation:
    subject: str
    chain: str
    public_key_exposed: bool
    exposure_age_blocks: int
    value_at_risk_usd: int
    signatures_per_day: int
    key_reuse_detected: bool
    replay_surface_present: bool
    signature_family: str
    pq_authorization_available: bool
    hybrid_authorization_available: bool
    chain_upgrade_latency_days: int

@dataclass(frozen=True, slots=True)
class Breakdown:
    exposure_age: int = 0
    value_at_risk: int = 0
    frequency: int = 0
    key_reuse: int = 0
    legacy_signature: int = 0
    chain_latency: int = 0
    replay_surface: int = 0
    pq_credit: int = 0
    hybrid_credit: int = 0

@dataclass(frozen=True, slots=True)
class Assessment:
    score: int
    urgency: str
    action: str
    reasons: tuple[str, ...]
    breakdown: Breakdown
