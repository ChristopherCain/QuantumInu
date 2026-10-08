export type SignatureFamily = "secp256k1" | "ed25519" | "wots-k256" | "ml-dsa" | "slh-dsa" | "unknown";
export interface Observation {
    subject: string;
    chain: string;
    publicKeyExposed: boolean;
    exposureAgeBlocks: number;
    valueAtRiskUsd: number;
    signaturesPerDay: number;
    keyReuseDetected: boolean;
    replaySurfacePresent: boolean;
    signatureFamily: SignatureFamily;
    pqAuthorizationAvailable: boolean;
    hybridAuthorizationAvailable: boolean;
    chainUpgradeLatencyDays: number;
}
export interface Assessment {
    score: number;
    urgency: "low" | "medium" | "high" | "critical";
    action: "monitor" | "prepare-migration" | "migrate" | "isolate-and-migrate";
    reasons: string[];
}
export declare function evaluate(o: Observation): Assessment;
