from solcx import compile_standard, install_solc
import json
import os


def compile():
    contract_dir = "contracts/"
    compiled_dir = "compiled_contracts/"

    if not os.path.exists(compiled_dir):
        os.makedirs(compiled_dir)  # Create directory if not exists

    # Store all contract sources
    sources = {}

    # Read all Solidity files from contracts/ directory
    for filename in os.listdir(contract_dir):
        if filename.endswith(".sol"):
            with open(os.path.join(contract_dir, filename), "r") as file:
                sources[filename] = {"content": file.read()}

    # Compile all contracts
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": sources,
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "evm.bytecode"]
                    }
                }
            },
        },
        solc_version="0.8.28",
    )

    # Save compiled contracts
    compiled_path = os.path.join(compiled_dir, "compiled_contracts.json")
    with open(compiled_path, "w") as file:
        json.dump(compiled_sol, file, indent=4)

    # Extract ABI and Bytecode dynamically
    compiled_data = {}  # Dictionary to store contract name as key and [ABI, Bytecode] as values

    for filename, contract_data in compiled_sol["contracts"].items():
        for contract_name, contract_info in contract_data.items():
            compiled_data[contract_name] = [  # Store ABI & Bytecode in a list
                contract_info["abi"],  # ABI
                contract_info["evm"]["bytecode"]["object"]  # Bytecode
            ]

    return compiled_data  # Return dictionary with contract names as keys
