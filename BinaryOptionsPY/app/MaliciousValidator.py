import json
import time
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from compile import compile  # Your custom Solidity compiler wrapper

# ==== Setup ====
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))  # Connect to local blockchain
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)  # PoA middleware for compatibility

# ==== Accounts ====
attacker = w3.eth.accounts[4]  # Use account[4] as attacker (adjust as needed)

# ==== Compile and Load Contract ====
compiled = compile()  # Compile all contracts
malicious_abi = compiled["MaliciousValidator"][0]  # Extract ABI
malicious_bytecode = compiled["MaliciousValidator"][1]  # Extract Bytecode

# ==== Deployed System Contracts (Update these as needed) ====
create_bo_address = "0xa16E02E87b7454126E5E10d957A927A7F5B5d2be"
binary_option_address = "0x4CEc804494d829bEA93AB8eA7045A7efBED3c229"
time_oracle_address = "0x8Ff3801288a85ea261E4277d44E1131Ea736F77B"

# ==== Deploy MaliciousValidator ====
MaliciousValidator = w3.eth.contract(abi=malicious_abi, bytecode=malicious_bytecode)

# Build constructor transaction with references to system contracts
tx = MaliciousValidator.constructor(
    create_bo_address,
    binary_option_address,
    time_oracle_address
).build_transaction({
    "from": attacker,
    "gas": 5_000_000,
    "gasPrice": w3.to_wei("20", "gwei"),
    "nonce": w3.eth.get_transaction_count(attacker),
    "value": w3.to_wei(1, "ether")  # Send ETH if required by constructor
})

# Deploy contract and wait for receipt
tx_hash = w3.eth.send_transaction(tx)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
malicious_address = receipt.contractAddress  # Store deployed address

print(f"✅ MaliciousValidator deployed at {malicious_address}")

# Reconnect to deployed instance
malicious = w3.eth.contract(address=malicious_address, abi=malicious_abi)

# ==== Run Test and Listen to Events ====
# Calls a test function by name and prints the result
def run_test(fn_name):
    print(f"\n🧪 Running: {fn_name}")

    # Build transaction to call the test function
    tx = malicious.functions[fn_name]().build_transaction({
        "from": attacker,
        "gas": 3_000_000,
        "gasPrice": w3.to_wei("20", "gwei"),
        "nonce": w3.eth.get_transaction_count(attacker)
    })

    tx_hash = w3.eth.send_transaction(tx)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # Decode TestResult events
    logs = malicious.events.TestResult().process_receipt(receipt)
    for event in logs:
        test = event["args"]["testName"]
        passed = event["args"]["passed"]
        print(f"{test} → {'✅ PASSED' if passed else '❌ FAILED'}")

# ==== Run All Tests ====
tests = [
    "testEarlyWithdrawal",
    "testOverwriteBuyer",
    "testCreatorImmutable",
    "testFundDraining",
    "testOracleEnforcement"
]

# Run each test with delay to prevent nonce collision
for test_fn in tests:
    run_test(test_fn)
    time.sleep(1)

print("\n🧾 All tests complete.")
