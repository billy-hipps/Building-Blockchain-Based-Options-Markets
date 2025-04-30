from web3 import Web3
from BO_status import BO_status
from stock_data import get_price
from schedule import fetch_time, schedule
from eth_utils import to_bytes, to_hex
import asyncio

# Deploy a CreateBO contract via Factory and schedule its strike event
# Parameters:
# - factoryAddress: string, address of the deployed Factory contract
# - parameters: dict, includes ticker, strike_date offset, payout, position, contract_price
# - factory_abi: list, ABI of the Factory contract
# - factory_bytecode: string, bytecode of the Factory contract (unused in this function)
# - createBO_abi: list, ABI of the CreateBO contract
# - creatorAddress: string, Ethereum address deploying the contract
# - privateKey: string, private key of the deployer
# - w3: Web3 instance, used to interact with Ethereum
# Returns:
# - create_bo_address: string, address of the deployed CreateBO contract
def deploy(factoryAddress, parameters, factory_abi, factory_bytecode, createBO_abi, creatorAddress, privateKey, w3):
    factory = w3.eth.contract(address=factoryAddress, abi=factory_abi)  # Instantiate Factory contract

    nonce = w3.eth.get_transaction_count(creatorAddress)  # Get nonce for deployer

    strikeDate = fetch_time() + parameters['strike_date']  # Calculate future strike timestamp

    parameters['strike_price'] = get_price(parameters['ticker'])  # Fetch real-time stock price

    payout_in_wei = w3.to_wei(parameters['payout'], "ether")  # Convert payout to wei

    # Estimate gas for deployment to avoid failure
    gas_estimate = factory.functions.CreateAndDeploy(
        to_hex(to_bytes(text=parameters['ticker'].ljust(32))),  # Pad ticker to 32 bytes
        parameters['strike_price'],
        strikeDate,
        payout_in_wei,
        parameters['position'],
        w3.to_wei(parameters['contract_price'], "ether")
    ).estimate_gas({"from": creatorAddress, "value": payout_in_wei})

    # Build the deployment transaction
    tx = factory.functions.CreateAndDeploy(
        to_hex(to_bytes(text=parameters['ticker'].ljust(32))),
        parameters['strike_price'],
        strikeDate,
        payout_in_wei,
        parameters['position'],
        w3.to_wei(parameters['contract_price'], "ether")
    ).build_transaction({
        "from": creatorAddress,
        "gas": gas_estimate + 50000,  # Add buffer to gas limit
        "gasPrice": w3.to_wei("20", "gwei"),  # Set gas price
        "nonce": nonce,
        "value": payout_in_wei  # Attach ETH payout value
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=privateKey)  # Sign the transaction

    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)  # Send the transaction

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)  # Wait for confirmation

    # Extract deployed contract address from logs
    if len(tx_receipt.logs) > 0:
        create_bo_address = tx_receipt.logs[0]["address"]
        print(f"CreateBO Contract Deployed")
    else:
        print("⚠ No contract address found in logs. Possible transaction failure.")
        return None

    # Print the status of the newly deployed CreateBO contract
    BO_status(create_bo_address, createBO_abi, w3)

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(schedule(
            parameters['ticker'],
            strikeDate,
            creatorAddress,
            privateKey,
            create_bo_address,
            createBO_abi,
            w3
        ))
    except Exception as e:
        print(f"[Error] Schedule coroutine failed: {e}")


    return create_bo_address  # Return address of deployed CreateBO contract

