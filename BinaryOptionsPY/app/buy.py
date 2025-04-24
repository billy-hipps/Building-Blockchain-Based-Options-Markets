#==== BUY A CONTRACT ====
from web3 import Web3
from compile import compile
from BO_status import BO_status
from fetch_abi import fetch_abi


def buy(buyerAddress, buyerPrivateKey, deployerAddress, w3):
    # Compile contracts 
    abi = fetch_abi('CreateBO')

    # Call the buyContract function from the contract
    contract = w3.eth.contract(address=deployerAddress, abi=abi)

    # Get the contract price
    price = contract.functions.contractPrice().call() 
    price = int(price) / 1e18

    nonce = w3.eth.get_transaction_count(buyerAddress)
    
    tx_buy = contract.functions.buyContract().build_transaction({
        "from": buyerAddress,
        "gas": 3000000,
        "gasPrice": w3.to_wei("20", "gwei"),
        "nonce": nonce, 
        "value": w3.to_wei(price, "ether")
    })

    signed_tx_buy = w3.eth.account.sign_transaction(tx_buy, private_key=buyerPrivateKey)
    tx_hash = w3.eth.send_raw_transaction(signed_tx_buy.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    BO_status(deployerAddress, abi, w3)
