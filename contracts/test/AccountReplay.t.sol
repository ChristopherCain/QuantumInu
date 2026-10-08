// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;
import {QuantumInuAccount} from "../src/QuantumInuAccount.sol";
contract Sink { uint256 public calls; function ping() external { calls++; } }
contract AccountReplayTest {
    function testDigestChangesWithNonce() public {
        bytes32 k0=keccak256("k0"); QuantumInuAccount a=new QuantumInuAccount(k0);
        Sink s=new Sink(); bytes memory data=abi.encodeCall(Sink.ping,());
        bytes32 k1=keccak256("k1");
        bytes32 d0=a.operationDigest(address(s),0,data,k1);
        bytes32 auth=keccak256(abi.encodePacked(k0,d0));
        a.execute(address(s),0,data,k1,auth);
        bytes32 d1=a.operationDigest(address(s),0,data,keccak256("k2"));
        require(d0!=d1);
    }
}
