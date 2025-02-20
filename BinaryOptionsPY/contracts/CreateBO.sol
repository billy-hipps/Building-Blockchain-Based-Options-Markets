// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.28;

import "./BinaryOption.sol";
import "./TimeOracle.sol";

// ======== Interface for BinaryOption ========
interface IBinaryOption {
    function buy(address payable _contractBuyer) external;
    function getStatus() external view returns (bool, bool, address, uint256);
    function terminate() external;

}

interface ITimeOracle {
    function getTime(uint256 _newTime) external returns (uint256);
}

contract CreateBO {

    // ======== State Variables ========
    address payable private creator;
    uint256 private balance;
    bool private isDeployed;
    bool private isBought;
    bool private isExpired;
    address private timeOracleAddress;

    // ======== BO Variables ========
    uint256 private strikePrice;
    uint256 private strikeDate;
    uint256 private payout;
    uint256 private expiryPrice;
    bool private position;
    uint256 private contractPrice;
    address payable private buyer;
    address private binaryOptionAddress;
    uint256 private currentTime;
    uint256 private timeDelta;
    uint256 private currentAssetPrice;
    

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

        timeOracleAddress = deployTimeOracle();
        
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


    function get_BO_status() public view returns (bool, bool, address, uint256) {
        require(msg.sender == creator, "Only creator can check the status of the contract");
        (bool _isBought, bool _isExpired, address _buyer, uint256 _balance) = IBinaryOption(binaryOptionAddress).getStatus();
        return (_isBought, _isExpired, _buyer, _balance);
    }


    // ======== Deploy Binary Option ========
    function deployBinaryOption() public {
        require(msg.sender == creator, "Only creator can deploy the contract");

        binaryOptionAddress = _deployBinaryOption();
        require(binaryOptionAddress != address(0), "BinaryOption contract not deployed");
        
        (bool success, ) = payable(binaryOptionAddress).call{value: address(this).balance}("");
        require(success, "Transfer to BinaryOption failed");

        emit Created(creator, address(this));

    }


    function _deployBinaryOption() private returns (address payable) {
        BinaryOption bo = new BinaryOption(
            strikePrice,
            strikeDate,
            payout,
            expiryPrice,
            position,
            contractPrice,
            creator, 
            payable(address(this))
        );
        return payable(address(bo));
    }


    // ======== Buy Binary Option Contract ========
    function buyContract() public payable {
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

    function deployTimeOracle() public returns (address) {
        TimeOracle timeOracle = new TimeOracle(address(this));
        return address(timeOracle);
    }

    function timeUpdate(uint256 _newTime) public {
        currentTime = ITimeOracle(timeOracleAddress).getTime(_newTime);
        timeDelta = strikeDate - currentTime;

        if (timeDelta <= 0) {
            IBinaryOption(binaryOptionAddress).terminate();
        } else {
            return;
        }
    }
    
}
