package qinusdk
import "testing"
func TestIntersect(t *testing.T){a:=CapabilitySet{WotsK256:true,MlDsa:true};b:=CapabilitySet{WotsK256:true};x:=a.Intersect(b);if !x.WotsK256||x.MlDsa{t.Fatal(x)}}
