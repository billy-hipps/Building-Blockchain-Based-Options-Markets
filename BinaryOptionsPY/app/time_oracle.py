import requests
from web3 import Web3

CONTRACT_ADDRESS = "0xYourTimeOracleContract"
ABI = [...]  # Load ABI from TimeOracle.json

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

# Fetch accurate UTC time
def fetch_time():
    response = requests.get("http://worldtimeapi.org/api/timezone/Etc/UTC")
    return response.json()["unixtime"]  # Returns UTC timestamp

# Update smart contract with new time
def update_time(deployerAccount, privateKey, oracleContract, deployerContract):
    timestamp = fetch_time()
    nonce = web3.eth.get_transaction_count(deployerAccount)

    tx = oracleContract.functions.updateTime(timestamp).build_transaction({
        "from": deployerAccount,
        "nonce": nonce,
        "gas": 100000,
        "gasPrice": web3.to_wei('5', 'gwei')
    })

    signed_tx = web3.eth.account.sign_transaction(tx, privateKey)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Transaction sent: {tx_hash.hex()}")

# Run the update function
update_time()

