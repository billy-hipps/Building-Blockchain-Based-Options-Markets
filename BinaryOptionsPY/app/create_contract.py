import json
import subprocess
import time
from web3 import Web3
from compile import compile
from deploy import deploy 
#==== PARAMETERISE AND DEPLOY CONTRACT ====

def create_contract(parameters, address, private_key, w3):
    # Compile contracts 
    compiled_data = compile()

    createContract = compiled_data["CreateBO"]
    BinaryOption = compiled_data["BinaryOption"]   
    buyContract = compiled_data["Buy"]
    
    # Deploy CreateBO with automatic ETH payment
    create_bo_address, binary_option_address = deploy(parameters, createContract[0], createContract[1], address, private_key, w3)

    return create_bo_address, binary_option_address
