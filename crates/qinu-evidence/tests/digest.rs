use qinu_core::{Observation, SignatureFamily};
use qinu_evidence::{EvidenceEnvelope, canonical_digest};

#[test]
fn digest_changes_with_sequence() {
    let o = Observation {
        subject:"x".into(), chain:"ethereum".into(), public_key_exposed:false,
        exposure_age_blocks:0, value_at_risk_usd:0, signatures_per_day:0,
        key_reuse_detected:false, replay_surface_present:false,
        signature_family:SignatureFamily::Secp256k1,
        pq_authorization_available:false, hybrid_authorization_available:false,
        chain_upgrade_latency_days:0,
    };
    let a = EvidenceEnvelope { observer_id:"obs-1".into(), observed_at_unix:1, sequence:1, observation:o.clone() };
    let b = EvidenceEnvelope { sequence:2, ..a.clone() };
    assert_ne!(canonical_digest(&a), canonical_digest(&b));
}
