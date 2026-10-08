from pathlib import Path
ROOT=Path(__file__).parents[1]
required=[
 "README.md","SECURITY.md","contracts/src/QuantumInuAccount.sol",
 "crates/qinu-policy/src/lib.rs","services/threat-sentinel/cmd/threat-sentinel/main.go",
 "specs/test-vectors/observations.json"
]
missing=[p for p in required if not (ROOT/p).exists()]
if missing: raise SystemExit("missing: "+", ".join(missing))
forbidden=["pythontrader","PYTHONTRADER"]
hits=[]
for p in ROOT.rglob("*"):
    if p.is_file() and ".git" not in p.parts:
        try: text=p.read_text(encoding="utf-8")
        except Exception: continue
        for token in forbidden:
            if token in text: hits.append(f"{p.relative_to(ROOT)}:{token}")
if hits: raise SystemExit("forbidden references: "+"; ".join(hits))
print("repository invariants: OK")
