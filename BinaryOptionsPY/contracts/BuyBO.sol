// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.28;

// Interface for the Binary Option contract
interface IBinaryOption {
    function isBought() external view returns (bool);
    function buyContract(address payable buyer, address payable contractOwner, uint256 contractPrice) external payable;
}

contract Buy {

    // ======== Events ========
    event Bought(address indexed buyer, address indexed contractAddress);
    event Deposited(address indexed sender, uint256 amount);

    // ======== State Variables ========
    bool public isBought;  // true = bought, false = not bought 
    uint256 public contractPrice;
    address payable public buyer;
    address payable public contractOwner;
    address payable public contractAddress;

    constructor(
        address payable _buyer,
        address payable _contractOwner,
        address payable _contractAddress
    ) payable {
        // Assign input values
        buyer = _buyer;
        contractOwner = _contractOwner;
        contractAddress = _contractAddress;

        // Get the current state of `isBought` from the Binary Option contract
        isBought = IBinaryOption(contractAddress).isBought();

        // Set the contract price (ETH sent with transaction)
        contractPrice = msg.value;
    }


    // Function to receive ETH
    receive() external payable {
        emit Deposited(msg.sender, msg.value);
    }


    // Public function to check contract balance
    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }


    // Function to buy the contract
    function buyOption() public payable {
        require(!isBought, "Contract already bought!");
        require(msg.sender == buyer, "Only buyer can buy");
        require(msg.value == contractPrice, "Incorrect payment amount");

        // Call `buyContract()` on the Binary Option contract
        IBinaryOption(contractAddress).buyContract{value: msg.value}(buyer, contractOwner, contractPrice);

        // Mark as bought
        isBought = true;

        // Emit event
        emit Bought(buyer, contractAddress);

        // Desytroy the contract
        selfdestruct(contractOwner);
    }


    function setBuyer(address payable buyer, address payable contractOwner, uint256 contractPrice) public payable {
        // Contract purchase logic here
        require(!isBought, "Contract has already been bought");

    }

}
