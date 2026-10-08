use qinu_core::CapabilitySet;

#[test]
fn intersection_is_conservative() {
    let a = CapabilitySet { wots_k256: true, ml_dsa: true, slh_dsa: false, hybrid_auth: true, account_rotation: true };
    let b = CapabilitySet { wots_k256: true, ml_dsa: false, slh_dsa: true, hybrid_auth: true, account_rotation: false };
    let x = a.intersection(&b);
    assert!(x.wots_k256);
    assert!(!x.ml_dsa);
    assert!(!x.slh_dsa);
    assert!(x.hybrid_auth);
    assert!(!x.account_rotation);
}
