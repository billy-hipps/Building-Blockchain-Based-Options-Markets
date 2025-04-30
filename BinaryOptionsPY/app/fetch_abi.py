import json
import os

# Fetch the ABI for a specified compiled contract
# Parameters:
# - contractName: string, name of the contract to retrieve ABI for
# Returns:
# - list: ABI of the specified contract
def fetch_abi(contractName):
    compiled_dir = "compiled_contracts/"  # Directory containing compiled contracts
    compiled_path = os.path.join(compiled_dir, "compiled_contracts.json")  # Full path to compiled JSON

    # Check if the compiled contracts file exists
    if not os.path.exists(compiled_path):
        raise FileNotFoundError(f"⚠ Compiled contracts file not found: {compiled_path}")

    # Load compiled contract data
    with open(compiled_path, "r") as file:
        compiled_data = json.load(file)

    contract_abis = {}  # Dictionary to hold contract name → ABI mapping

    # Traverse compiled data and extract ABIs
    if "contracts" in compiled_data:
        for filename, contract_data in compiled_data["contracts"].items():
            for contract_name, contract_info in contract_data.items():
                if "abi" in contract_info:
                    contract_abis[contract_name] = contract_info["abi"]  # Store ABI
                else:
                    print(f"⚠ ABI not found for {contract_name}")

    return contract_abis[contractName]  # Return ABI for the requested contract

