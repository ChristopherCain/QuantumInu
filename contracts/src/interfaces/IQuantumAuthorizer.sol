// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;

interface IQuantumAuthorizer {
    function verify(bytes32 digest, bytes calldata proof) external view returns (bool);
}
