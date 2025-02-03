import json
import subprocess
import time
from web3 import Web3

# Step 1: Compile Solidity Contract with Hardhat
print("🔄 Compiling Solidity contract using Hardhat...")
try:
    subprocess.run(["npx", "hardhat", "compile"], check=True)
    print("✅ Compilation successful!")
except subprocess.CalledProcessError as e:
    print("❌ Compilation failed!")
    raise e

# Step 2: Wait briefly to ensure files are written
time.sleep(2)

# Step 3: Load compiled contract data from Hardhat's artifacts
contract_path = "artifacts/contracts/BinaryOption.sol/BinaryOption.json"

try:
    with open(contract_path, "r") as file:
        contract_json = json.load(file)
        abi = contract_json["abi"]
        bytecode = contract_json["bytecode"]
    print("✅ ABI & Bytecode loaded successfully!")
except FileNotFoundError:
    print(f"❌ Could not find compiled contract at {contract_path}")
    exit(1)

# Step 4: Connect to Hardhat's local Ethereum node
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

if not w3.is_connected():
    raise Exception("❌ Web3 is not connected to Hardhat!")

# Step 5: Use the first Hardhat account for deployment
hardhat_accounts = w3.eth.accounts  # List of Hardhat accounts
DEPLOYER_ADDRESS = hardhat_accounts[0]  # First account
PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"  # Replace with your Hardhat account private key

print(f"🚀 Deploying contract from: {DEPLOYER_ADDRESS}")

# Step 6: Deploy Contract
BinaryOption = w3.eth.contract(abi=abi, bytecode=bytecode)

tx = BinaryOption.constructor().build_transaction({
    'from': DEPLOYER_ADDRESS,
    'nonce': w3.eth.get_transaction_count(DEPLOYER_ADDRESS),
    'gas': 5000000,  # Increased gas
    'gasPrice': w3.to_wei('10', 'gwei')
})

# Step 7: Sign and Send Transaction
signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

# Step 8: Wait for Deployment to Complete
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress

print(f"🎉 Contract successfully deployed at: {contract_address}")

# Step 9: Interact with the Deployed Contract
binary_option = w3.eth.contract(address=contract_address, abi=abi)

print(f"🔹 Token Name: {binary_option.functions.name().call()}")
print(f"🔹 Token Symbol: {binary_option.functions.symbol().call()}")
print(f"🔹 Total Supply: {binary_option.functions.totalSupply().call()}")

# Step 10: Save Contract Address & ABI for Frontend
frontend_dir = "../frontend/src/contracts"
contract_data = {"BinaryOption": contract_address}

try:
    import os
    os.makedirs(frontend_dir, exist_ok=True)

    with open(f"{frontend_dir}/contract-address.json", "w") as f:
        json.dump(contract_data, f, indent=2)

    with open(f"{frontend_dir}/BinaryOption.json", "w") as f:
        json.dump(contract_json, f, indent=2)

    print("✅ Contract address & ABI saved for frontend!")
except Exception as e:
    print(f"❌ Error saving frontend files: {e}")
