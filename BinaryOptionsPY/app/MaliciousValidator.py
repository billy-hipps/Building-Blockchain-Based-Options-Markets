import json
import time
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from compile import compile  # your custom compile function

# ==== Setup ====
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

# ==== Accounts ====
attacker = w3.eth.accounts[4]  # Adjust if needed

# ==== Compile and Load Contract ====
compiled = compile()
malicious_abi = compiled["MaliciousValidator"][0]
malicious_bytecode = compiled["MaliciousValidator"][1]

# ==== Deployed System Contracts (Update these!) ====
create_bo_address = "0xa16E02E87b7454126E5E10d957A927A7F5B5d2be"
binary_option_address = "0x4CEc804494d829bEA93AB8eA7045A7efBED3c229"
time_oracle_address = "0x8Ff3801288a85ea261E4277d44E1131Ea736F77B"

# ==== Deploy MaliciousValidator ====
MaliciousValidator = w3.eth.contract(abi=malicious_abi, bytecode=malicious_bytecode)

tx = MaliciousValidator.constructor(
    create_bo_address,
    binary_option_address,
    time_oracle_address
).build_transaction({
    "from": attacker,
    "gas": 5_000_000,
    "gasPrice": w3.to_wei("20", "gwei"),
    "nonce": w3.eth.get_transaction_count(attacker),
    "value": w3.to_wei(1, "ether")
})

tx_hash = w3.eth.send_transaction(tx)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
malicious_address = receipt.contractAddress

print(f"✅ MaliciousValidator deployed at {malicious_address}")

malicious = w3.eth.contract(address=malicious_address, abi=malicious_abi)

# ==== Run Test and Listen to Events ====
def run_test(fn_name):
    print(f"\n🧪 Running: {fn_name}")
    tx = malicious.functions[fn_name]().build_transaction({
        "from": attacker,
        "gas": 3_000_000,
        "gasPrice": w3.to_wei("20", "gwei"),
        "nonce": w3.eth.get_transaction_count(attacker)
    })
    tx_hash = w3.eth.send_transaction(tx)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

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

for test_fn in tests:
    run_test(test_fn)
    time.sleep(1)  # Prevent nonce collision

print("\n🧾 All tests complete.")
