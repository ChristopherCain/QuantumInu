use qinu_core::*;

#[test]
fn exposed_bitcoin_key_rotates() {
    let o=Observation{chain:"bitcoin".into(),public_key_exposed:true,
        signature_family:AlgorithmFamily::EcdsaSecp256k1,high_value:false,
        high_frequency:true,pq_authorization_available:false};
    let d=evaluate(&o);
    assert_eq!(d.urgency,Urgency::High);
    assert_eq!(d.action,Action::RotateToUnexposedScript);
}
