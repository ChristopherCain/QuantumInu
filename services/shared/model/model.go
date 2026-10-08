package model

type SignatureFamily string
const (
	Secp256k1 SignatureFamily = "secp256k1"
	Ed25519   SignatureFamily = "ed25519"
	WotsK256  SignatureFamily = "wots-k256"
	MlDsa     SignatureFamily = "ml-dsa"
	SlhDsa    SignatureFamily = "slh-dsa"
)

type Observation struct {
	Subject string `json:"subject"`
	Chain string `json:"chain"`
	PublicKeyExposed bool `json:"public_key_exposed"`
	ExposureAgeBlocks uint64 `json:"exposure_age_blocks"`
	ValueAtRiskUSD uint64 `json:"value_at_risk_usd"`
	SignaturesPerDay uint32 `json:"signatures_per_day"`
	KeyReuseDetected bool `json:"key_reuse_detected"`
	ReplaySurfacePresent bool `json:"replay_surface_present"`
	SignatureFamily SignatureFamily `json:"signature_family"`
	PQAuthorizationAvailable bool `json:"pq_authorization_available"`
	HybridAuthorizationAvailable bool `json:"hybrid_authorization_available"`
	ChainUpgradeLatencyDays uint32 `json:"chain_upgrade_latency_days"`
}

type Breakdown struct {
	ExposureAge int `json:"exposure_age"`
	ValueAtRisk int `json:"value_at_risk"`
	Frequency int `json:"frequency"`
	KeyReuse int `json:"key_reuse"`
	LegacySignature int `json:"legacy_signature"`
	ChainLatency int `json:"chain_latency"`
	ReplaySurface int `json:"replay_surface"`
	PQCredit int `json:"pq_credit"`
	HybridCredit int `json:"hybrid_credit"`
}

type Assessment struct {
	Score int `json:"score"`
	Urgency string `json:"urgency"`
	Action string `json:"action"`
	Reasons []string `json:"reasons"`
	Breakdown Breakdown `json:"breakdown"`
}
