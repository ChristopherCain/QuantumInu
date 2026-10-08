export function evaluate(o) {
    const reasons = [];
    let score = 0;
    if (o.publicKeyExposed) {
        reasons.push("PUBLIC_KEY_EXPOSED");
        score += o.exposureAgeBlocks >= 100000 ? 14 : 7;
        if (o.exposureAgeBlocks >= 100000)
            reasons.push("EXPOSURE_AGE_HIGH");
    }
    else
        reasons.push("PUBLIC_KEY_NOT_EXPOSED");
    if (o.valueAtRiskUsd >= 1_000_000) {
        score += 22;
        reasons.push("HIGH_VALUE_SUBJECT");
    }
    else if (o.valueAtRiskUsd >= 100_000)
        score += 12;
    else if (o.valueAtRiskUsd >= 10_000)
        score += 6;
    if (o.signaturesPerDay >= 1000) {
        score += 16;
        reasons.push("HIGH_SPEND_FREQUENCY");
    }
    else if (o.signaturesPerDay >= 100)
        score += 8;
    if (o.keyReuseDetected) {
        score += 20;
        reasons.push("KEY_REUSE_DETECTED");
    }
    if (o.signatureFamily === "secp256k1" || o.signatureFamily === "ed25519") {
        score += 12;
        reasons.push("LEGACY_SIGNATURE_ONLY");
    }
    if (o.chainUpgradeLatencyDays >= 365) {
        score += 8;
        reasons.push("CHAIN_UPGRADE_LATENCY_HIGH");
    }
    if (o.replaySurfacePresent) {
        score += 10;
        reasons.push("REPLAY_SURFACE_PRESENT");
    }
    if (o.pqAuthorizationAvailable) {
        score -= 14;
        reasons.push("PQ_AUTHORIZATION_AVAILABLE");
    }
    if (o.hybridAuthorizationAvailable) {
        score -= 6;
        reasons.push("HYBRID_AUTH_AVAILABLE");
    }
    score = Math.max(0, Math.min(100, score));
    if (score >= 70)
        return { score, urgency: "critical", action: "isolate-and-migrate", reasons };
    if (score >= 45)
        return { score, urgency: "high", action: "migrate", reasons };
    if (score >= 20)
        return { score, urgency: "medium", action: "prepare-migration", reasons };
    return { score, urgency: "low", action: "monitor", reasons };
}
