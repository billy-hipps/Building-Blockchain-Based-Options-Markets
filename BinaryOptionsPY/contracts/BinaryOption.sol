// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.28;

contract BinaryOption {
    // ======== Events ========
    event Transfer(address indexed from, address indexed to, uint value);
    event Approval(address indexed owner, address indexed buyer, uint value);
    // event Termination(address indexed owner, address indexed buyer, uint payout);
    // event Bought(address indexed owner, address indexed buyer, uint price);

    // ======== State Variables ========
    string public symbol;
    string public name;
    uint8 public decimals;
    uint public _totalSupply;
    uint public strikePrice;
    uint public strikeDate;
    uint public payout;
    uint public expiryPrice;
    bool public position; // true = long, false = short
    uint public contractPrice;
    address public creator;
    bool public bought;

    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;

    // ======== Constructor ========
    constructor(
        uint _strikePrice, 
        uint _strikeDate, 
        uint _payout, 
        uint _expiryPrice,
        bool _position, 
        uint _contractPrice, 
        address _creator
    ) {
        symbol = "BO";
        name = "Binary Option";
        decimals = 18;
        _totalSupply = 1_000_000_000_000_000; // 1 contract with 15 decimal places

        // Initialize parameters
        strikePrice = _strikePrice;
        strikeDate = block.timestamp + _strikeDate; // Assuming `_strikeDate` is a duration in seconds
        payout = _payout;
        expiryPrice = _expiryPrice;
        position = _position;
        contractPrice = _contractPrice;
        creator = _creator;

        // Assign total supply to creator
        balances[creator] = _totalSupply;
        emit Transfer(address(0), creator, _totalSupply);
    }

    // ======== View Functions (ERC20) ========
    function totalSupply() public view returns (uint) {
        return _totalSupply - balances[address(0)];
    }

    function balanceOf(address account) public view returns (uint) {
        return balances[account];
    }

    function allowance(address owner, address buyer) public view returns (uint) {
        return allowed[owner][buyer];
    }

    // ======== ERC20 Token Transfers ========
    function transfer(address recipient, uint amount) external returns (bool) {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        balances[msg.sender] -= amount;
        balances[recipient] += amount;
        
        emit Transfer(msg.sender, recipient, amount);
        return true;
    }

    function approve(address buyer, uint amount) public returns (bool) {
        allowed[msg.sender][buyer] = amount;
        emit Approval(msg.sender, buyer, amount);
        return true;
    }

    function transferFrom(address sender, address recipient, uint amount) public returns (bool) {
        require(balances[sender] >= amount, "Insufficient balance");
        require(allowed[sender][msg.sender] >= amount, "Allowance exceeded");

        balances[sender] -= amount;
        allowed[sender][msg.sender] -= amount;
        balances[recipient] += amount;

        emit Transfer(sender, recipient, amount);
        return true;
    }



    // Application specific functions

    //function buy(address buyer, uint price) public returns (bool success) 
        // check the buyer has sufficient funds to buy the contract 
        // check the buyer has approved the contract to spend the funds 
        // transfer the funds from the buyer to the contract

    //function validate(address creator, address buyer, uint price, uint payout) public returns (bool success) 
        // check the creator has sufficient funds to issue the payout 
        // check the buyer has sufficient funds to buy the contract 
    
    //function collectPayout(address creator, uint payout) public returns(bool success) 
        //send the payout amount from the creator of the contract to the contract 

    //function terminate(address owner, address recipient, uint payout;) external returns (bool success)
        //if date is before stike date -> who is terminating? -> issue appropriate penalty
        //else: if asset price is >= strike price, payout = payout, recipient = owner, call complete function 
        //      else: payout = 0, recipient = creator 
}