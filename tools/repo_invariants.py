from pathlib import Path

ROOT = Path(__file__).parents[1]

required = [
    "README.md",
    "SECURITY.md",
    "contracts/src/QuantumInuAccount.sol",
    "crates/qinu-policy/src/lib.rs",
    "services/threat-sentinel/cmd/threat-sentinel/main.go",
    "specs/test-vectors/observations.json",
]

missing = [p for p in required if not (ROOT / p).exists()]
if missing:
    raise SystemExit("missing: " + ", ".join(missing))

forbidden = ["python" + "trader", "PYTHON" + "TRADER"]

hits = []

for p in ROOT.rglob("*"):
    if not p.is_file():
        continue

    if ".git" in p.parts:
        continue

    # don't scan this checker itself
    if p.resolve() == Path(__file__).resolve():
        continue

    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        continue

    for token in forbidden:
        if token in text:
            hits.append(f"{p.relative_to(ROOT)}:{token}")

if hits:
    raise SystemExit("forbidden references: " + "; ".join(hits))

print("repository invariants: OK")
