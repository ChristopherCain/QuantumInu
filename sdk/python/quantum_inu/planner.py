from dataclasses import dataclass
@dataclass(frozen=True)
class Observation:
    chain:str; subject:str; public_key_exposed:bool; signature_family:str
    high_value:bool=False; high_frequency:bool=False; pq_authorization_available:bool=False
@dataclass(frozen=True)
class Assessment: urgency:str; action:str; reasons:tuple[str,...]

def plan_migration(o:Observation)->Assessment:
    if not o.public_key_exposed: return Assessment("low","monitor",("PUBLIC_KEY_NOT_EXPOSED",))
    reasons=["PUBLIC_KEY_EXPOSED"]; urgency="medium"
    if o.high_frequency: urgency="high"; reasons.append("HIGH_SPEND_FREQUENCY")
    if o.high_value: urgency="critical"; reasons.append("HIGH_VALUE_SUBJECT")
    action=("adopt_hybrid_authorization" if o.pq_authorization_available else
            "rotate_to_unexposed_script" if o.chain.lower()=="bitcoin" else "rotate_classical_key")
    return Assessment(urgency,action,tuple(reasons))
