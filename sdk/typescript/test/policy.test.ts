import test from "node:test";
import assert from "node:assert/strict";
import {evaluate,Observation} from "../src/index.js";
const base:Observation={subject:"x",chain:"ethereum",publicKeyExposed:false,exposureAgeBlocks:0,valueAtRiskUsd:0,signaturesPerDay:1,keyReuseDetected:false,replaySurfacePresent:false,signatureFamily:"secp256k1",pqAuthorizationAvailable:false,hybridAuthorizationAvailable:false,chainUpgradeLatencyDays:30};
test("low",()=>assert.equal(evaluate(base).urgency,"low"));
test("pq credit",()=>assert.ok(evaluate({...base,publicKeyExposed:true,pqAuthorizationAvailable:true}).score<evaluate({...base,publicKeyExposed:true}).score));
