// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract TimeOracle {
    uint256 public currentTime;
    uint256 public currentAssetPrice;
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
    function update(uint256 _newTime, uint256 _currentPrice) public onlyDeployer {
        require(_newTime > currentTime, "New time must be in the future");
        currentTime = _newTime;
        currentAssetPrice = _currentPrice;
        emit TimeUpdated(_newTime);
    }

    // Get the latest oracle time
    function oracleUpdate(uint256 _newTime, uint _currentPrice) public returns (uint256, uint256) {
        update(_newTime, _currentPrice);
        return (currentTime, currentAssetPrice);
    }
}

