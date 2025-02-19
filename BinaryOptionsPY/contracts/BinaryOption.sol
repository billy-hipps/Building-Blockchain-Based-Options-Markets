// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.28;


contract BinaryOption {
    // ======== Variables ========

    // ======== State Variables ========
    bool private isBought; // true = bought, false = not bought
    bool private isExpired; // true = expired, false = not expired
    address payable private contractCreator;
    address payable private deployerAddress;
    address payable private contractBuyer;
    uint256 private contractBalance;

    uint8 private decimals;

    // ======== Contract Variables ========
    string private symbol;
    string private name;
    uint256 private strikePrice;
    uint256 private strikeDate;
    uint256 private payout;
    uint256 private expiryPrice;
    bool private position; // true = long, false = short
    uint256 private contractPrice;

    uint256 private _totalSupply;

    // ======== Constructor ========
    constructor(
        uint256 _strikePrice, 
        uint256 _strikeDate, 
        uint256 _payout, 
        uint256 _expiryPrice,
        bool _position, 
        uint256 _contractPrice, 
        address payable _contractCreator,
        address payable _deployerAddress

    ) payable {
        // Default state variables
        deployerAddress = _deployerAddress;
        contractCreator = _contractCreator;
        contractBuyer = payable(address(0));
        isBought = false;
        isExpired = false;

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

        // Start the countdown to expiry
        


    }


    function get_isBought() public view returns (bool) {
        return isBought;
    }

    function get_strikeDate() public view returns (uint256) {
        return strikeDate;
    }

    function get_strikePrice() public view returns (uint256) {
        return strikePrice;
    }

    function get_payout() public view returns (uint256) {
        return payout;
    }

    function get_expiryPrice() public view returns (uint256) {
        return expiryPrice;
    }

    function get_owner() public view returns (address) {
        return contractCreator;
    }

    function get_contractBuyer() public view returns (address payable) {
        return contractBuyer;
    }

    // Function to receive ETH
    receive() external payable {
    }

    // Public function to check contract balance
    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }

    function getStatus() external view returns (bool, bool, address, uint256) {
        return (isBought, isExpired, contractBuyer, address(this).balance);
    }

    function buy(address payable _contractBuyer) external {
        require (msg.sender == deployerAddress, "You do not have permission to call this function.");
        require (!isBought, "Contract has already been bought.");
        _buy(_contractBuyer);
    }

    // Buy the contract
    function _buy(address payable _contractBuyer) private {
        contractBuyer = _contractBuyer;
        isBought = true;
    }

    // Function to terminate the contract
    function terminate() private {
        isBought = get_isBought();
        strikeDate = get_strikeDate();
        strikePrice = get_strikePrice();
        payout = get_payout();
        expiryPrice = get_expiryPrice();
        contractBuyer = get_contractBuyer();

        contractBalance = address(this).balance;

        
    }

}
