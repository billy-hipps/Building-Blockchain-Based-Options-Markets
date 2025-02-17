import asyncio
import json
import logging
from web3 import AsyncWeb3
from web3.providers.persistent import WebSocketProvider
from eth_abi import decode

# Enable Debug Logging
LOG = True
if LOG:
    logger = logging.getLogger("web3.providers.WebSocketProvider")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())


async def log_events(contract_address, compiled_contract_path="compiled_contracts/comp_BO.json"):
    # Load compiled contract ABI from JSON
    with open(compiled_contract_path, "r") as file:
        compiled_contract = json.load(file)

    # Extract contract name dynamically
    contract_name = list(compiled_contract["contracts"].keys())[0]
    contract_abi = compiled_contract["contracts"][contract_name]["BinaryOption"]["abi"]

    # Initialize Web3 with Async WebSocket Provider
    async with AsyncWeb3(WebSocketProvider("ws://127.0.0.1:8545")) as w3:

        # Load contract dynamically
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)

        # Build event signature mappings
        event_map = {
            w3.keccak(text=f"{e['name']}({','.join(i['type'] for i in e['inputs'])})").hex(): e
            for e in contract.events._events
        }

        # Subscribe to logs (listens for ALL events)
        filter_params = {"address": contract_address}  # No specific topics → listens for all events
        subscription_id = await w3.eth.subscribe("logs", filter_params)
        print(f"🔹 Listening for ALL events on contract {contract_address} (Subscription ID: {subscription_id})")

        # Process events dynamically
        async for payload in w3.provider.iter_subscriptions():
            log = payload["result"]

            # Get event signature from topics
            event_signature = log["topics"][0]
            event_abi = event_map.get(event_signature)

            if not event_abi:
                print(f"⚠️ Unknown event detected: {log}")
                continue  # Skip unknown events

            # Decode indexed and non-indexed parameters dynamically
            indexed_inputs = [i for i in event_abi["inputs"] if i.get("indexed")]
            non_indexed_inputs = [i for i in event_abi["inputs"] if not i.get("indexed")]

            # Decode indexed parameters from topics
            decoded_indexed = [
                decode([inp["type"]], bytes.fromhex(log["topics"][i + 1][2:]))[0]
                for i, inp in enumerate(indexed_inputs)
            ]

            # Decode non-indexed parameters from data
            decoded_non_indexed = decode(
                [inp["type"] for inp in non_indexed_inputs], bytes.fromhex(log["data"][2:])
            )

            # Combine indexed and non-indexed parameters
            event_args = {
                inp["name"]: val for inp, val in zip(indexed_inputs + non_indexed_inputs, decoded_indexed + decoded_non_indexed)
            }

            # Print Event Data
            print(f"🔹 Event '{event_abi['name']}' detected: {event_args}")

            # Optional: Unsubscribe condition (e.g., contract termination)
            if "terminate" in event_abi["name"].lower():
                await w3.eth.unsubscribe(subscription_id)
                print(f"❌ Unsubscribed from contract events")
                break

        # Fetch latest block info after unsubscribing
        latest_block = await w3.eth.get_block("latest")
        print(f"🔹 Latest Block: {latest_block}")
