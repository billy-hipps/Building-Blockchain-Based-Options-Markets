from compile import compile
from deploy_factory import deploy_factory

# Deploys the Factory contract to the blockchain
# Parameters:
# - address: string, Admin's Ethereum address used to deploy the contract
# - privateKey: string, private key for signing the deployment transaction
# - w3: Web3 instance, used to interact with the Ethereum blockchain
# Returns:
# - factory_address: string, deployed Factory contract address
def create_factory(address, privateKey, w3):
    # Compile contracts and extract ABI and Bytecode
    compiledData = compile()

    factory = compiledData["Factory"]  # [ABI, Bytecode] for Factory contract
    
    # Deploy Factory contract and return its address
    factory_address = deploy_factory(
        factory[0],  # Factory ABI
        factory[1],  # Factory Bytecode
        address,     # Deployer's Ethereum address
        privateKey,  # Deployer's private key
        w3           # Web3 instance
    )

    return factory_address 
