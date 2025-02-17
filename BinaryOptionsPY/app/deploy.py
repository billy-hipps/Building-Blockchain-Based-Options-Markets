from web3 import Web3

def deploy(parameters, abi, bytecode, deployer_account, private_key, w3):
    """
    Deploys the CreateBO contract, calls `deployBinaryOption`, 
    and prints the deployed BinaryOption contract address.

    :return: Tuple (CreateBO contract address, BinaryOption contract address).
    """

    assert w3.is_connected(), "Web3 connection failed!"

    # Create contract object
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    # Get deployer's nonce
    nonce = w3.eth.get_transaction_count(deployer_account)

    # Build transaction for deploying CreateBO
    tx = contract.constructor(
        parameters['strike_price'],
        parameters['strike_date'],
        parameters['payout'],
        parameters['expiry_price'],
        parameters['position'],
        w3.to_wei(parameters['contract_price'], "ether")
    ).build_transaction({
        "from": deployer_account,
        "gas": 3000000,  
        "gasPrice": w3.to_wei("20", "gwei"),
        "nonce": nonce,
        "value": w3.to_wei(parameters['payout'], "ether")  
    })

    # Sign and send the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    # Wait for transaction confirmation
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # Get deployed CreateBO contract address
    create_bo_address = tx_receipt.contractAddress
    print(f"CreateBO Contract Deployed at: {create_bo_address}")
    print(f"CreateBO balance: {w3.eth.get_balance(create_bo_address)}")

    # Load deployed contract instance
    deployed_contract = w3.eth.contract(address=create_bo_address, abi=abi)

    # **Step 1: Get Expected Return Value from `deployBinaryOption`**
    expected_binary_option_address = deployed_contract.functions.deployBinaryOption().call()
    print(f"Expected BinaryOption Address (before txn): {expected_binary_option_address}")

    # Get new nonce for transaction
    nonce = w3.eth.get_transaction_count(deployer_account)

    # **Step 2: Send the transaction**
    tx_binary_option = deployed_contract.functions.deployBinaryOption().build_transaction({
        "from": deployer_account,
        "gas": 3000000,
        "gasPrice": w3.to_wei("20", "gwei"),
        "nonce": nonce
    })

    # Sign and send deployBinaryOption transaction
    signed_tx_binary_option = w3.eth.account.sign_transaction(tx_binary_option, private_key=private_key)
    tx_hash_binary_option = w3.eth.send_raw_transaction(signed_tx_binary_option.raw_transaction)

    # Wait for confirmation
    receipt_binary_option = w3.eth.wait_for_transaction_receipt(tx_hash_binary_option)

    # **Step 3: Get actual deployed Binary Option address**
    binary_option_address = deployed_contract.functions.binaryOptionAddress().call()
    print(f"BinaryOption Contract Deployed at: {binary_option_address}")
    print(f"BO balance: {w3.eth.get_balance(binary_option_address)}")

    return create_bo_address, binary_option_address
