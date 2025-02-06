from flask import Flask, request, jsonify
from web3 import Web3
import json

app = Flask(__name__)

# Connect to Hardhat Local Network
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Load Contract ABI & Address
with open("frontend/src/contracts/contract-address.json") as f:
    contract_address = json.load(f)["BinaryOption"]

with open("frontend/src/contracts/BinaryOption.json") as f:
    contract_abi = json.load(f)["abi"]

# Initialize contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Default Account for Transactions
DEPLOYER_ADDRESS = w3.eth.accounts[0]
PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

@app.route("/balance", methods=["GET"])
def get_balance():
    """ Get balance of an address """
    address = request.args.get("address")
    balance = contract.functions.balanceOf(address).call()
    return jsonify({"balance": balance})

@app.route("/transfer", methods=["POST"])
def transfer_tokens():
    """ Transfer tokens to another user """
    data = request.json
    sender = data["sender"]
    recipient = data["recipient"]
    amount = int(data["amount"])

    tx = contract.functions.transfer(recipient, amount).build_transaction({
        "from": sender,
        "nonce": w3.eth.get_transaction_count(sender),
        "gas": 200000,
        "gasPrice": w3.to_wei("10", "gwei"),
    })

    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return jsonify({"tx_hash": tx_hash.hex()})

@app.route("/token-info", methods=["GET"])
def token_info():
    """ Get token name, symbol, and total supply """
    name = contract.functions.name().call()
    symbol = contract.functions.symbol().call()
    supply = contract.functions.totalSupply().call()
    return jsonify({"name": name, "symbol": symbol, "total_supply": supply})

if __name__ == "__main__":
    app.run(debug=True)
