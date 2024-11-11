// SPDX License-Identifier: UNLICENSED
pragma solidity 0.8.26;

// ERC Token Standard #20 Interface 
interface ERC20Interface {
    function totalSupply() external view returns (uint);
    function balanceOf(address account) external view returns (uint balance);
    function allowance(address owner, address sender) external view returns (uint remaining);
    function transfer(address recipient, uint amount) external returns (bool success);
    function approve(address spender, uint amount) external returns (bool success);
    function transferFrom(address sender, address recipient, uint amount) external returns (bool success);

    event Transfer(address indexed from, address indexed to, uint value);
    event Approval(address indexed owner, address indexed spender, uint value);

}

// Token contract 
contract basicToken is ERC20Interface {
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