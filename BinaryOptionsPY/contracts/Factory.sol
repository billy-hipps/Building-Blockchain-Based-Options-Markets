// SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.23;

import "./CreateBO.sol";

interface ICreateBO {
    function deployBinaryOption() external;
}

contract Factory {
    address[] public createBOarray;

    event ContractDeployed(address indexed createBO);

    function CreateAndDeploy(
        bytes32 _ticker,
        uint256 _strikePrice, 
        uint256 _strikeDate, 
        uint256 _payout, 
        bool _position,
        uint256 _contractPrice
    ) public payable {
        address payable creator = payable(msg.sender);

        require(msg.value >= _payout, "Factory: Payout amount is not equal to the amount sent");

        // Create the CreateBO contract
        CreateBO createBO = new CreateBO(
            address(this),
            _ticker,
            _strikePrice, 
            _strikeDate, 
            _payout, 
            _position,
            _contractPrice, 
            creator
        );

        address payable createBOAddress = payable(address(createBO));

        // Store in array
        createBOarray.push(createBOAddress);

        // Transfer ETH to CreateBO
        (bool success, ) = createBOAddress.call{value: msg.value}("");
        require(success, "Transfer failed.");

        // Deploy Binary Option contract via CreateBO
        ICreateBO(createBOAddress).deployBinaryOption();

        // Emit event
        emit ContractDeployed(createBOAddress);
    }

    function getDeployedContracts() public view returns (address[] memory) {
        return createBOarray;
    }
}
