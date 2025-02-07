from web3 import Web3
import json
from eth_account import Account


def deploy(parameters, abi, bytecode, deployer_account, private_key):

    # Connect to a local Ethereum blockchain
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

    # Deploy the contract
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    # Build the transaction
    tx = contract.constructor(
        parameters['strike_price'],
        parameters['strike_date'],
        parameters['payout'],
        parameters['expiry_price'],
        parameters['position'],
        parameters['contract_price'],
        deployer_account
    ).build_transaction({
        "from": deployer_account,
        "gas": 3000000,
        "gasPrice": w3.to_wei("20", "gwei"),
        "nonce": w3.eth.get_transaction_count(deployer_account),
    })

    # Sign and send the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # Get deployed contract address
    contract_address = tx_receipt.contractAddress

    return contract_address
