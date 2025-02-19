import json
import subprocess
import time
from web3 import Web3
from compile import compile
from deploy import deploy 
#==== PARAMETERISE AND DEPLOY CONTRACT ====

def create_contract(parameters, address, privateKey, w3):
    # Compile contracts 
    compiledData = compile()

    createContract = compiledData["CreateBO"]  
    
    # Deploy CreateBO with automatic ETH payment
    create_bo_address = deploy(parameters, createContract[0], createContract[1], address, privateKey, w3)

    return create_bo_address
