package model
type Observation struct {
    Chain string `json:"chain"`
    Subject string `json:"subject"`
    PublicKeyExposed bool `json:"public_key_exposed"`
    SignatureFamily string `json:"signature_family"`
    HighValue bool `json:"high_value"`
    HighFrequency bool `json:"high_frequency"`
    PQAvailable bool `json:"pq_authorization_available"`
}
type Assessment struct { Urgency string `json:"urgency"`; Action string `json:"action"`; Reasons []string `json:"reasons"` }
