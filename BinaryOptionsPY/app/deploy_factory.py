from web3 import Web3
from web3.exceptions import ContractLogicError, TransactionNotFound

# Deploy the Factory contract to the blockchain
# Parameters:
# - abi: list, ABI of the Factory contract
# - bytecode: string, compiled bytecode of the Factory contract
# - deployerAccount: string, Ethereum address used to deploy the contract
# - privateKey: string, private key corresponding to deployerAccount
# - w3: Web3 instance, connected to an Ethereum node
# Returns:
# - factory_address: string, deployed contract address or None if failed
def deploy_factory(abi, bytecode, deployerAccount, privateKey, w3):
    if not w3.is_connected():
        print("[Error] Web3 connection failed.")
        return None

    try:
        # Create contract instance
        contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    except Exception as e:
        print(f"[Error] Failed to create contract object: {e}")
        return None

    try:
        nonce = w3.eth.get_transaction_count(deployerAccount)
    except Exception as e:
        print(f"[Error] Failed to retrieve nonce: {e}")
        return None

    try:
        tx = contract.constructor().build_transaction({
            "from": deployerAccount,
            "gas": 30000000,
            "gasPrice": w3.to_wei("20", "gwei"),
            "nonce": nonce
        })
    except ContractLogicError as e:
        print(f"[Contract Error] Failed to build deployment transaction: {e}")
        return None
    except Exception as e:
        print(f"[Error] Unexpected error while building transaction: {e}")
        return None

    try:
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=privateKey)
    except Exception as e:
        print(f"[Error] Failed to sign transaction: {e}")
        return None

    try:
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    except Exception as e:
        print(f"[Error] Failed to send transaction: {e}")
        return None

    try:
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt.status != 1:
            print("[Warning] Deployment transaction failed or was reverted.")
            return None
    except TransactionNotFound:
        print("[Error] Transaction not found on the network.")
        return None
    except Exception as e:
        print(f"[Error] Failed to confirm deployment transaction: {e}")
        return None

    try:
        factory_address = tx_receipt.contractAddress
        print(f'✅ Factory contract deployed at: {factory_address}')
        return factory_address
    except Exception as e:
        print(f"[Error] Failed to retrieve contract address from receipt: {e}")
        return None
