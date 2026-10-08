from pathlib import Path
import json,time
p=Path(__file__).parents[1]/"specs/test-vectors/observations.json"
rows=json.loads(p.read_text())
n=10000
t=time.perf_counter()
for _ in range(n):
    for row in rows:
        hash(json.dumps(row["observation"],sort_keys=True))
dt=time.perf_counter()-t
print(json.dumps({"benchmark":"vector-canonicalization","iterations":n*len(rows),"seconds":dt},indent=2))
