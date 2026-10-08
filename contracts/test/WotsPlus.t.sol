// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;
import {WotsPlus} from "../src/WotsPlus.sol";
contract WotsHarness {
    function chain(bytes32 x,uint256 n) external pure returns(bytes32){return WotsPlus.chain(x,n);}
}
contract WotsPlusTest {
    function testChainProgresses() public {
        WotsHarness h=new WotsHarness();
        bytes32 x=keccak256("x");
        require(h.chain(x,0)==x);
        require(h.chain(x,1)==keccak256(abi.encodePacked(x)));
    }
}
