package analyzer
import ("testing";"quantum-inu/threat-sentinel/internal/model")
func TestExposed(t *testing.T){
    got:=Assess(model.Observation{Chain:"bitcoin",PublicKeyExposed:true,HighFrequency:true})
    if got.Urgency!="high" || got.Action!="rotate_to_unexposed_script" { t.Fatalf("%+v",got) }
}
