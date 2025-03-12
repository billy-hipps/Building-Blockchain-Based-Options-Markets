from web3 import Web3
from BO_status import BO_status
from schedule import fetch_time, schedule
from eth_utils import to_bytes, to_hex
import asyncio


def deploy(factoryAddress, parameters, factory_abi, factory_bytecode, createBO_abi, creatorAddress, privateKey, w3):

    factory = w3.eth.contract(address=factoryAddress, abi=factory_abi)

    nonce = w3.eth.get_transaction_count(creatorAddress)

    strikeDate = fetch_time() + parameters['strike_date']

    payout_in_wei = w3.to_wei(parameters['payout'], "ether")

    # Estimate gas to avoid out-of-gas errors
    gas_estimate = factory.functions.CreateAndDeploy(
        to_hex(to_bytes(text=parameters['ticker'].ljust(32))),
        parameters['strike_price'],
        strikeDate,
        payout_in_wei,
        parameters['position'],
        w3.to_wei(parameters['contract_price'], "ether")
    ).estimate_gas({"from": creatorAddress, "value": payout_in_wei})

    # Build transaction
    tx = factory.functions.CreateAndDeploy(
        to_hex(to_bytes(text=parameters['ticker'].ljust(32))),
        parameters['strike_price'],
        strikeDate,
        payout_in_wei,
        parameters['position'],
        w3.to_wei(parameters['contract_price'], "ether")
    ).build_transaction({
        "from": creatorAddress,
        "gas": gas_estimate + 50000,  # Add buffer
        "gasPrice": w3.to_wei("20", "gwei"),
        "nonce": nonce,
        "value": payout_in_wei
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=privateKey)

    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # FIX: Get contract address from logs instead of `contractAddress`
    if len(tx_receipt.logs) > 0:
        create_bo_address = tx_receipt.logs[0]["address"]
        print(f"CreateBO Contract Deployed at: {create_bo_address}")
    else:
        print("⚠ No contract address found in logs. Possible transaction failure.")
        return None

    BO_status(create_bo_address, createBO_abi, w3)

    # Ensure event loop works correctly
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(schedule(strikeDate, creatorAddress, privateKey, create_bo_address, createBO_abi, w3))
    else:
        asyncio.run(schedule(parameters['ticker'], strikeDate, creatorAddress, privateKey, create_bo_address, createBO_abi, w3))

    return create_bo_address
