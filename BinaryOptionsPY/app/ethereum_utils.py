from web3 import Web3


def is_valid_address(address: str) -> bool:
    """
    Check whether the given string is a valid Ethereum address.
    """
    if not isinstance(address, str):
        return False
    return Web3.is_address(address)


def to_checksum(address: str) -> str:
    """
    Convert an address to its EIP-55 checksum format.
    Raises ValueError if the input is invalid.
    """
    if not is_valid_address(address):
        raise ValueError(f"Invalid Ethereum address: {address}")
    return Web3.to_checksum_address(address)


def safe_to_checksum(address: str) -> str:
    """
    Convert to checksum address or return None if invalid.
    """
    try:
        return to_checksum(address)
    except ValueError:
        return None
