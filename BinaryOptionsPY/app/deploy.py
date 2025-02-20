from web3 import Web3
from BO_status import BO_status
from schedule import fetch_time, schedule
import asyncio

def deploy(parameters, abi, bytecode, deployerAccount, privateKey, w3):
    """
    Deploys the CreateBO contract, calls `deployBinaryOption`, 
    and prints the deployed BinaryOption contract address.

    :return: Tuple (CreateBO contract address, BinaryOption contract address).
    """

    assert w3.is_connected(), "Web3 connection failed!"


    # ======== DEPLOY THE CREATEBO CONTRACT ========

    # Create contract object
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    # Get deployer's nonce
    nonce = w3.eth.get_transaction_count(deployerAccount)

    strikeDate = fetch_time() + 2 * 60  # 2 minutes from now

    # Build transaction for deploying CreateBO
    tx = contract.constructor(
        parameters['strike_price'],
        strikeDate,
        parameters['payout'],
        parameters['expiry_price'],
        parameters['position'],
        w3.to_wei(parameters['contract_price'], "ether")
    ).build_transaction({
        "from": deployerAccount,
        "gas": 3000000,  
        "gasPrice": w3.to_wei("20", "gwei"),
        "nonce": nonce,
        "value": w3.to_wei(parameters['payout'], "ether")  
    })

    # Sign and send the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=privateKey)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    # Wait for transaction confirmation
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # Get deployed CreateBO contract address
    create_bo_address = tx_receipt.contractAddress
    print(f"CreateBO Contract Deployed at: {create_bo_address}")
    print(f"CreateBO balance: {w3.eth.get_balance(create_bo_address) / 10**18}\n")


    # ======== DEPLOY THE BINARYOPTION CONTRACT ========

    # Load deployed contract instance
    deployed_contract = w3.eth.contract(address=create_bo_address, abi=abi)

    # Get new nonce for transaction
    nonce = w3.eth.get_transaction_count(deployerAccount)

    tx_binary_option = deployed_contract.functions.deployBinaryOption().build_transaction({
        "from": deployerAccount,
        "gas": 3000000,
        "gasPrice": w3.to_wei("20", "gwei"),
        "nonce": nonce
    })

    # Sign and send deployBinaryOption transaction
    signed_tx_binary_option = w3.eth.account.sign_transaction(tx_binary_option, private_key=privateKey)
    tx_hash_binary_option = w3.eth.send_raw_transaction(signed_tx_binary_option.raw_transaction)

    # Wait for confirmation
    receipt_binary_option = w3.eth.wait_for_transaction_receipt(tx_hash_binary_option)

    BO_status(create_bo_address, abi, w3)
    
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(schedule(strikeDate, deployerAccount, privateKey, create_bo_address, abi, w3))
    else:
        asyncio.run(schedule(strikeDate, deployerAccount, privateKey, create_bo_address, abi, w3))

    return create_bo_address
