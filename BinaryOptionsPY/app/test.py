from datetime import datetime
import json
import pandas as pd
import numpy as np
import os
import time
import asyncio

from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from eth_utils import to_bytes, to_hex

from compile import compile  # Custom compile function
from stock_data import get_price  # Fetch live asset price

# ==== Utility ====
# Get current UNIX timestamp
def fetch_time():
    return int(time.time())

# ==== Initialize Benchmark Table ====
# Track function name, caller role, gas used, and execution time
data = pd.DataFrame({
    'Function': ['Deploy Factory', 'Create and Deploy', 'Buy', 'Time Update'],
    'Contract': ['Factory', 'Factory', 'CreateBO', 'Factory'],
    'Caller': ['Admin', 'Creator', 'Buyer', 'Both'],
    'Gas Used': [None]*4,
    'Timestamp': [None]*4
})

# ==== Ethereum Test Accounts ====
admin_acct = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
admin_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

creator_acct = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"
creator_key = "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d"

buyer_acct = "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC"
buyer_key = "0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a"

# ==== Web3 Setup ====
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

compiledData = compile()
factory_abi = compiledData["Factory"][0]
factory_bytecode = compiledData["Factory"][1]
createbo_abi = compiledData["CreateBO"][0]

# ==== Deploy Factory Contract ====
factory = w3.eth.contract(abi=factory_abi, bytecode=factory_bytecode)
nonce = w3.eth.get_transaction_count(admin_acct)

start = time.time()
tx = factory.constructor().build_transaction({
    "from": admin_acct,
    "gas": 30000000,
    "gasPrice": w3.to_wei("20", "gwei"),
    "nonce": nonce
})
signed_tx = w3.eth.account.sign_transaction(tx, private_key=admin_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
end = time.time()

data.loc[data['Function'] == 'Deploy Factory', 'Gas Used'] = float(receipt.gasUsed)
data.loc[data['Function'] == 'Deploy Factory', 'Timestamp'] = round(end - start, 4)

factory_address = receipt.contractAddress
factory = w3.eth.contract(address=factory_address, abi=factory_abi)

# ==== Create and Deploy CreateBO Contract ====
parameters = {
    'ticker': 'AAPL',
    'strike_price': 220,
    'strike_date': 120,  # seconds from now
    'contract_price': 10,  # in ETH
    'payout': 20,  # in ETH
    'position': True  # True = Long
}

strikeDate = fetch_time() + parameters['strike_date']
payout_in_wei = w3.to_wei(parameters['payout'], "ether")
contract_price_in_wei = w3.to_wei(parameters['contract_price'], "ether")
ticker_bytes = to_bytes(text=parameters['ticker'].ljust(32))

nonce = w3.eth.get_transaction_count(creator_acct)

start = time.time()
gas_estimate = factory.functions.CreateAndDeploy(
    to_hex(ticker_bytes),
    parameters['strike_price'],
    strikeDate,
    payout_in_wei,
    parameters['position'],
    contract_price_in_wei
).estimate_gas({"from": creator_acct, "value": payout_in_wei})

tx = factory.functions.CreateAndDeploy(
    to_hex(ticker_bytes),
    parameters['strike_price'],
    strikeDate,
    payout_in_wei,
    parameters['position'],
    contract_price_in_wei
).build_transaction({
    "from": creator_acct,
    "gas": gas_estimate + 50000,
    "gasPrice": w3.to_wei("20", "gwei"),
    "nonce": nonce,
    "value": payout_in_wei
})
signed_tx = w3.eth.account.sign_transaction(tx, private_key=creator_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
end = time.time()

create_bo_address = receipt.logs[0]["address"] if receipt.logs else None
if create_bo_address is None:
    raise Exception("CreateBO deployment failed: no address in logs.")

data.loc[data['Function'] == 'Create and Deploy', 'Gas Used'] = float(receipt.gasUsed)
data.loc[data['Function'] == 'Create and Deploy', 'Timestamp'] = round(end - start, 4)

# ==== Buy the Contract ====
CreateBO = w3.eth.contract(address=create_bo_address, abi=createbo_abi)
price = CreateBO.functions.contractPrice().call()

nonce = w3.eth.get_transaction_count(buyer_acct)

start = time.time()
tx = CreateBO.functions.buyContract().build_transaction({
    "from": buyer_acct,
    "gas": 3000000,
    "gasPrice": w3.to_wei("20", "gwei"),
    "nonce": nonce,
    "value": price
})
signed_tx = w3.eth.account.sign_transaction(tx, private_key=buyer_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
end = time.time()

data.loc[data['Function'] == 'Buy', 'Gas Used'] = float(receipt.gasUsed)
data.loc[data['Function'] == 'Buy', 'Timestamp'] = round(end - start, 4)

# ==== Schedule Time Updates (5 updates) ====
async def schedule(ticker, strikeDate, deployerAddress, privateKey, contractAddress, abi, w3):
    timeIntervals = []
    startTime = fetch_time()

    offset = (strikeDate - startTime) % 5
    if offset > 0:
        timeIntervals.append(offset)

    intervalSize = (strikeDate - (startTime + offset)) / 5
    for i in range(1, 6):
        timeIntervals.append((startTime + offset) + (i * intervalSize))

    total_time = 0.0
    total_gas = 0.0

    for timestamp in timeIntervals:
        await asyncio.sleep(timestamp - fetch_time())
        newPrice = get_price(ticker)
        contract = w3.eth.contract(address=contractAddress, abi=abi)
        nonce = w3.eth.get_transaction_count(deployerAddress)

        start_time = time.time()
        tx = contract.functions.timeUpdate(int(timestamp), newPrice).build_transaction({
            "from": deployerAddress,
            "gas": 3000000,
            "gasPrice": w3.to_wei("20", "gwei"),
            "nonce": nonce
        })
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=privateKey)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        end_time = time.time()

        total_time += end_time - start_time
        total_gas += receipt.gasUsed

    data.loc[data['Function'] == 'Time Update', 'Gas Used'] = float(total_gas)
    data.loc[data['Function'] == 'Time Update', 'Timestamp'] = round(total_time, 4)

# ==== Run Scheduler ====
asyncio.run(schedule(parameters['ticker'], strikeDate, creator_acct, creator_key, create_bo_address, createbo_abi, w3))

# ==== Save Results ====
data.to_csv("transaction_summary.csv", index=False)  # Save gas and timing data to CSV
