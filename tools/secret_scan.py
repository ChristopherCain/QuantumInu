from pathlib import Path
import re,sys
R=Path(__file__).resolve().parents[1]
rules=[re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),re.compile(r"\bAKIA[0-9A-Z]{16}\b"),re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")]
hits=[]
for p in R.rglob("*"):
    if not p.is_file() or any(x in p.parts for x in (".git","target","node_modules","dist")): continue
    try:s=p.read_text()
    except:continue
    if any(r.search(s) for r in rules): hits.append(str(p.relative_to(R)))
if hits: print(*hits,sep="\\n");sys.exit(1)
print("secret-pattern scan: OK")
