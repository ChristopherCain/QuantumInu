// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;

contract EvidenceRegistry {
    mapping(bytes32 => uint64) public firstSeenBlock;
    mapping(bytes32 => address) public submitter;

    event EvidenceRecorded(bytes32 indexed digest, address indexed submitter, uint64 blockNumber);

    function record(bytes32 digest) external {
        require(digest != bytes32(0), "ZERO_DIGEST");
        if (firstSeenBlock[digest] == 0) {
            firstSeenBlock[digest] = uint64(block.number);
            submitter[digest] = msg.sender;
            emit EvidenceRecorded(digest, msg.sender, uint64(block.number));
        }
    }

    function exists(bytes32 digest) external view returns (bool) {
        return firstSeenBlock[digest] != 0;
    }
}
