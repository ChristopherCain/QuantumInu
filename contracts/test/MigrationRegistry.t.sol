// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;
import "../src/MigrationRegistry.sol";
contract MigrationRegistryTest {
 function testSet() public {
   MigrationRegistry r=new MigrationRegistry();
   r.setMigrationState(MigrationRegistry.Status.Hybrid,keccak256("ML-DSA-65+ECDSA"),1);
   MigrationRegistry.Record memory x=r.migrationState(address(this));
   require(x.epoch==1,"epoch");
 }
}
