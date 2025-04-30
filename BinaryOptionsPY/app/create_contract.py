import json
import subprocess
import time
from web3 import Web3
from compile import compile  # Function to compile Solidity contracts
from deploy import deploy  # Function to deploy the CreateBO contract


# Deploys a CreateBO contract using a Factory contract
# Parameters:
# - factoryAddress: string, address of the deployed Factory contract
# - parameters: dict, constructor parameters for CreateBO contract
# - creatorAddress: string, Ethereum address initiating the deployment
# - privateKey: string, private key for signing deployment transaction
# - w3: Web3 instance, used to interact with the Ethereum blockchain
# Returns:
# - create_bo_address: string, address of the deployed CreateBO contract
def create_contract(factoryAddress, parameters, creatorAddress, privateKey, w3):
    # Compile all contracts and retrieve their ABIs and bytecode
    compiledData = compile()

    factory = compiledData["Factory"]   # [ABI, Bytecode] for Factory contract
    createBO = compiledData["CreateBO"] # [ABI, Bytecode] for CreateBO contract
    
    # Deploy CreateBO contract via the Factory using provided parameters
    create_bo_address = deploy(
        factoryAddress,      # Factory contract address
        parameters,          # Constructor arguments for CreateBO
        factory[0],          # Factory ABI
        factory[1],          # Factory Bytecode
        createBO[0],         # CreateBO ABI
        creatorAddress,      # Address deploying the CreateBO contract
        privateKey,          # Private key of the deployer
        w3                   # Web3 instance
    )

    return create_bo_address  # Return deployed CreateBO contract address
