from pathlib import Path
import re
ROOT=Path(__file__).parents[1]
patterns=[
 re.compile(r"AKIA[0-9A-Z]{16}"),
 re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
 re.compile(r"(?i)(api[_-]?key|secret[_-]?key)\s*[=:]\s*['\"][^'\"]{12,}"),
]
hits=[]
for p in ROOT.rglob("*"):
    if not p.is_file() or ".git" in p.parts: continue
    try:s=p.read_text(encoding="utf-8")
    except Exception:continue
    for pat in patterns:
        if pat.search(s):hits.append(str(p.relative_to(ROOT)))
if hits: raise SystemExit("possible secrets: "+", ".join(sorted(set(hits))))
print("secret scan: OK")
