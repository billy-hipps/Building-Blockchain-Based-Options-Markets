// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.28;

import "./BinaryOption.sol";

// ======== Interface for BinaryOption ========
interface IBinaryOption {
    function buy(address payable _contractBuyer) external;
}

contract CreateBO {
    // ======== State Variables ========
    address payable public creator;
    uint256 public balance;
    bool public isDeployed;
    bool public isBought;

    // ======== BO Variables ========
    uint256 public strikePrice;
    uint256 public strikeDate;
    uint256 public payout;
    uint256 public expiryPrice;
    bool public position;
    uint256 public contractPrice;
    address payable public buyer;
    address public binaryOptionAddress;

    // ======== Events ========
    event Deposited(address indexed sender, uint256 amount);
    event Created(address indexed creator, address contractAddress);
    event Bought(address indexed buyer, address indexed contractAddress);

    // ======== Constructor ========
    constructor(
        uint256 _strikePrice,
        uint256 _strikeDate,
        uint256 _payout,
        uint256 _expiryPrice,
        bool _position,
        uint256 _contractPrice
    ) payable {
        creator = payable(msg.sender);
        strikePrice = _strikePrice;
        strikeDate = _strikeDate;
        payout = _payout;  // Ensure payout is in Wei
        expiryPrice = _expiryPrice;
        position = _position;
        contractPrice = _contractPrice;
        isDeployed = false;
        isBought = false;
    }

    // ======== View Functions ========
    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }

    function getPayout() public view returns (uint256) {
        return payout;
    }

    function getBuyer() public view returns (address) {
        return buyer;
    }

    function get_isBought() public view returns (bool) {
        return isBought;
    }

    // ======== ETH Deposit ========
    receive() external payable {
        emit Deposited(msg.sender, msg.value);

        // Always get the actual balance of the contract
        balance = address(this).balance;
    }

    // ======== Deploy Binary Option ========
    function deployBinaryOption() public returns (address) {
        //require(balance >= payout, "Insufficient balance for payout");

        binaryOptionAddress = _deployBinaryOption();

        require(binaryOptionAddress != address(0), "BinaryOption contract not deployed");
        (bool success, ) = payable(binaryOptionAddress).call{value: address(this).balance}("");
        require(success, "Transfer to BinaryOption failed");

        emit Created(creator, address(this));

        return binaryOptionAddress;
    }

    function _deployBinaryOption() internal returns (address payable) {
        BinaryOption bo = new BinaryOption(
            strikePrice,
            strikeDate,
            payout,
            expiryPrice,
            position,
            contractPrice,
            creator
        );
        return payable(address(bo));
    }

    // ======== Buy Binary Option Contract ========
    function buyContract() external payable {
        require(binaryOptionAddress != address(0), "BinaryOption not deployed");
        require(!isDeployed, "BinaryOption already bought!");
        require(msg.sender != creator, "Creator cannot buy the contract!");
        require(msg.value >= contractPrice, "Incorrect ETH amount sent!");

        // Call `buy()` on the deployed BinaryOption contract
        IBinaryOption(binaryOptionAddress).buy(payable(msg.sender));

        // Transfer the received ETH to the creator
        (bool success, ) = creator.call{value: msg.value}("");
        require(success, "Transfer to creator failed");

        isBought = true;
        buyer = payable(msg.sender);

        emit Bought(msg.sender, address(this));
    }
    
}
