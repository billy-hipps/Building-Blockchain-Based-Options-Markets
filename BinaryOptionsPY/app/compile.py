from solcx import compile_standard, install_solc
import json

# Install Solidity compiler version (match your contract's pragma)
install_solc("0.8.28")

def compile():
    # Read the Solidity contract
    with open("contracts/BinaryOption.sol", "r") as file:
        contract_source_code = file.read()

    # Compile the contract
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"BinaryOption.sol": {"content": contract_source_code}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                    }
                }
            },
        },
        solc_version="0.8.28",
    )

    # Save compiled contract to JSON file
    with open("compiled_contract.json", "w") as file:
        json.dump(compiled_sol, file)

    # Extract ABI and Bytecode
    abi = compiled_sol["contracts"]["BinaryOption.sol"]["BinaryOption"]["abi"]
    bytecode = compiled_sol["contracts"]["BinaryOption.sol"]["BinaryOption"]["evm"]["bytecode"]["object"]

    print("Contract Compiled Successfully!")

    return abi, bytecode