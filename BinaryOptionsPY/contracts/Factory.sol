// SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.23;

import "./CreateBO.sol";  // Import CreateBO contract

// ======== Interface for CreateBO ========
interface ICreateBO {
    function deployBinaryOption() external;
}

// ======== Factory Contract ========
contract Factory {
    address[] public createBOarray;  // Stores all deployed CreateBO contract addresses

    // Event emitted when a new CreateBO contract is deployed
    event ContractDeployed(address indexed createBO);

    // ======== Deploy CreateBO and BinaryOption ========
    /**
     * Deploys a CreateBO contract and triggers deployment of a BinaryOption contract through it.
     *
     * @param _ticker The asset identifier
     * @param _strikePrice The target price for settlement
     * @param _strikeDate The time duration until expiration (in seconds)
     * @param _payout The amount to be paid out if condition is met
     * @param _position true = long, false = short
     * @param _contractPrice The price for a user to buy the contract
     */
    function CreateAndDeploy(
        bytes32 _ticker,
        uint256 _strikePrice, 
        uint256 _strikeDate, 
        uint256 _payout, 
        bool _position,
        uint256 _contractPrice
    ) public payable {
        address payable creator = payable(msg.sender);  // Save caller as contract creator

        require(msg.value >= _payout, "Factory: Payout amount is not equal to the amount sent");

        // Deploy a new CreateBO contract
        CreateBO createBO = new CreateBO(
            address(this),      // Factory address
            _ticker,
            _strikePrice, 
            _strikeDate, 
            _payout, 
            _position,
            _contractPrice, 
            creator
        );

        address payable createBOAddress = payable(address(createBO));  // Cast to payable

        createBOarray.push(createBOAddress);  // Store the new contract address

        // Forward ETH to the CreateBO contract
        (bool success, ) = createBOAddress.call{value: msg.value}("");
        require(success, "Transfer failed.");

        // Trigger deployment of BinaryOption inside the CreateBO
        ICreateBO(createBOAddress).deployBinaryOption();

        emit ContractDeployed(createBOAddress);  // Emit event for off-chain tracking
    }

    // ======== View All Deployed Contracts ========
    /**
     * Returns all CreateBO contracts deployed by this factory.
     */
    function getDeployedContracts() public view returns (address[] memory) {
        return createBOarray;
    }
}
