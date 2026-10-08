// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;

contract QuantumInuAccount {
    bytes32 public keyHash;
    uint256 public nonce;

    error BadAuthorization();
    error InvalidNextKey();
    error CallFailed(bytes data);

    event Executed(uint256 indexed nonce, address indexed target, uint256 value, bytes32 nextKeyHash);

    constructor(bytes32 initialKeyHash) {
        require(initialKeyHash != bytes32(0), "ZERO_KEY");
        keyHash = initialKeyHash;
    }

    function operationDigest(
        address target,
        uint256 value,
        bytes calldata data,
        bytes32 nextKeyHash
    ) public view returns (bytes32) {
        return keccak256(abi.encode(
            block.chainid,
            address(this),
            nonce,
            target,
            value,
            keccak256(data),
            nextKeyHash
        ));
    }

    // Research placeholder: caller provides a verified authorization commitment produced
    // by an external verifier module. This keeps account state transition logic isolated.
    function execute(
        address target,
        uint256 value,
        bytes calldata data,
        bytes32 nextKeyHash,
        bytes32 authorizationCommitment
    ) external payable returns (bytes memory result) {
        if (nextKeyHash == bytes32(0) || nextKeyHash == keyHash) revert InvalidNextKey();
        bytes32 digest = operationDigest(target, value, data, nextKeyHash);
        if (authorizationCommitment != keccak256(abi.encodePacked(keyHash, digest))) {
            revert BadAuthorization();
        }

        uint256 current = nonce;
        keyHash = nextKeyHash;
        nonce = current + 1;

        (bool ok, bytes memory out) = target.call{value:value}(data);
        if (!ok) revert CallFailed(out);

        emit Executed(current, target, value, nextKeyHash);
        return out;
    }

    receive() external payable {}
}
