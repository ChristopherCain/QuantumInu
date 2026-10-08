package main
import (
  "crypto/sha256"
  "encoding/hex"
  "encoding/json"
  "fmt"
  "os"
  "quantuminu/services/shared/model"
)
type Envelope struct {
  ObserverID string `json:"observer_id"`
  Sequence uint64 `json:"sequence"`
  Observation model.Observation `json:"observation"`
  Digest string `json:"digest"`
}
func main(){
  var o model.Observation
  if err:=json.NewDecoder(os.Stdin).Decode(&o);err!=nil{panic(err)}
  raw,_:=json.Marshal(o); d:=sha256.Sum256(append([]byte("QINU_OBSERVER_V1"),raw...))
  e:=Envelope{ObserverID:"local-observer",Sequence:1,Observation:o,Digest:hex.EncodeToString(d[:])}
  out,_:=json.MarshalIndent(e,"","  ");fmt.Println(string(out))
}
