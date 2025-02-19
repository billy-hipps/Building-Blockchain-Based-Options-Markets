import requests
from web3 import Web3
from eth_account.messages import encode_defunct

# Setup Web3 connection
RPC_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
PRIVATE_KEY = "YOUR_PRIVATE_KEY"
CONTRACT_ADDRESS = "0xYourContractAddress"
ABI = [...]  # Load the ABI of your TimeOracle contract

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

# Fetch accurate time from API
def fetch_time():
    response = requests.get("http://worldtimeapi.org/api/timezone/Etc/UTC")
    return response.json()["unixtime"]  # Returns UTC timestamp

# Send time update transaction
def update_time():
    timestamp = fetch_time()
    nonce = web3.eth.get_transaction_count(account.address)

    tx = contract.functions.updateTime(timestamp).build_transaction({
        "from": account.address,
        "nonce": nonce,
        "gas": 100000,
        "gasPrice": web3.to_wei('5', 'gwei')
    })

    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"Transaction sent: {tx_hash.hex()}")

# Run the update function
update_time()
