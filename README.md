<p align="center"><img src="docs/assets/quantum-inu.png" width="220" alt="Quantum Inu"></p>

# Quantum Inu
**The Universal Post-Quantum Security Layer for Crypto**

Quantum Inu is an Ethereum-native, multichain **research implementation** for cryptographic migration, exposed-key monitoring, algorithm agility, and chain-specific authorization adapters.

> Status: research / pre-audit. This repository does not claim that Ethereum, Bitcoin, Solana, or any other chain is already quantum-resistant end-to-end.

## Architecture

```text
                    qinu-core (Rust)
              capability + migration policy
                         |
          +--------------+--------------+
          |              |              |
      Ethereum        Bitcoin        Solana
      adapter          policy         policy
          |              |              |
          +------- Threat Sentinel ------+
                    (Go service)
                         |
               SDKs + evidence schema
               TypeScript / Python
```

## Components

| Component | Language | Purpose |
|---|---|---|
| `crates/qinu-core` | Rust | deterministic capability registry + migration policy |
| `services/threat-sentinel` | Go | normalized exposed-key risk analysis |
| `sdk/typescript` | TypeScript | typed client + planner |
| `sdk/python` | Python | migration planner + scripting SDK |
| `contracts` | Solidity | account-level migration metadata registry |
| `specs` | JSON/Markdown | portable observation and evidence formats |
| `docs` | EN/RU/ZH | architecture, threat model, chain boundaries |

## Core model

Quantum Inu separates five concerns:

1. **Observe** public-key exposure and authorization state.
2. **Classify** urgency with deterministic reason codes.
3. **Negotiate** classical / hybrid / post-quantum capabilities.
4. **Migrate** through a chain-specific adapter.
5. **Verify** observations with signed evidence envelopes.

Supported algorithm identifiers include `ML-KEM`, `ML-DSA`, `SLH-DSA`, `ECDSA-SECP256K1`, `ED25519`, and hybrid authorization suites.

Cryptographic primitives are intentionally delegated to audited implementations; this repository does not implement ML-KEM/ML-DSA/SLH-DSA from scratch.

## Example decision

```json
{
  "chain": "bitcoin",
  "subject": "bc1q...",
  "public_key_exposed": true,
  "signature_family": "ecdsa-secp256k1",
  "high_frequency": true,
  "pq_authorization_available": false
}
```

Result:

```text
urgency  HIGH
action   ROTATE_TO_UNEXPOSED_SCRIPT
reason   PUBLIC_KEY_EXPOSED, HIGH_SPEND_FREQUENCY
```

## Quick verification

```bash
python -m unittest discover sdk/python/tests
python tools/repo_invariants.py
python tools/secret_scan.py

cargo test --manifest-path crates/qinu-core/Cargo.toml

cd services/threat-sentinel
go test ./...
```

## What is implemented

- deterministic migration policy engine;
- algorithm capability registry;
- public-key exposure schema;
- Go threat sentinel;
- Python and TypeScript planners;
- Solidity migration-state registry;
- multilingual documentation;
- CI, security policy, invariant and secret-pattern checks.

## Integration boundaries

**Ethereum:** account-level smart-account / authorization migration is possible; consensus-wide signature migration requires protocol support.

**Bitcoin:** adapters can reason about key exposure and rotation; post-quantum consensus signatures require a network upgrade.

**Solana:** adapters can coordinate program/account authority migration; network-wide Ed25519 replacement is protocol-level.

## Security

Read [`SECURITY.md`](SECURITY.md) and [`docs/security/THREAT_MODEL.md`](docs/security/THREAT_MODEL.md).

## Roadmap

- audited PQ provider adapters;
- hybrid EIP-4337 authorization module;
- Bitcoin exposure indexer;
- Solana authority migration adapter;
- multi-observer evidence verification;
- reproducible benchmark corpus;
- external review.

## License

MIT.
