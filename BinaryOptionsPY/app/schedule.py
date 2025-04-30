from datetime import datetime
import time
from time import sleep
import requests
import asyncio

from stock_data import get_price  # Fetch live asset price

# Returns current UNIX timestamp
def fetch_time():
    return int(time.time())

# Schedule periodic time updates to the CreateBO contract
# Parameters:
# - ticker: string, asset symbol (e.g., "AAPL")
# - strikeDate: int, UNIX timestamp when the contract ends
# - deployerAddress: string, address authorized to send updates
# - privateKey: string, private key of the deployer
# - contractAddress: string, address of the deployed CreateBO contract
# - abi: list, ABI of the CreateBO contract
# - w3: Web3 instance
async def schedule(ticker, strikeDate, deployerAddress, privateKey, create_bo_address, create_bo_abi, w3):
    # Determine time intervals for updates (5 updates before strike)
    timeIntervals = []
    startTime = fetch_time()

    offset = (strikeDate - startTime) % 5
    if offset > 0:
        timeIntervals.append(offset)

    intervalSize = (strikeDate - (startTime + offset)) / 5

    for i in range(1, 6):
        timeIntervals.append((startTime + offset) + (i * intervalSize))

    # Send price updates at scheduled intervals
    for timestamp in timeIntervals:
        await asyncio.sleep(timestamp - fetch_time())  # Wait until target time
        newPrice = get_price(ticker)  # Fetch latest price

        contract = w3.eth.contract(address=create_bo_address, abi=create_bo_abi)  # Load contract instance
        nonce = w3.eth.get_transaction_count(deployerAddress)

        # Build transaction to call timeUpdate()
        tx = contract.functions.timeUpdate(int(timestamp), newPrice).build_transaction({
            "from": deployerAddress,
            "gas": 3000000,
            "gasPrice": w3.to_wei("20", "gwei"),
            "nonce": nonce
        })

        # Sign and send the transaction
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=privateKey)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print("Contract has expired.")  # Final log after strike time is reached
