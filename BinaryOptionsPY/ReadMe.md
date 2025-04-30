# Building Blockchain-Based Options Markets

## Description

Implementation of the Ethereum based Binary Options market, described in [Report.pdf](./report.pdf).

---

## Installation

```bash
# Clone the repo
git clone <https://github.com/billy-hipps/Building-Blockchain-Based-Options-Markets>
cd <BinaryOptionsPY>
```

## Install dependencies

```bash
# Install required Python packages
pip install web3 eth-account streamlit pandas numpy yfinance py-solc-x requests
```

## 🛠 Install Node.js and Hardhat

To run a local Ethereum blockchain for testing, you need Node.js and Hardhat.

### 1. Install Node.js (via Homebrew on macOS)

```bash
# Install Node.js using Homebrew
brew install node

# Confirm installation
node -v
npm -v
```

```bash
# Install Hardhat locally
npm install --save-dev hardhat

# Set up Hardhat project (choose "Create a basic sample project")
npx hardhat
```

## 🚀 Steps to Use

1. **Start the local blockchain**  
   Open a terminal and run:  
   ```bash
   cd BinaryOptionsPY
   npx hardhat node
   ```

2. **Launch the application interface**  
   In a new terminal window, run the Streamlit frontend:  
   ```bash
   cd BinaryOptionsPY
   sudo streamlit run app/init.py
   ```

3. **Repeat step 2**  
   Open another terminal and run the same Streamlit command again to simulate a second user (e.g., one buyer and one creator).

---

## 🧠 Smart Contracts

- `BinaryOption.sol` – Core contract representing a single binary option with strike price, expiry, and payout logic.
- `CreateBO.sol` – Handles deployment of a `BinaryOption` contract and stores relevant configuration parameters.
- `Factory.sol` – Manages deployment of multiple `CreateBO` contracts and provides a registry of all created options.
- `TimeOracle.sol` – Off-chain oracle interface used to feed in time and price data for option expiry resolution.


---

## License

MIT License © [Durham University]
