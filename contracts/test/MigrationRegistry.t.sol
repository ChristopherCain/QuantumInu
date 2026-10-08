// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;
import {MigrationRegistry} from "../src/MigrationRegistry.sol";
contract MigrationRegistryTest {
    function testStateRoundTrip() public {
        MigrationRegistry r = new MigrationRegistry();
        r.setState(address(this), MigrationRegistry.State.Prepare, bytes32(uint256(7)));
        require(r.stateOf(address(this)) == MigrationRegistry.State.Prepare);
    }
}
