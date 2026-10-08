# Threat Model
Assets: signing keys, authorization policy, migration metadata, threat observations, algorithm-registry state.

Adversaries:
- classical key thief;
- future cryptographically relevant quantum attacker;
- malicious observer;
- downgrade attacker;
- compromised migration coordinator;
- replay attacker.

Controls:
- monotonic migration epochs;
- explicit algorithm IDs;
- deprecation registry;
- deterministic reason codes;
- signed evidence format;
- no bespoke cryptographic primitive implementations.
