import json
import subprocess
import time
from web3 import Web3
from compile import compile
from deploy import deploy
#==== PARAMETERISE AND DEPLOY CONTRACT ====

def create_contract(parameters, address, private_key, w3):
    # compile contract
    abi, bytecode = compile()

    # deploy contract
    contract_address = deploy(parameters, abi, bytecode, address, private_key)

    # Interact with deployed contract
    binary_option = w3.eth.contract(address=contract_address, abi=abi)

    print(f"Contract deployed at: {contract_address}")
    print(f"Strike Price: {binary_option.functions.strikePrice().call()}")
    print(f"Strike Date: {binary_option.functions.strikeDate().call()}")
    print(f"Payout: {binary_option.functions.payout().call()}")
    print(f"Expiry Price: {binary_option.functions.expiryPrice().call()}")
    print(f"Position: {binary_option.functions.position().call()}")
    print(f"Contract Price: {binary_option.functions.contractPrice().call()}")
    print(f"Creator: {binary_option.functions.creator().call()}")

    return binary_option, address