// SPDX License-Identifier: UNLICENSED
pragma solidity 0.8.28;

event Transfer(address indexed from, address indexed to, uint value);
event Approval(address indexed owner, address indexed buyer, uint value);
//event Terminmation(address indexed owner, address indexed buyer, uint payOff;);  

// Token contract 
contract BinaryOption {
    string public symbol;
    string public name;
    uint8 public decimals;
    uint public _totalSupply;
    // uint strikePrice;
    // uint strikeDate;
    // uint payOff;
    // uint contractPrice;
    // string assetTicker; 
    mapping(address => uint) balances; // show balance of a coin in a wallet 
    mapping(address => mapping(address => uint)) allowed; // wallet may allow for token to be spent in > 1 addresses

    constructor() {
        symbol = "ABO";
        name = "AAPL_BO";
        decimals = 18;
        _totalSupply = 1_000_000_000_000_000; //1 contract with 18 zeros of decimal points 
        // strikePrice = 224;
        // strikeDate = 10 days;
        // payOff = 5 gwei;
        // contractPrice = 1 gwei; 
        // assetTicker = "AAPL"

        balances[0x0966307038aB5cb9DcDeca50993e1f7153615eDa] = _totalSupply; // balance of my wallet is total supply (i am the creator)
        emit Transfer(address(0), 0x0966307038aB5cb9DcDeca50993e1f7153615eDa, _totalSupply); // any transfer will originate from my wallet? 
    }

    // Implementations of essential functions 
    function totalSupply() public view returns (uint) {
        return _totalSupply - balances[address(0)]; // implement the balances mapping from above 
    }

    function balanceOf(address account) public view returns (uint balance) {
        return balances[account];
    }

    function allowance(address owner, address buyer) public view returns (uint remaining) {
        return allowed[owner][buyer];
    }

    function transfer(address recipient, uint amount) external returns (bool success) {
        balances[msg.sender] = balances[msg.sender] - amount;
        balances[recipient] = balances[recipient] + amount;
        emit Transfer(msg.sender, recipient, amount);
        return true;
    }

    function approve(address buyer, uint amount) public returns (bool success) {
        allowed[msg.sender][buyer] = amount;
        emit Approval(msg.sender, buyer, amount);
        return true;
    }

    function transferFrom(address sender, address recipient, uint amount) public returns (bool success) {
        balances[sender] = balances[sender] - amount;
        allowed[sender][msg.sender] = allowed[sender][msg.sender] - amount;
        balances[recipient] = balances[recipient] + amount;
        emit Transfer(sender, recipient, amount);
        return true;

    }

    //function validate(address creator, address buyer, uint price, uint payOff) public returns (bool success) 
        // check the creator has sufficient funds to issue the payoff 
        // check the buyer has sufficient funds to buy the contract 
    
    //function collectPayout(address creator, uint payOff) public returns(bool success) 
        //send the payoff amount from the creator of the contract to the contract 

    //function terminate(address owner, address recipient, uint payOff;) external returns (bool success)
        //if date is before stike date -> who is terminating? -> issue appropriate penalty
        //else: if asset price is >= strike price, payOff = payOff, recipient = owner, call complete function 
        //      else: payOff = 0, recipient = creator 
}

