// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;

contract CapabilityRegistry {
    struct Capabilities {
        bool wotsK256;
        bool mlDsa;
        bool slhDsa;
        bool hybridAuth;
        bool accountRotation;
    }

    mapping(address => Capabilities) private _caps;
    event CapabilitiesUpdated(address indexed subject, Capabilities capabilities);

    function set(address subject, Capabilities calldata caps) external {
        _caps[subject] = caps;
        emit CapabilitiesUpdated(subject, caps);
    }

    function get(address subject) external view returns (Capabilities memory) {
        return _caps[subject];
    }
}
