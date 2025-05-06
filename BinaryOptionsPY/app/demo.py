import random
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

from create_contract import create_contract
from create_factory import create_factory
from stock_data import get_price

# --- Configuration ---

network = "http://127.0.0.1:8545"


ACCOUNT = {
    "address": "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266",
    "private_key": "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
}

# --- Random Parameter Generation ---

def generate_random_parameters():
    tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]
    positions = [True, False]
    prices = [10, 15, 20, 25, 30]
    payouts = [100, 150, 200, 250, 300]

    return {
        "ticker": random.choice(tickers),
        "current_price": None,
        "position": random.choice(positions),
        "contract_price": random.choice(prices),
        "payout": random.choice(payouts),
        "strike_date": 600
    }

# --- Deployment Logic ---

def main():
    # Initialize Web3
    w3 = Web3(Web3.HTTPProvider(network))
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

    # Deploy factory (or replace with a known factory address if already deployed)
    factory_address = Web3.to_checksum_address("0x5fbdb2315678afecb367f032d93f642f64180aa3")

    # Generate random parameters for the CreateBO contract
    parameters = generate_random_parameters()
    ticker = parameters["ticker"]
    current_price = get_price(ticker)
    parameters["current_price"] = current_price
    print(f"🚀 Deploying contract with parameters: {parameters}")

    try:
        contract_address = create_contract(
            factory_address,
            parameters,
            ACCOUNT["address"],
            ACCOUNT["private_key"],
            w3
        )
        print(f"✅ Contract deployed at address: {contract_address}")
    except Exception as e:
        print(f"❌ Deployment failed: {e}")

if __name__ == "__main__":
    main()


