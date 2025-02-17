// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.28;


contract BinaryOption {
    // ======== Variables ========

    // ======== State Variables ========
    bool public isBought; // true = bought, false = not bought
    uint256 public contractBalance;
    address payable public contractCreator;
    address payable public contractBuyer;
    uint8 public decimals;

    // ======== Contract Variables ========
    string public symbol;
    string public name;
    uint256 public _totalSupply;
    uint256 public strikePrice;
    uint256 public strikeDate;
    uint256 public payout;
    uint256 public expiryPrice;
    bool public position; // true = long, false = short
    uint256 public contractPrice;

    // ======== Constructor ========
    constructor(
        uint256 _strikePrice, 
        uint256 _strikeDate, 
        uint256 _payout, 
        uint256 _expiryPrice,
        bool _position, 
        uint256 _contractPrice, 
        address payable _contractCreator

    ) payable {
        // Default state variables
        contractCreator = _contractCreator;
        contractBuyer = payable(address(0));
        isBought = false;

        // Hard coded (for now) 
        symbol = "BO";
        name = "Binary Option";
        decimals = 0;
        _totalSupply = 1; // Only one contract can be created at a time

        // Parameterised 
        strikePrice = _strikePrice;
        strikeDate = block.timestamp + _strikeDate; // Assuming `_strikeDate` is a duration in seconds
        payout = _payout;
        expiryPrice = _expiryPrice;
        position = _position;
        contractPrice = _contractPrice;

    }

    function get_contractBuyer() public view returns (address) {
        return contractBuyer;
    }

    function get_isBought() public view returns (bool) {
        return isBought;
    }

    // Function to receive ETH
    receive() external payable {
    }

    // Public function to check contract balance
    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }

    // Buy the contract
    function buy(address payable _contractBuyer) external {
        contractBuyer = _contractBuyer;
        isBought = true;
    }

}
