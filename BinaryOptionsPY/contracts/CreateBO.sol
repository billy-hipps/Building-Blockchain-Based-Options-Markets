// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.23;

import "./BinaryOption.sol";
import "./TimeOracle.sol";

// ======== Interfaces ========
interface IBinaryOption {
    function buy(address payable _contractBuyer) external;
    function getStatus() external view returns (bool, bool, address, uint256);
    function getWinner() external view returns (string memory);
    function terminate(uint256 _newPrice) external;
}

interface ITimeOracle {
    function oracleUpdate(uint256 _newTime, uint256 _newPrice) external returns (uint256, uint256);
}

// ======== CreateBO Contract ========
contract CreateBO {

    // ======== State Variables ========
    address public immutable factory;
    address payable public immutable creator;
    address payable public buyer;
    address public binaryOptionAddress;
    address public immutable timeOracleAddress;
    string public winner;

    bool public isBought;
    bool public isExpired;

    // ======== BO Parameters ========
    bytes32 public immutable ticker;
    uint256 public immutable strikePrice;
    uint256 public immutable strikeDate;
    uint256 public immutable payout;
    bool public immutable position;
    uint256 public immutable contractPrice;

    uint256 private currentTime;
    uint256 private timeDelta;
    uint256 private currentAssetPrice;

    // ======== Events ========
    event Deposited(address indexed sender, uint256 amount);
    event Created(address indexed creator, address contractAddress);
    event Bought(address indexed buyer, address indexed contractAddress);

    // ======== Constructor ========
    constructor(
        address _factory,
        bytes32 _ticker,
        uint256 _strikePrice,
        uint256 _strikeDate,
        uint256 _payout,
        bool _position,
        uint256 _contractPrice,
        address payable _creator
    ) payable {
        require(_factory != address(0), "CreateBO: Factory address cannot be zero");
        require(_creator != address(0), "CreateBO: Creator address cannot be zero");

        factory = _factory;
        creator = _creator;

        ticker = _ticker;
        strikePrice = _strikePrice;
        strikeDate = _strikeDate;
        payout = _payout;
        position = _position;
        contractPrice = _contractPrice;

        timeOracleAddress = deployTimeOracle();
        isBought = false;
        isExpired = false;
    }

    modifier onlyCreator() {
        require(msg.sender == creator, "CreateBO: Only creator can call this function");
        _;
    }

    modifier onlyFactory() {
        require(msg.sender == factory, "CreateBO: Only factory can call this function");
        _;
    }

    modifier onlyThis() {
        require(msg.sender == address(this), "CreateBO: Only this contract can call this function");
        _;
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
    }

    // ======== Time Oracle ========
    function deployTimeOracle() public returns (address) {
        TimeOracle timeOracle = new TimeOracle(address(this));
        return address(timeOracle);
    }

    function timeUpdate(uint256 _newTime, uint256 _newPrice) public onlyCreator {
        (currentTime, currentAssetPrice) = ITimeOracle(timeOracleAddress).oracleUpdate(_newTime, _newPrice);
        timeDelta = strikeDate - currentTime;

        if (timeDelta <= 0) {
            isExpired = true;
            IBinaryOption(binaryOptionAddress).terminate(_newPrice);
            winner = IBinaryOption(binaryOptionAddress).getWinner();
        }
    }

    function get_BO_status() public view onlyCreator returns (bool, bool, address, uint256) {
        return IBinaryOption(binaryOptionAddress).getStatus();
    }

    // ======== Deploy Binary Option ========
    function deployBinaryOption() public onlyFactory {
        binaryOptionAddress = address(_deployBinaryOption());
        require(binaryOptionAddress != address(0), "CreateBO: BinaryOption contract not deployed");

        (bool success, ) = payable(binaryOptionAddress).call{value: address(this).balance}("");
        require(success, "CreateBO: Transfer to BinaryOption failed");

        emit Created(creator, address(this));
    }

    function _deployBinaryOption() private returns (address payable) {
        BinaryOption bo = new BinaryOption(
            ticker,
            strikePrice,
            strikeDate,
            payout,
            position,
            contractPrice,
            creator, 
            payable(address(this))
        );
        return payable(address(bo));
    }

    // ======== Buy Binary Option Contract ========
    function buyContract() public payable {
        require(binaryOptionAddress != address(0), "CreateBO: BinaryOption not deployed");
        require(msg.sender != creator, "CreateBO: Creator cannot buy the contract!");
        require(msg.value >= contractPrice, "CreateBO: Incorrect ETH amount sent!");
        require(!isBought, "CreateBO: Contract already bought!");
        require(!isExpired, "CreateBO: Contract already expired!");

        isBought = true;
        IBinaryOption(binaryOptionAddress).buy(payable(msg.sender));
        
        buyer = payable(msg.sender);

        (bool success, ) = creator.call{value: msg.value}("");
        require(success, "CreateBO: Transfer to creator failed");

        emit Bought(msg.sender, address(this));
    }
}
