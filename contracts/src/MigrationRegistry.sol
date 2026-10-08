// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;
contract MigrationRegistry {
 enum Status{Unset,Classical,Hybrid,PostQuantumReady,Deprecated}
 struct Record{Status status;bytes32 algorithmId;uint64 epoch;uint64 updatedAt;}
 mapping(address=>Record) private records;
 event MigrationStateUpdated(address indexed account,Status status,bytes32 indexed algorithmId,uint64 epoch);
 function setMigrationState(Status status,bytes32 algorithmId,uint64 epoch) external {
   require(epoch>=records[msg.sender].epoch,"epoch regression");
   records[msg.sender]=Record(status,algorithmId,epoch,uint64(block.timestamp));
   emit MigrationStateUpdated(msg.sender,status,algorithmId,epoch);
 }
 function migrationState(address account) external view returns(Record memory){return records[account];}
}
