# Building Blockchain-Based Options Markets

## Description

Implementation of the Ethereum based Binary Options market, described in [Report.pdf](/BinaryOptionsPY/Report.pdf).

### Executive Summary

This project delivers a decentralised binary options trading platform designed to eliminate the broker-driven fraud historically associated with retail binary options markets. Traditional brokers have been known to deny payouts or close accounts arbitrarily, creating significant counterparty risk and undermining market integrity. By using blockchain and smart contracts to automate trade execution and settlement, this platform enforces trustless payouts and immutable contract logic, removing the need for intermediaries and ensuring trade outcomes cannot be manipulated. 

Report

The system was built and tested on Ethereum, featuring a suite of Solidity smart contracts, a Factory-based deployment architecture, and secure oracles for time and asset pricing. Comprehensive access controls and security measures ensure that roles, payouts, and oracle data cannot be tampered with. Testing confirmed strong protection against adversarial behaviours, while static analysis validated secure contract design. 

Report

Cost analysis showed that buyers face highly competitive fees—consistently below 0.1% for typical retail trade sizes between $100 and $2,000—comparable to or cheaper than traditional exchanges. Although sellers incur higher gas costs due to contract deployment overhead, the premium is offset by the complete removal of counterparty risk. Performance results also highlight sensitivity to Ethereum network congestion and the benefits of using a dollar-pegged stablecoin in future iterations to improve price predictability. 

Report

The research further outlines a path to expand functionality through automated margining, enabling dynamic risk management and improved capital efficiency while retaining trustless settlement. 

Report

Overall, the findings demonstrate that blockchain offers a commercially viable and security-enhancing alternative for retail derivatives trading. The platform provides fair, transparent, and resilient execution, illustrating the broader potential of decentralised financial infrastructure to reshape markets that depend on trust.

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
