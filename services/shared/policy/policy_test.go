package policy
import (
  "testing"
  "quantuminu/services/shared/model"
)
func TestCriticalPath(t *testing.T){
  o:=model.Observation{PublicKeyExposed:true,ExposureAgeBlocks:200000,ValueAtRiskUSD:2000000,SignaturesPerDay:5000,KeyReuseDetected:true,ReplaySurfacePresent:true,SignatureFamily:model.Secp256k1,ChainUpgradeLatencyDays:500}
  a:=Evaluate(o)
  if a.Urgency!="critical"{t.Fatalf("got %s",a.Urgency)}
}
func TestPQCredit(t *testing.T){
  o:=model.Observation{PublicKeyExposed:true,ValueAtRiskUSD:200000,SignatureFamily:model.Secp256k1}
  a:=Evaluate(o);o.PQAuthorizationAvailable=true;b:=Evaluate(o)
  if b.Score>=a.Score{t.Fatal("PQ credit did not reduce score")}
}
