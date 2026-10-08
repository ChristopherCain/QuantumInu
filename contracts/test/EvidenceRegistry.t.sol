// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;
import {EvidenceRegistry} from "../src/EvidenceRegistry.sol";
contract EvidenceRegistryTest {
    function testEvidenceRecordedOnce() public {
        EvidenceRegistry r = new EvidenceRegistry();
        bytes32 d=keccak256("evidence");
        r.record(d); require(r.exists(d));
        uint64 first=r.firstSeenBlock(d); r.record(d); require(r.firstSeenBlock(d)==first);
    }
}
