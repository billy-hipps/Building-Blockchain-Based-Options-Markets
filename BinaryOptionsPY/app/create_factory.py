from compile import compile
from deploy_factory import deploy_factory


def create_factory(address, privateKey, w3):
    # Compile contracts 
    compiledData = compile()

    factory = compiledData["Factory"]  
    
    # Deploy CreateBO with automatic ETH payment
    factory_address = deploy_factory(factory[0], factory[1], address, privateKey, w3)

    return factory_address