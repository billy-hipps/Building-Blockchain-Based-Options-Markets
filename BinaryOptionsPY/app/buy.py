# ==== BUY A CONTRACT ====
from web3 import Web3
from compile import compile
from BO_status import BO_status
from fetch_abi import fetch_abi
from web3.exceptions import ContractLogicError, TransactionNotFound

# Function to buy a Binary Option contract
def buy(buyerAddress, buyerPrivateKey, deployerAddress, w3):
    try:
        # Fetch ABI for the CreateBO contract
        try:
            abi = fetch_abi('CreateBO')
        except Exception as e:
            print(f"[Error] Failed to load ABI: {e}")
            return

        # Create a contract instance
        try:
            contract = w3.eth.contract(address=deployerAddress, abi=abi)
        except Exception as e:
            print(f"[Error] Failed to create contract instance: {e}")
            return

        # Get the contract price
        try:
            price = contract.functions.contractPrice().call()
            price = int(price) / 1e18
        except Exception as e:
            print(f"[Error] Failed to retrieve contract price: {e}")
            return

        # Get nonce
        try:
            nonce = w3.eth.get_transaction_count(buyerAddress)
        except Exception as e:
            print(f"[Error] Failed to fetch nonce: {e}")
            return

        # Build the transaction
        try:
            tx_buy = contract.functions.buyContract().build_transaction({
                "from": buyerAddress,
                "gas": 3000000,
                "gasPrice": w3.to_wei("20", "gwei"),
                "nonce": nonce,
                "value": w3.to_wei(price, "ether")
            })
        except ContractLogicError as e:
            print(f"[Contract Error] Failed to build transaction: {e}")
            return
        except Exception as e:
            print(f"[Error] Unexpected error during transaction build: {e}")
            return

        # Sign the transaction
        try:
            signed_tx_buy = w3.eth.account.sign_transaction(tx_buy, private_key=buyerPrivateKey)
        except Exception as e:
            print(f"[Error] Failed to sign transaction: {e}")
            return

        # Send the transaction
        try:
            tx_hash = w3.eth.send_raw_transaction(signed_tx_buy.raw_transaction)
        except Exception as e:
            print(f"[Error] Failed to send transaction: {e}")
            return

        # Wait for transaction receipt
        try:
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            if receipt.status != 1:
                print("[Warning] Transaction reverted or failed.")
                return
        except TransactionNotFound:
            print("[Error] Transaction not found on the network.")
            return
        except Exception as e:
            print(f"[Error] Failed to confirm transaction: {e}")
            return

        # Show updated contract status
        try:
            BO_status(deployerAddress, abi, w3)
        except Exception as e:
            print(f"[Error] Could not fetch contract status: {e}")

    except Exception as e:
        print(f"[Fatal Error] Unexpected failure in buy(): {e}")
