//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.20;

import "./CreateBO.sol";

interface ICreateBO {
    function deployBinaryOption() external;
}

contract Factory {
    address[] public createBOarray;
    address payable public createBOAddress;
    address payable public creator;


    function CreateAndDeploy(bytes32 _ticker,
                            uint256 _strikePrice, 
                            uint256 _strikeDate, 
                            uint256 _payout, 
                            bool _position ,
                            uint256 _contractPrice) public payable {

        creator = payable(msg.sender);
        
        // Function call must include transefer of payout amount
        require(msg.value >= _payout, "Factory: Payout amount is not equal to the amount sent");

        // Payout ammount is sufficient, create CreateBO contract
        CreateBO createBO = new CreateBO(address(this),
                            _ticker,
                            _strikePrice, 
                            _strikeDate, 
                            _payout, 
                            _position ,
                            _contractPrice, 
                            creator);

        // Store the CreateBO contract in an array
        createBOAddress = payable(address(createBO));
        createBOarray.push(createBOAddress);

        // Transfer the payout amount to the CreateBO contract
        (bool success, ) = payable(createBOAddress).call{value: msg.value}("");
        require(success, "Transfer failed.");

        // Deploy the Binary Option contract
        ICreateBO(createBOAddress).deployBinaryOption();

    }

    function detDeployedContracts() public view returns (address[] memory) {
        return createBOarray;
    }


}
