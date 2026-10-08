use qinu_core::{
    Action,
    Observation,
    SignatureFamily,
    Urgency,
};
use qinu_policy::evaluate;

fn bitcoin_observation() -> Observation {
    Observation {
        subject: "bc1q-test-subject".into(),
        chain: "bitcoin".into(),
        public_key_exposed: true,
        exposure_age_blocks: 250_000,
        value_at_risk_usd: 500_000,
        signatures_per_day: 2_000,
        key_reuse_detected: false,
        replay_surface_present: false,
        signature_family: SignatureFamily::Secp256k1,
        pq_authorization_available: false,
        hybrid_authorization_available: false,
        chain_upgrade_latency_days: 900,
    }
}

#[test]
fn exposed_bitcoin_key_requires_migration() {
    let decision = evaluate(&bitcoin_observation());

    assert!(matches!(
        decision.urgency,
        Urgency::High | Urgency::Critical
    ));

    assert!(matches!(
        decision.action,
        Action::Migrate | Action::IsolateAndMigrate
    ));

    assert!(decision
        .reasons
        .iter()
        .any(|r| r == "PUBLIC_KEY_EXPOSED"));

    assert!(decision
        .reasons
        .iter()
        .any(|r| r == "LEGACY_SIGNATURE_ONLY"));
}
