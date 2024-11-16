// SPDX License-Identifier: MIT
pragma solidity 0.8.28;

// define important events 
event Transfer(address indexed from, address indexed to, uint value);
event Approval(address indexed owner, address indexed spender, uint value);

// Token contract 
contract basicToken {
    string public symbol;
    string public name;
    uint8 public decimals;
    uint public _totalSupply;

    mapping(address => uint) balances; // show balance of a coin in a wallet 
    mapping(address => mapping(address => uint)) allowed; // wallet may allow for token to be spent in > 1 addresses

    constructor() {
        symbol = "ABC";
        name = "Basic Coin";
        decimals = 18;
        _totalSupply = 1_000_001_000_000_000_000_000; // A million + 1 coins with 18 zeros of decimal points 
        balances[0x914CD4762d67386785ff738708E1012E5d098db4] = _totalSupply; // balance of my wallet is total supply (i am the creator)
        emit Transfer(address(0), 0x914CD4762d67386785ff738708E1012E5d098db4, _totalSupply); // any transfer will originate from my wallet? 
    }

    // Implementations of essential functions 
    function totalSupply() public view returns (uint) {
        return _totalSupply - balances[address(0)]; // implement the balances mapping from above 
    }

    function balanceOf(address account) public view returns (uint balance) {
        return balances[account];
    }

    function allowance(address owner, address spender) public view returns (uint remaining) {
        return allowed[owner][spender];
    }

    function transfer(address recipient, uint amount) public returns (bool success) {
        balances[msg.sender] = balances[msg.sender] - amount;
        balances[recipient] = balances[recipient] + amount;
        emit Transfer(msg.sender, recipient, amount);
        return true;
    }

    function approve(address spender, uint amount) public returns (bool success) {
        allowed[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(address sender, address recipient, uint amount) public returns (bool success) {
        balances[sender] = balances[sender] - amount;
        allowed[sender][msg.sender] = allowed[sender][msg.sender] - amount;
        balances[recipient] = balances[recipient] + amount;
        emit Transfer(sender, recipient, amount);
        return true;

    }
}