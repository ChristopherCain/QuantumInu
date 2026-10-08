// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;

import {IQuantumAuthorizer} from "./interfaces/IQuantumAuthorizer.sol";

contract HybridAuthorizer {
    IQuantumAuthorizer public immutable pq;

    constructor(IQuantumAuthorizer pq_) { pq = pq_; }

    function verify(
        bytes32 digest,
        bytes calldata pqProof,
        address expectedSigner,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external view returns (bool) {
        if (!pq.verify(digest, pqProof)) return false;
        address recovered = ecrecover(digest, v, r, s);
        return recovered != address(0) && recovered == expectedSigner;
    }
}
