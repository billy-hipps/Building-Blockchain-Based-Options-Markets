from datetime import datetime
import time
from time import sleep
import requests
import asyncio

def fetch_time():
    return int(time.time())

# Function to schedule time updates
async def schedule(strikeDate, deployerAddress, privateKey, contractAddress, abi, w3):
    # every timestep call the timeUpdate function in the CreateBO contract
    timeIntervals = []

    startTime = fetch_time()

    offset = (strikeDate - startTime) % 5
    if offset > 0:
        timeIntervals.append(offset)

    intervalSize = (strikeDate - (startTime + offset)) / 5

    for i in range(1, 6):
        timeIntervals.append((startTime + offset) + (i * intervalSize))

    for timestamp in timeIntervals:
        await asyncio.sleep(timestamp - fetch_time())
        contract = w3.eth.contract(address=contractAddress, abi=abi)
        nonce = w3.eth.get_transaction_count(deployerAddress)

        tx = contract.functions.timeUpdate(int(timestamp)).build_transaction({
            "from": deployerAddress,
            "gas": 3000000,
            "gasPrice": w3.to_wei("20", "gwei"),
            "nonce": nonce
        })

        signed_tx = w3.eth.account.sign_transaction(tx, private_key=privateKey)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


    print("Contract has expired.")