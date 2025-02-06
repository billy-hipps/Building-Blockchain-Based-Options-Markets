from web3 import Web3
from solcx import compile_source, install_solc, set_solc_version

# Install and set Solidity compiler version
install_solc('0.8.28')  
set_solc_version('0.8.28')

# Connect to Hardhat's local blockchain
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Ensure connection
if not w3.is_connected():
    raise Exception("Web3 is not connected to Hardhat!")

# Load Solidity contract
with open("contracts/BinaryOption.sol", "r") as file:
    contract_source = file.read()

# Compile Solidity contract
compiled_sol = compile_source(contract_source, output_values=['abi', 'bin'])
contract_id, contract_interface = compiled_sol.popitem()

# Extract contract ABI & Bytecode
abi = contract_interface['abi']
bytecode = contract_interface['bin']

# Use the first pre-funded Hardhat account
hardhat_accounts = w3.eth.accounts  # List of available accounts
DEPLOYER_ADDRESS = hardhat_accounts[0]  # First account
print(f"Deployer Address: {DEPLOYER_ADDRESS}")
PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"  # Private key of first account

# Deploy Contract
BinaryOption = w3.eth.contract(abi=abi, bytecode=bytecode)

# Build transaction
tx = BinaryOption.constructor().build_transaction({
    'from': DEPLOYER_ADDRESS,
    'nonce': w3.eth.get_transaction_count(DEPLOYER_ADDRESS),
    'gas': 2000000,
    'gasPrice': w3.to_wei('10', 'gwei')
})

# Sign and send transaction
signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

# Wait for transaction to be mined
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Print contract address
contract_address = tx_receipt.contractAddress
print(f"Contract deployed at: {contract_address}")

# Interact with deployed contract
binary_option = w3.eth.contract(address=contract_address, abi=abi)

# Read Token Name and Symbol
print(f"Token Name: {binary_option.functions.name().call()}")
print(f"Token Symbol: {binary_option.functions.symbol().call()}")
print(f"Total Supply: {binary_option.functions.totalSupply().call()}")
