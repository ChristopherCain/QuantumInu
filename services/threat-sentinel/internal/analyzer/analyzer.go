package analyzer
import "quantum-inu/threat-sentinel/internal/model"

func Assess(o model.Observation) model.Assessment {
    if !o.PublicKeyExposed { return model.Assessment{"low","monitor",[]string{"PUBLIC_KEY_NOT_EXPOSED"}} }
    reasons:=[]string{"PUBLIC_KEY_EXPOSED"}; urgency:="medium"
    if o.HighFrequency { urgency="high"; reasons=append(reasons,"HIGH_SPEND_FREQUENCY") }
    if o.HighValue { urgency="critical"; reasons=append(reasons,"HIGH_VALUE_SUBJECT") }
    action:="rotate_classical_key"
    if o.PQAvailable { action="adopt_hybrid_authorization" } else if o.Chain=="bitcoin" { action="rotate_to_unexposed_script" }
    return model.Assessment{urgency,action,reasons}
}
