from pathlib import Path
import hashlib,json
ROOT=Path(__file__).parents[1]
files=[]
for p in sorted(ROOT.rglob("*")):
    if p.is_file() and ".git" not in p.parts and p.name!="MANIFEST.json":
        files.append({"path":str(p.relative_to(ROOT)).replace("\\","/"),"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"bytes":p.stat().st_size})
(ROOT/"MANIFEST.json").write_text(json.dumps({"files":files},indent=2))
print(len(files))
