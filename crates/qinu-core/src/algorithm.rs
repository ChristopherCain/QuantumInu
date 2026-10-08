#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum AlgorithmFamily { MlKem, MlDsa, SlhDsa, EcdsaSecp256k1, Ed25519 }

impl AlgorithmFamily {
    pub fn is_post_quantum(self) -> bool {
        matches!(self, Self::MlKem | Self::MlDsa | Self::SlhDsa)
    }
}
