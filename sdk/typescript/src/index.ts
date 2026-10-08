export type Observation={chain:string;subject:string;publicKeyExposed:boolean;signatureFamily:string;highValue?:boolean;highFrequency?:boolean;pqAuthorizationAvailable?:boolean};
export type Assessment={urgency:"low"|"medium"|"high"|"critical";action:string;reasons:string[]};
export function planMigration(o:Observation):Assessment{
 if(!o.publicKeyExposed)return{urgency:"low",action:"monitor",reasons:["PUBLIC_KEY_NOT_EXPOSED"]};
 const reasons=["PUBLIC_KEY_EXPOSED"]; let urgency:Assessment["urgency"]="medium";
 if(o.highFrequency){urgency="high";reasons.push("HIGH_SPEND_FREQUENCY")}
 if(o.highValue){urgency="critical";reasons.push("HIGH_VALUE_SUBJECT")}
 const action=o.pqAuthorizationAvailable?"adopt_hybrid_authorization":o.chain.toLowerCase()==="bitcoin"?"rotate_to_unexposed_script":"rotate_classical_key";
 return{urgency,action,reasons};
}
