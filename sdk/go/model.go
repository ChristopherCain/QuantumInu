package qinusdk
type CapabilitySet struct{WotsK256, MlDsa, SlhDsa, HybridAuth, AccountRotation bool}
func (a CapabilitySet) Intersect(b CapabilitySet) CapabilitySet{
 return CapabilitySet{a.WotsK256&&b.WotsK256,a.MlDsa&&b.MlDsa,a.SlhDsa&&b.SlhDsa,a.HybridAuth&&b.HybridAuth,a.AccountRotation&&b.AccountRotation}
}
