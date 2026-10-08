package main
import (
  "encoding/json"
  "fmt"
  "os"
  "quantuminu/services/shared/model"
  "quantuminu/services/shared/policy"
)
func main() {
  var o model.Observation
  if err:=json.NewDecoder(os.Stdin).Decode(&o); err!=nil { panic(err) }
  a:=policy.Evaluate(o)
  b,_:=json.MarshalIndent(a,"","  ")
  fmt.Println(string(b))
}
