import json
import os

def fetch_abi(contractName):
    """
    Retrieves ABIs of all compiled contracts from the compiled JSON file.

    :param compiled_dir: The directory containing compiled contracts.
    :return: A dictionary where contract names are keys and ABIs are values.
    """
    compiled_dir="compiled_contracts/"
    compiled_path = os.path.join(compiled_dir, "compiled_contracts.json")

    # Check if the compiled file exists
    if not os.path.exists(compiled_path):
        raise FileNotFoundError(f"⚠ Compiled contracts file not found: {compiled_path}")

    # Load the compiled contracts JSON
    with open(compiled_path, "r") as file:
        compiled_data = json.load(file)

    contract_abis = {}

    # Extract ABIs from compiled data
    if "contracts" in compiled_data:
        for filename, contract_data in compiled_data["contracts"].items():
            for contract_name, contract_info in contract_data.items():
                if "abi" in contract_info:
                    contract_abis[contract_name] = contract_info["abi"]
                else:
                    print(f"⚠ ABI not found for {contract_name}")

    return contract_abis[contractName]  # Dictionary with contract names as keys and ABIs as values

