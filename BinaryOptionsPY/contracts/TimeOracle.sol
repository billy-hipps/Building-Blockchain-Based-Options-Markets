// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TimeOracle {
    uint256 public currentTime;
    address public deployer;
    event TimeUpdated(uint256 newTime);

    constructor(address _updater) {
        deployer = _updater;
    }

    modifier onlyDeployer() {
        require(msg.sender == deployer, "Not authorized");
        _;
    }

    // Off-chain oracle updates the time
    function updateTime(uint256 _newTime) public onlyDeployer {
        require(_newTime > currentTime, "New time must be in the future");
        currentTime = _newTime;
        emit TimeUpdated(_newTime);
    }

    // Get the latest oracle time
    function getTime(uint256 _newTime) public returns (uint256) {
        updateTime(_newTime);
        return currentTime;
    }
}

