// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;


contract BinaryOption {

    // ======== State Variables ========
    address payable private deployerAddress;
    address payable private contractCreator;
    address payable private contractBuyer;
    bool private isBought; // true = bought, false = not bought
    bool private isExpired; // true = expired, false = not expired

    // ======== BO Parameters ========
    string private symbol;
    string private name;

    uint256 private strikePrice;
    uint256 private strikeDate;
    uint256 private payout;
    bool private position; // true = long, false = short

    uint256 private expiryPrice;
    uint256 private contractPrice;

    // ======== Constructor ========
    constructor(
        uint256 _strikePrice, 
        uint256 _strikeDate, 
        uint256 _payout, 
        bool _position,

        uint256 _expiryPrice,
        uint256 _contractPrice,

        address payable _contractCreator,
        address payable _deployerAddress

    ) payable {
        // BO Parameters
        strikePrice = _strikePrice;
        strikeDate = block.timestamp + _strikeDate;
        payout = _payout;
        position = _position;

        expiryPrice = _expiryPrice;
        contractPrice = _contractPrice;

        deployerAddress = _deployerAddress;
        contractCreator = _contractCreator;

        // Default state vaiables
        contractBuyer = payable(address(0));
        isBought = false;
        isExpired = false;

        // Hard coded (for now) 
        symbol = "BO";
        name = "Binary Option";

    }

    modifier onlyDeployer() {
        require(msg.sender == deployerAddress, "BO: Not authorized");
        _;
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

    function buy(address payable _contractBuyer) external onlyDeployer {
        require (!isBought, "BO: Contract has already been bought.");
        _buy(_contractBuyer);
    }

    // Buy the contract
    function _buy(address payable _contractBuyer) private {
        contractBuyer = _contractBuyer;
        isBought = true;
    }

    function terminate() external onlyDeployer {
        require (!isExpired, "BO: Contract has already expired.");
        _terminate();
    }

    function _terminate() private {
        if (!isBought) {
            // Refund the contract creator
            contractCreator.transfer(address(this).balance);
        } else {
            if (position == true) {
                if (expiryPrice >= strikePrice) {
                    // Pay out the contract buyer
                    contractBuyer.transfer(address(this).balance);
                } else {
                    // Pay out the contract creator
                    contractCreator.transfer(address(this).balance);
                }
            } else {
                if (expiryPrice <= strikePrice) {
                    // Pay out the contract buyer
                    contractBuyer.transfer(address(this).balance);
                } else {
                    // Pay out the contract creator
                    contractCreator.transfer(address(this).balance);
                }
            }
        } 
        isExpired = true;
    }

}
