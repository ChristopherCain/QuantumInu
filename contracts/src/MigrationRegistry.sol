// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;

contract MigrationRegistry {
    enum State { Unknown, Monitor, Prepare, Migrating, Protected }
    mapping(address => State) public stateOf;
    mapping(address => bytes32) public evidenceOf;
    event MigrationStateChanged(address indexed subject, State state, bytes32 evidence);

    function setState(address subject, State state, bytes32 evidence) external {
        stateOf[subject] = state;
        evidenceOf[subject] = evidence;
        emit MigrationStateChanged(subject, state, evidence);
    }
}
