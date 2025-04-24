// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.23;

contract BinaryOption {

    // ======== State Variables ========
    address payable public immutable deployerAddress;
    address payable public immutable contractCreator;
    address payable private contractBuyer;
    bool private isBought; // true = bought, false = not bought
    bool private isExpired; // true = expired, false = not expired

    // ======== BO Parameters ========
    bytes32 public immutable ticker;
    string public constant symbol = "BO";
    string public constant name = "Binary Option";

    uint256 public immutable strikePrice;
    uint256 public immutable strikeDate;
    uint256 public immutable payout;
    bool public immutable position; // true = long, false = short

    uint256 private expiryPrice;
    uint256 public immutable contractPrice;

    // ======== Events ========
    event Bought(address indexed buyer);
    event Terminated(uint256 expiryPrice, address recipient);
    event PriceUpdate(uint256 newPrice);

    // ======== Constructor ========
    constructor(
        bytes32 _ticker,
        uint256 _strikePrice, 
        uint256 _strikeDate, 
        uint256 _payout, 
        bool _position,
        uint256 _contractPrice,
        address payable _contractCreator,
        address payable _deployerAddress
    ) payable {
        require(_contractCreator != address(0), "BO: Invalid contract creator address");
        require(_deployerAddress != address(0), "BO: Invalid deployer address");

        strikePrice = _strikePrice;
        strikeDate = block.timestamp + _strikeDate;
        payout = _payout;
        position = _position;
        contractPrice = _contractPrice;
        deployerAddress = _deployerAddress;
        contractCreator = _contractCreator;

        contractBuyer = payable(address(0));
        isBought = false;
        isExpired = false;
        ticker = _ticker;
    }

    modifier onlyDeployer() {
        require(msg.sender == deployerAddress, "BO: Not authorized");
        _;
    }

    modifier onlyThis() {
        require(msg.sender == address(this), "BO: Not authorized");
        _;
    }

    // Function to receive ETH
    receive() external payable {}

    // Public function to check contract balance
    function getBalance() public view onlyDeployer returns (uint256) {
        return address(this).balance;
    }

    function getStatus() external view onlyDeployer returns (bool, bool, address, uint256) {
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
        emit Bought(_contractBuyer);
    }

    function terminate(uint256 _newPrice) external onlyDeployer {
        require (!isExpired, "BO: Contract has already expired.");
        expiryPrice = _newPrice;
        emit PriceUpdate(_newPrice);
        _terminate();
    }

    function _terminate() private {
        address payable recipient;

        if (!isBought) {
            recipient = contractCreator;
        } else {
            if (position == true) {
                recipient = (expiryPrice >= strikePrice) ? contractBuyer : contractCreator;
            } else {
                recipient = (expiryPrice <= strikePrice) ? contractBuyer : contractCreator;
            }
        }

        isExpired = true;

        (bool success, ) = recipient.call{value: address(this).balance}("");
        require(success, "Transfer failed");

        emit Terminated(expiryPrice, recipient);
    }
}
