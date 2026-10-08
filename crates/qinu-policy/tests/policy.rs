use qinu_core::{Observation, SignatureFamily, Urgency, Action};
use qinu_policy::evaluate;

fn base() -> Observation {
    Observation {
        subject: "0xabc".into(), chain: "ethereum".into(),
        public_key_exposed: false, exposure_age_blocks: 0,
        value_at_risk_usd: 0, signatures_per_day: 1,
        key_reuse_detected: false, replay_surface_present: false,
        signature_family: SignatureFamily::Secp256k1,
        pq_authorization_available: false, hybrid_authorization_available: false,
        chain_upgrade_latency_days: 30,
    }
}

#[test]
fn low_subject_is_monitor() {
    let a = evaluate(&base());
    assert_eq!(a.urgency, Urgency::Low);
    assert_eq!(a.action, Action::Monitor);
}

#[test]
fn exposed_high_value_reused_key_is_critical() {
    let mut o = base();
    o.public_key_exposed = true;
    o.exposure_age_blocks = 500_000;
    o.value_at_risk_usd = 2_000_000;
    o.signatures_per_day = 5_000;
    o.key_reuse_detected = true;
    o.replay_surface_present = true;
    o.chain_upgrade_latency_days = 800;
    let a = evaluate(&o);
    assert_eq!(a.urgency, Urgency::Critical);
    assert_eq!(a.action, Action::IsolateAndMigrate);
    assert!(a.score >= 70);
}

#[test]
fn pq_capability_reduces_score() {
    let mut a = base();
    a.public_key_exposed = true;
    a.value_at_risk_usd = 500_000;
    let mut b = a.clone();
    b.pq_authorization_available = true;
    assert!(evaluate(&b).score < evaluate(&a).score);
}
