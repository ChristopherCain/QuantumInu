package main
import (
  "encoding/json"
  "fmt"
  "os"
  "quantuminu/services/shared/model"
  "quantuminu/services/shared/policy"
)
type Plan struct{
  Subject string `json:"subject"`
  Chain string `json:"chain"`
  Action string `json:"action"`
  Priority string `json:"priority"`
  RequiresConsensusUpgrade bool `json:"requires_consensus_upgrade"`
}
func main(){
  var o model.Observation
  if err:=json.NewDecoder(os.Stdin).Decode(&o);err!=nil{panic(err)}
  a:=policy.Evaluate(o)
  requires:=o.Chain=="bitcoin" || o.Chain=="solana"
  p:=Plan{Subject:o.Subject,Chain:o.Chain,Action:a.Action,Priority:a.Urgency,RequiresConsensusUpgrade:requires}
  out,_:=json.MarshalIndent(p,"","  ");fmt.Println(string(out))
}
