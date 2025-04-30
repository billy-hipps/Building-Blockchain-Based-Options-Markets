from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from eth_account import Account
from compile import compile
from create_factory import create_factory

# Handles user login, role selection, and factory contract setup
# Returns:
# - creator: bool, user role (True if contract creator, False if buyer)
# - accountAddress: string, Ethereum address of user
# - privateKey: string, user's private key for transaction signing
# - factory_address: string, deployed Factory contract address
def login():
    # Connect to local Hardhat blockchain node
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    
    # Inject middleware for compatibility with PoA chains like Hardhat
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

    account = None
    privateKey = None

    # Prompt user for role selection
    creator = input("Login as creator? (y/n): ").strip().lower()
    if creator == 'y':
        creator = True
    else:
        creator = False

    # Prompt for login credentials until valid
    valid = False
    while not valid:
        accountAddress = input("Enter your account address: ").strip()
        privateKey = input("Enter your private key: ").strip()

        # Validate private key against provided address
        try:
            account = Account.from_key(privateKey)
            if account.address.lower() != accountAddress.lower():
                print("Invalid account address and private key pair")
                continue
        except ValueError:
            print("Invalid private key")
            continue

        valid = True
        compile()  # Compile contracts before continuing

        factory_address = None

        # Prompt to create a new Factory contract or use an existing one
        while True:
            action = input("Do you want to create a factory contract? (y/n): ")
            if action == 'y':
                print("Creating factory contract...")
                factory_address = create_factory(accountAddress, privateKey, w3)  # Deploy new Factory
                break
            elif action == 'n':
                factory_address = input("Enter the factory address: ")
                factory_address = w3.to_checksum_address(factory_address)  # Normalize address
                break

    return creator, accountAddress, privateKey, factory_address  # Return login session data
