# Security Policy

Quantum Inu is research/pre-audit software.

## Reporting

Do not open public issues for undisclosed vulnerabilities. Provide a minimal reproducer,
affected component, expected impact, and environment details to the maintainers through
a private security advisory.

## Scope

In scope:
- authorization bypass
- replay protection failures
- key-rotation failures
- malformed evidence acceptance
- capability downgrade
- score manipulation
- signature-verification discrepancies

Out of scope:
- claims that account-level authorization upgrades consensus
- attacks requiring modified local test fixtures
- denial of service caused only by intentionally unbounded benchmark inputs
