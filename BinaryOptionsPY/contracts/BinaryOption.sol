// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.23;

contract BinaryOption {

    // ======== State Variables ========
    address payable public immutable deployerAddress;    // Address that deployed this contract (factory)
    address payable public immutable contractCreator;    // Creator of the binary option
    address payable private contractBuyer;               // Buyer of the contract, if purchased
    bool private isBought;                               // Indicates if contract has been bought
    bool private isExpired;                              // Indicates if contract has been terminated
    string private winner;                               // Winner of the contract (Buyer or Creator)

    // ======== BO Parameters ========
    bytes32 public immutable ticker;                     // Asset identifier (e.g., AAPL)
    string public constant symbol = "BO";                // Token symbol (informational only)
    string public constant name = "Binary Option";       // Token name (informational only)

    uint256 public immutable strikePrice;                // Target price to determine outcome
    uint256 public immutable strikeDate;                 // UNIX timestamp at which outcome is evaluated
    uint256 public immutable payout;                     // Amount paid out if condition is met
    bool public immutable position;                      // true = long, false = short

    uint256 private expiryPrice;                         // Price at expiry (set at termination)
    uint256 public immutable contractPrice;              // Purchase price of the option

    // ======== Events ========
    event Bought(address indexed buyer);                 // Emitted when contract is bought
    event Terminated(uint256 expiryPrice, address recipient); // Emitted when contract is closed
    event PriceUpdate(uint256 newPrice);                 // Emitted during termination with final price

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
        strikeDate = block.timestamp + _strikeDate;      // Relative future timestamp
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

    // ======== Modifiers ========

    // Restricts function to deployer/factory
    modifier onlyDeployer() {
        require(msg.sender == deployerAddress, "BO: Not authorized");
        _;
    }

    // Restricts function to internal calls only
    modifier onlyThis() {
        require(msg.sender == address(this), "BO: Not authorized");
        _;
    }

    // ======== Fallback Function ========
    // Accept ETH transfers directly
    receive() external payable {}

    // ======== Public Read Functions ========

    // Returns contract balance (only callable by deployer)
    function getBalance() public view onlyDeployer returns (uint256) {
        return address(this).balance;
    }

    // Returns current status for monitoring
    function getStatus() external view onlyDeployer returns (bool, bool, address, uint256) {
        return (isBought, isExpired, contractBuyer, address(this).balance);
    }

    function getWinner() external view onlyDeployer returns (string memory) {
        return winner;
    }

    // Triggers purchase of the contract
    function buy(address payable _contractBuyer) external onlyDeployer {
        require (!isBought, "BO: Contract has already been bought.");
        _buy(_contractBuyer);
    }

    // Internal function to set buyer and update state
    function _buy(address payable _contractBuyer) private {
        contractBuyer = _contractBuyer;
        isBought = true;
        emit Bought(_contractBuyer);
    }

    // Triggers contract resolution with a final price
    function terminate(uint256 _newPrice) external onlyDeployer {
        require (!isExpired, "BO: Contract has already expired.");
        expiryPrice = _newPrice;
        emit PriceUpdate(_newPrice);
        winner = _terminate();
    }

    // Internal logic to decide payout and perform fund transfer
    function _terminate() private returns (string memory) {
        address payable recipient;

        // If not bought, refund creator
        if (!isBought) {
            recipient = contractCreator;
        } else {
            // Determine winner based on position and expiry price
            if (position == true) {
                // Long: buyer wins if price >= strike
                recipient = (expiryPrice >= strikePrice) ? contractBuyer : contractCreator;
            } else {
                // Short: buyer wins if price <= strike
                recipient = (expiryPrice <= strikePrice) ? contractBuyer : contractCreator;
            }
        }

        isExpired = true;

        // Transfer all ETH to the winning recipient
        (bool success, ) = recipient.call{value: address(this).balance}("");
        require(success, "Transfer failed");

        emit Terminated(expiryPrice, recipient);

        string memory _winner;

        if (recipient == contractBuyer) {
            _winner = "Buyer";
        } else {
            _winner = "Creator";
        }
        return _winner;
    }
}
