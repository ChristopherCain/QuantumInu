// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;

contract KeyRotationManager {
    struct KeyState { bytes32 current; uint64 nonce; }
    mapping(address => KeyState) public stateOf;

    event Rotated(address indexed subject, bytes32 previous, bytes32 next, uint64 nonce);

    function initialize(bytes32 initialKey) external {
        require(stateOf[msg.sender].current == bytes32(0), "ALREADY_INITIALIZED");
        require(initialKey != bytes32(0), "ZERO_KEY");
        stateOf[msg.sender] = KeyState(initialKey, 0);
    }

    function rotate(bytes32 expectedCurrent, bytes32 next) external {
        KeyState storage s = stateOf[msg.sender];
        require(s.current == expectedCurrent, "STALE_KEY");
        require(next != bytes32(0) && next != expectedCurrent, "INVALID_NEXT_KEY");
        bytes32 previous = s.current;
        s.current = next;
        unchecked { s.nonce += 1; }
        emit Rotated(msg.sender, previous, next, s.nonce);
    }
}
