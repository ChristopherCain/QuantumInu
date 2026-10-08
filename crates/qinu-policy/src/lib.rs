use qinu_core::{
    Action, Assessment, Observation, ScoreBreakdown, SignatureFamily, Urgency,
    PUBLIC_KEY_EXPOSED, PUBLIC_KEY_NOT_EXPOSED, EXPOSURE_AGE_HIGH, HIGH_VALUE_SUBJECT,
    HIGH_SPEND_FREQUENCY, KEY_REUSE_DETECTED, LEGACY_SIGNATURE_ONLY,
    CHAIN_UPGRADE_LATENCY_HIGH, REPLAY_SURFACE_PRESENT,
    PQ_AUTHORIZATION_AVAILABLE, HYBRID_AUTH_AVAILABLE,
};

pub fn evaluate(o: &Observation) -> Assessment {
    let mut reasons = Vec::new();
    let mut b = ScoreBreakdown {
        exposure_age: 0, value_at_risk: 0, frequency: 0, key_reuse: 0,
        legacy_signature: 0, chain_latency: 0, replay_surface: 0,
        pq_credit: 0, hybrid_credit: 0,
    };

    if o.public_key_exposed {
        reasons.push(PUBLIC_KEY_EXPOSED.to_string());
        if o.exposure_age_blocks >= 100_000 {
            b.exposure_age = 14;
            reasons.push(EXPOSURE_AGE_HIGH.to_string());
        } else {
            b.exposure_age = 7;
        }
    } else {
        reasons.push(PUBLIC_KEY_NOT_EXPOSED.to_string());
    }

    if o.value_at_risk_usd >= 1_000_000 {
        b.value_at_risk = 22;
        reasons.push(HIGH_VALUE_SUBJECT.to_string());
    } else if o.value_at_risk_usd >= 100_000 {
        b.value_at_risk = 12;
    } else if o.value_at_risk_usd >= 10_000 {
        b.value_at_risk = 6;
    }

    if o.signatures_per_day >= 1000 {
        b.frequency = 16;
        reasons.push(HIGH_SPEND_FREQUENCY.to_string());
    } else if o.signatures_per_day >= 100 {
        b.frequency = 8;
    }

    if o.key_reuse_detected {
        b.key_reuse = 20;
        reasons.push(KEY_REUSE_DETECTED.to_string());
    }

    if matches!(o.signature_family, SignatureFamily::Secp256k1 | SignatureFamily::Ed25519) {
        b.legacy_signature = 12;
        reasons.push(LEGACY_SIGNATURE_ONLY.to_string());
    }

    if o.chain_upgrade_latency_days >= 365 {
        b.chain_latency = 8;
        reasons.push(CHAIN_UPGRADE_LATENCY_HIGH.to_string());
    }

    if o.replay_surface_present {
        b.replay_surface = 10;
        reasons.push(REPLAY_SURFACE_PRESENT.to_string());
    }

    if o.pq_authorization_available {
        b.pq_credit = -14;
        reasons.push(PQ_AUTHORIZATION_AVAILABLE.to_string());
    }
    if o.hybrid_authorization_available {
        b.hybrid_credit = -6;
        reasons.push(HYBRID_AUTH_AVAILABLE.to_string());
    }

    let raw = b.exposure_age as i32
        + b.value_at_risk as i32
        + b.frequency as i32
        + b.key_reuse as i32
        + b.legacy_signature as i32
        + b.chain_latency as i32
        + b.replay_surface as i32
        + b.pq_credit as i32
        + b.hybrid_credit as i32;

    let score = raw.clamp(0, 100) as u16;
    let (urgency, action) = match score {
        0..=19 => (Urgency::Low, Action::Monitor),
        20..=44 => (Urgency::Medium, Action::PrepareMigration),
        45..=69 => (Urgency::High, Action::Migrate),
        _ => (Urgency::Critical, Action::IsolateAndMigrate),
    };

    Assessment { score, urgency, action, reasons, breakdown: b }
}
