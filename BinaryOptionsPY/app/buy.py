#==== BUY A CONTRACT ====
from web3 import Web3
from compile import compile


def buy(price, buyerAddress, buyerPrivateKey, deployerAddress, w3):
    # Compile contracts 
    compiled_data = compile()
    createContract = compiled_data["CreateBO"]

    # Call the buyContract function from the contract
    contract = w3.eth.contract(address=deployerAddress, abi=createContract[0])

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

    buyer = contract.functions.getBuyer().call()
    is_bought = contract.functions.get_isBought().call()

    print(f"Buyer: {buyer}")
    print(f"isBought: {is_bought}")
