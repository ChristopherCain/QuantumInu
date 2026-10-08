use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct CapabilitySet {
    pub wots_k256: bool,
    pub ml_dsa: bool,
    pub slh_dsa: bool,
    pub hybrid_auth: bool,
    pub account_rotation: bool,
}

impl CapabilitySet {
    pub fn intersection(&self, other: &Self) -> Self {
        Self {
            wots_k256: self.wots_k256 && other.wots_k256,
            ml_dsa: self.ml_dsa && other.ml_dsa,
            slh_dsa: self.slh_dsa && other.slh_dsa,
            hybrid_auth: self.hybrid_auth && other.hybrid_auth,
            account_rotation: self.account_rotation && other.account_rotation,
        }
    }

    pub fn any_pq(&self) -> bool {
        self.wots_k256 || self.ml_dsa || self.slh_dsa
    }
}
