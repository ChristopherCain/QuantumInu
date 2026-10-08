use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum SignatureFamily {
    Secp256k1,
    Ed25519,
    WotsK256,
    MlDsa,
    SlhDsa,
    Unknown,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Observation {
    pub subject: String,
    pub chain: String,
    pub public_key_exposed: bool,
    pub exposure_age_blocks: u64,
    pub value_at_risk_usd: u64,
    pub signatures_per_day: u32,
    pub key_reuse_detected: bool,
    pub replay_surface_present: bool,
    pub signature_family: SignatureFamily,
    pub pq_authorization_available: bool,
    pub hybrid_authorization_available: bool,
    pub chain_upgrade_latency_days: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum Urgency { Low, Medium, High, Critical }

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum Action { Monitor, PrepareMigration, Migrate, IsolateAndMigrate }

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ScoreBreakdown {
    pub exposure_age: u16,
    pub value_at_risk: u16,
    pub frequency: u16,
    pub key_reuse: u16,
    pub legacy_signature: u16,
    pub chain_latency: u16,
    pub replay_surface: u16,
    pub pq_credit: i16,
    pub hybrid_credit: i16,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Assessment {
    pub score: u16,
    pub urgency: Urgency,
    pub action: Action,
    pub reasons: Vec<String>,
    pub breakdown: ScoreBreakdown,
}
