from solcx import compile_standard, install_solc
import json
import os

# Compile all Solidity contracts in the 'contracts/' directory
# Returns: dict mapping contract names to [ABI, Bytecode]
def compile():
    contract_dir = "contracts/"  # Directory containing .sol files
    compiled_dir = "compiled_contracts/"  # Output directory for compiled results

    if not os.path.exists(compiled_dir):
        os.makedirs(compiled_dir)  # Create output directory if it doesn't exist

    sources = {}  # Dictionary to store source content of each contract

    # Load all Solidity (.sol) files into the sources dictionary
    for filename in os.listdir(contract_dir):
        if filename.endswith(".sol"):
            with open(os.path.join(contract_dir, filename), "r") as file:
                sources[filename] = {"content": file.read()}

    # Compile all contracts using Solidity compiler version 0.8.28
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": sources,
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "evm.bytecode"]  # Specify ABI and bytecode as output
                    }
                }
            },
        },
        solc_version="0.8.28",
    )

    # Save the full compilation output to a JSON file
    compiled_path = os.path.join(compiled_dir, "compiled_contracts.json")
    with open(compiled_path, "w") as file:
        json.dump(compiled_sol, file, indent=4)

    compiled_data = {}  # Dictionary to store ABI and Bytecode for each contract

    # Extract ABI and Bytecode from the compiled output
    for filename, contract_data in compiled_sol["contracts"].items():
        for contract_name, contract_info in contract_data.items():
            compiled_data[contract_name] = [
                contract_info["abi"],  # Contract ABI
                contract_info["evm"]["bytecode"]["object"]  # Contract bytecode
            ]

    return compiled_data  # Return ABI and Bytecode for each contract by name

