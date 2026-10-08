package main
import ("encoding/json";"os";"quantum-inu/threat-sentinel/internal/analyzer";"quantum-inu/threat-sentinel/internal/model")
func main(){ var o model.Observation; if json.NewDecoder(os.Stdin).Decode(&o)!=nil { os.Exit(2) }; json.NewEncoder(os.Stdout).Encode(analyzer.Assess(o)) }
