// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;
import {KeyRotationManager} from "../src/KeyRotationManager.sol";
contract KeyRotationTest {
    function testRotation() public {
        KeyRotationManager r=new KeyRotationManager();
        bytes32 a=keccak256("a"); bytes32 b=keccak256("b");
        r.initialize(a); r.rotate(a,b);
        (bytes32 key,uint64 nonce)=r.stateOf(address(this));
        require(key==b && nonce==1);
    }
}
