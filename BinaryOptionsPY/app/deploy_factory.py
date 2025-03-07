from web3 import Web3


def deploy_factory(abi, bytecode, deployerAccount, privateKey, w3):
    
    assert w3.is_connected(), "Web3 connection failed!"

    # Create contract object
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    # Get deployer's nonce
    nonce = w3.eth.get_transaction_count(deployerAccount)

    tx = contract.constructor().build_transaction({
        "from": deployerAccount,
        "gas": 30000000,  
        "gasPrice": w3.to_wei("20", "gwei"),
        "nonce": nonce
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=privateKey)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    factory_address = tx_receipt.contractAddress

    print(f'Factory contract deployed at: {factory_address}')

    return factory_address