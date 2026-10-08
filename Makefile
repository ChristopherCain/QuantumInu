.PHONY: test verify
test:
	python -m unittest discover sdk/python/tests
	cargo test --manifest-path crates/qinu-core/Cargo.toml
	cd services/threat-sentinel && go test ./...
verify:
	python tools/repo_invariants.py
	python tools/secret_scan.py
