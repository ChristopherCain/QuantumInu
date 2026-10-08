package policy

import "quantuminu/services/shared/model"

func Evaluate(o model.Observation) model.Assessment {
	reasons := []string{}
	b := model.Breakdown{}
	if o.PublicKeyExposed {
		reasons = append(reasons, "PUBLIC_KEY_EXPOSED")
		if o.ExposureAgeBlocks >= 100000 { b.ExposureAge = 14; reasons = append(reasons, "EXPOSURE_AGE_HIGH") } else { b.ExposureAge = 7 }
	} else {
		reasons = append(reasons, "PUBLIC_KEY_NOT_EXPOSED")
	}
	if o.ValueAtRiskUSD >= 1000000 { b.ValueAtRisk=22; reasons=append(reasons,"HIGH_VALUE_SUBJECT")
	} else if o.ValueAtRiskUSD >= 100000 { b.ValueAtRisk=12
	} else if o.ValueAtRiskUSD >= 10000 { b.ValueAtRisk=6 }
	if o.SignaturesPerDay >= 1000 { b.Frequency=16; reasons=append(reasons,"HIGH_SPEND_FREQUENCY")
	} else if o.SignaturesPerDay >= 100 { b.Frequency=8 }
	if o.KeyReuseDetected { b.KeyReuse=20; reasons=append(reasons,"KEY_REUSE_DETECTED") }
	if o.SignatureFamily==model.Secp256k1 || o.SignatureFamily==model.Ed25519 { b.LegacySignature=12; reasons=append(reasons,"LEGACY_SIGNATURE_ONLY") }
	if o.ChainUpgradeLatencyDays >= 365 { b.ChainLatency=8; reasons=append(reasons,"CHAIN_UPGRADE_LATENCY_HIGH") }
	if o.ReplaySurfacePresent { b.ReplaySurface=10; reasons=append(reasons,"REPLAY_SURFACE_PRESENT") }
	if o.PQAuthorizationAvailable { b.PQCredit=-14; reasons=append(reasons,"PQ_AUTHORIZATION_AVAILABLE") }
	if o.HybridAuthorizationAvailable { b.HybridCredit=-6; reasons=append(reasons,"HYBRID_AUTH_AVAILABLE") }
	score := b.ExposureAge+b.ValueAtRisk+b.Frequency+b.KeyReuse+b.LegacySignature+b.ChainLatency+b.ReplaySurface+b.PQCredit+b.HybridCredit
	if score < 0 { score=0 }; if score > 100 { score=100 }
	urgency, action := "low","monitor"
	if score >= 70 { urgency,action="critical","isolate-and-migrate"
	} else if score >= 45 { urgency,action="high","migrate"
	} else if score >= 20 { urgency,action="medium","prepare-migration" }
	return model.Assessment{Score:score,Urgency:urgency,Action:action,Reasons:reasons,Breakdown:b}
}
