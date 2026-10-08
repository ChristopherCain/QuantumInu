from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class CapabilitySet:
    wots_k256: bool=False
    ml_dsa: bool=False
    slh_dsa: bool=False
    hybrid_auth: bool=False
    account_rotation: bool=False

    def intersect(self, other:"CapabilitySet")->"CapabilitySet":
        return CapabilitySet(
            self.wots_k256 and other.wots_k256,
            self.ml_dsa and other.ml_dsa,
            self.slh_dsa and other.slh_dsa,
            self.hybrid_auth and other.hybrid_auth,
            self.account_rotation and other.account_rotation,
        )
