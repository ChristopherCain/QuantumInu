from pathlib import Path
ROOT=Path(__file__).parents[2]
def test_security_docs_present():
    for name in ["THREAT_MODEL.md","CHAIN_BOUNDARIES.md","CRYPTOGRAPHIC_BOUNDARIES.md","AUDIT_SCOPE.md"]:
        assert (ROOT/"docs/quantum-inu"/name).exists()
