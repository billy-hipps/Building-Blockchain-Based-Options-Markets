// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

// ======== Time Oracle Contract ========
contract TimeOracle {
    uint256 public currentTime;           // Latest updated time (typically a UNIX timestamp)
    uint256 public currentAssetPrice;     // Latest price of the tracked asset
    address public immutable deployer;    // Authorized updater address (e.g., backend oracle)

    // Event emitted whenever time is updated
    event TimeUpdated(uint256 newTime);

    // ======== Constructor ========
    /**
     * Initializes the contract with an authorized updater (deployer).
     * @param _updater The address allowed to update oracle values.
     */
    constructor(address _updater) {
        require(_updater != address(0), "Invalid updater address");
        deployer = _updater;
    }

    // ======== Modifiers ========

    // Restricts function access to the deployer only
    modifier onlyDeployer() {
        require(msg.sender == deployer, "Not authorized");
        _;
    }

    // ======== Core Oracle Update Logic ========

    /**
     * Updates the oracle with a new time and asset price.
     * Only callable by the deployer (off-chain oracle).
     * @param _newTime The new UNIX timestamp (must be in the future).
     * @param _currentPrice The current price of the asset.
     */
    function update(uint256 _newTime, uint256 _currentPrice) public onlyDeployer {
        require(_newTime > currentTime, "New time must be in the future");
        currentTime = _newTime;
        currentAssetPrice = _currentPrice;
        emit TimeUpdated(_newTime);
    }

    /**
     * External interface to trigger update and return new values.
     * Can be used for confirmation or chained calls.
     * @param _newTime The new timestamp to set.
     * @param _currentPrice The asset price to set.
     * @return (updated time, updated price)
     */
    function oracleUpdate(uint256 _newTime, uint256 _currentPrice) public returns (uint256, uint256) {
        update(_newTime, _currentPrice);
        return (currentTime, currentAssetPrice);
    }
}
