use crate::AlgorithmFamily;

#[derive(Debug, Clone)]
pub struct Observation {
    pub chain: String,
    pub public_key_exposed: bool,
    pub signature_family: AlgorithmFamily,
    pub high_value: bool,
    pub high_frequency: bool,
    pub pq_authorization_available: bool,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Urgency { Low, Medium, High, Critical }
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Action { Monitor, RotateClassicalKey, RotateToUnexposedScript, AdoptHybridAuthorization }
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Decision { pub urgency: Urgency, pub action: Action, pub reasons: Vec<&'static str> }

pub fn evaluate(o: &Observation) -> Decision {
    if !o.public_key_exposed {
        return Decision { urgency: Urgency::Low, action: Action::Monitor, reasons: vec!["PUBLIC_KEY_NOT_EXPOSED"] };
    }
    let mut reasons=vec!["PUBLIC_KEY_EXPOSED"];
    let urgency = if o.high_value {
        reasons.push("HIGH_VALUE_SUBJECT"); Urgency::Critical
    } else if o.high_frequency {
        reasons.push("HIGH_SPEND_FREQUENCY"); Urgency::High
    } else { Urgency::Medium };

    let action = if o.pq_authorization_available {
        Action::AdoptHybridAuthorization
    } else if o.chain.eq_ignore_ascii_case("bitcoin") {
        Action::RotateToUnexposedScript
    } else {
        Action::RotateClassicalKey
    };
    Decision { urgency, action, reasons }
}
