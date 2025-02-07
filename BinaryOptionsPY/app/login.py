from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from eth_account import Account 

def login():
    # Connect to local Hardhat blockchain
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    
    # Add middleware for PoA chains if needed (e.g., Hardhat or Binance Smart Chain)
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

    account = None
    private_key = None

    # Choose login type
    creator = input("Login as creator? (y/n): ").strip().lower() == 'y'

    # Login with account address and private key
    valid = False
    while not valid:
        account_address = input("Enter your account address: ").strip()
        private_key = input("Enter your private key: ").strip()

        # Check if the account address and private key are valid
        try:
            account = Account.from_key(private_key)
            if account.address.lower() != account_address.lower():
                print("Invalid account address and private key pair")
                continue
        except ValueError:
            print("Invalid private key")
            continue

        valid = True

    return creator, account_address, private_key
