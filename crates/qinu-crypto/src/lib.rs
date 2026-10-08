use serde::{Deserialize, Serialize};
use sha3::{Digest, Keccak256};

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
pub enum AlgorithmId {
    Secp256k1,
    Ed25519,
    WotsK256,
    MlDsa44,
    MlDsa65,
    MlDsa87,
    SlhDsaSha2_128s,
}

pub fn domain_hash(domain: &[u8], payload: &[u8]) -> [u8; 32] {
    let mut h = Keccak256::new();
    h.update(domain);
    h.update(payload);
    h.finalize().into()
}

pub const WOTS_W: usize = 16;
pub const WOTS_CHAINS: usize = 67;
pub const WOTS_SIGNATURE_BYTES: usize = 2144;
