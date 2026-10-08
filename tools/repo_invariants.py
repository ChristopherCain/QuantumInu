from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[1]
req=["README.md","SECURITY.md","LICENSE","crates/qinu-core/Cargo.toml","services/threat-sentinel/go.mod",
"sdk/python/pyproject.toml","sdk/typescript/package.json","contracts/src/MigrationRegistry.sol","specs/exposure-observation.schema.json"]
bad=[x for x in req if not (R/x).exists()]
schema=json.loads((R/"specs/exposure-observation.schema.json").read_text())
if schema.get("additionalProperties") is not False: bad.append("schema additionalProperties must be false")
if bad: print("FAIL",*bad,sep="\n"); sys.exit(1)
print("repository invariants: OK")
