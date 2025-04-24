import time
import pandas as pd
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from deploy import deploy  # 👈 this is your working deploy function
from compile import compile  # assumes you have this
from eth_utils import to_checksum_address

# Web3 setup
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

# Accounts
creator_acct = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"
creator_key = "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d"

# Compile contracts
compiled = compile()
factory_abi, factory_bytecode = compiled["Factory"]
createbo_abi = compiled["CreateBO"][0]

# Deploy Factory
factory = w3.eth.contract(abi=factory_abi, bytecode=factory_bytecode)
nonce = w3.eth.get_transaction_count(creator_acct)

tx = factory.constructor().build_transaction({
    "from": creator_acct,
    "gas": 6000000,
    "gasPrice": w3.to_wei("20", "gwei"),
    "nonce": nonce
})
signed_tx = w3.eth.account.sign_transaction(tx, private_key=creator_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
factory_address = receipt.contractAddress
factory_address = to_checksum_address(factory_address)

# Parameters template
base_params = {
    'ticker': 'AAPL',
    'strike_price': 0,  # will be set by deploy()
    'strike_date': 120,
    'contract_price': 1,   # Updated to 1 ETH
    'payout': 1,           # Updated to 1 ETH
    'position': True
}


# Results store
browse_results = []

# Loop through number of contracts
for contract_count in range(1, 201, 10):
    print(f"\n🚀 Deploying and browsing {contract_count} contracts...")
    deployed_addresses = []

    for i in range(contract_count):
        # Each deploy() returns a CreateBO address
        address = deploy(
            factoryAddress=factory_address,
            parameters=base_params.copy(),
            factory_abi=factory_abi,
            factory_bytecode=factory_bytecode,
            createBO_abi=createbo_abi,
            creatorAddress=creator_acct,
            privateKey=creator_key,
            w3=w3
        )
        if address:
            deployed_addresses.append(address)

    # Simulate "Browse"
    start_time = time.time()

    for addr in deployed_addresses:
        contract = w3.eth.contract(address=addr, abi=createbo_abi)
        try:
            contract.functions.ticker().call()
            contract.functions.contractPrice().call()
            contract.functions.strikePrice().call()
            contract.functions.payout().call()
            contract.functions.position().call()
            contract.functions.isBought().call()
            contract.functions.isExpired().call()
        except Exception as e:
            print(f"❌ Browse error for contract {addr}: {e}")

    end_time = time.time()

    browse_results.append({
        "Contracts": contract_count,
        "Browse Time (s)": round(end_time - start_time, 4)
    })

# Save to CSV
df = pd.DataFrame(browse_results)
df.to_csv("browse_time_scaling.csv", index=False)
print("✅ Test complete. Saved as browse_time_scaling.csv")