// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;

library WotsPlus {
    uint256 internal constant W = 16;
    uint256 internal constant CHAINS = 67;

    function chain(bytes32 start, uint256 steps) internal pure returns (bytes32 x) {
        require(steps < W, "STEPS");
        x = start;
        for (uint256 i; i < steps; ++i) {
            x = keccak256(abi.encodePacked(x));
        }
    }

    function compress(bytes32[] memory endpoints) internal pure returns (bytes32) {
        require(endpoints.length == CHAINS, "CHAIN_COUNT");
        return keccak256(abi.encodePacked(endpoints));
    }
}
