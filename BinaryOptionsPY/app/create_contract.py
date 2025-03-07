import json
import subprocess
import time
from web3 import Web3
from compile import compile
from deploy import deploy 
#==== PARAMETERISE AND DEPLOY CONTRACT ====

def create_contract(factoryAddress, parameters, creatorAddress, privateKey, w3):
    # Compile contracts 
    compiledData = compile()

    factory = compiledData["Factory"]
    createBO = compiledData["CreateBO"]
    
    # Deploy CreateBO with automatic ETH payment
    create_bo_address = deploy(factoryAddress, parameters, factory[0], factory[1], createBO[0], creatorAddress, privateKey, w3)

    return create_bo_address
    