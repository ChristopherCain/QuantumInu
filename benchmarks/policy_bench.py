from time import perf_counter
from pathlib import Path
import json, sys
sys.path.insert(0,str(Path(__file__).parents[1]/"sdk/python"))
from quantum_inu import Observation,evaluate

o=Observation("x","ethereum",True,200000,250000,500,False,True,"secp256k1",False,False,400)
N=100_000
t0=perf_counter()
for _ in range(N): evaluate(o)
dt=perf_counter()-t0
print(json.dumps({"benchmark":"python-policy","iterations":N,"seconds":dt,"ops_per_second":N/dt},indent=2))
