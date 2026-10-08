use qinu_core::Observation;
use serde::{Deserialize, Serialize};
use sha3::{Digest, Keccak256};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct EvidenceEnvelope {
    pub observer_id: String,
    pub observed_at_unix: u64,
    pub sequence: u64,
    pub observation: Observation,
}

pub fn canonical_digest(envelope: &EvidenceEnvelope) -> [u8; 32] {
    let bytes = serde_json::to_vec(envelope).expect("serializable envelope");
    let mut h = Keccak256::new();
    h.update(b"QINU_EVIDENCE_V1");
    h.update(bytes);
    h.finalize().into()
}

pub fn digest_hex(envelope: &EvidenceEnvelope) -> String {
    canonical_digest(envelope).iter().map(|b| format!("{b:02x}")).collect()
}
