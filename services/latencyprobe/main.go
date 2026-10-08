package main
import ("encoding/json";"flag";"fmt";"net/http";"sort";"time")
type Result struct{URL string `json:"url"`; Samples int `json:"samples"`; P50MS float64 `json:"p50_ms"`; P95MS float64 `json:"p95_ms"`; Failures int `json:"failures"`}
func percentile(xs []float64,p float64) float64 {if len(xs)==0{return 0};sort.Float64s(xs);i:=int(float64(len(xs)-1)*p);return xs[i]}
func main(){u:=flag.String("url","http://127.0.0.1:8000/health","endpoint");n:=flag.Int("n",20,"samples");flag.Parse();xs:=[]float64{};fail:=0;c:=http.Client{Timeout:2*time.Second};for i:=0;i<*n;i++{t:=time.Now();r,e:=c.Get(*u);if e!=nil{fail++;continue};r.Body.Close();xs=append(xs,float64(time.Since(t).Microseconds())/1000)};b,_:=json.MarshalIndent(Result{*u,*n,percentile(xs,.5),percentile(xs,.95),fail},"","  ");fmt.Println(string(b))}
