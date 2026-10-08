from pathlib import Path
import json
ROOT=Path(__file__).parents[2]
def test_vectors_have_unique_names():
    rows=json.loads((ROOT/"specs/test-vectors/observations.json").read_text())
    names=[r["name"] for r in rows]
    assert len(names)==len(set(names))
