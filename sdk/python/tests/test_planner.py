import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from quantum_inu import Observation,plan_migration
def test_bitcoin():
    r=plan_migration(Observation("bitcoin","bc1",True,"ecdsa",high_frequency=True))
    assert r.urgency=="high" and r.action=="rotate_to_unexposed_script"
