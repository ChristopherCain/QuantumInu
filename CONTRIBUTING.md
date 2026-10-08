# Contributing
PRs should be reviewable and test-backed.

Run:
```bash
python -m unittest discover sdk/python/tests
python tools/repo_invariants.py
cargo test --manifest-path crates/qinu-core/Cargo.toml
cd services/threat-sentinel && go test ./...
```

Use real authorship and real commit history. Do not manufacture dates, contributors, stars, or activity.
