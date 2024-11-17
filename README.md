# Cryptocurrency Screener
This project is a cryptocurrency screener that scans for tokens on different exchanges and checks if they meet specific RSI (Relative Strength Index) conditions. Currently it applies the Slingshot strategy.

## Overview
The script allows users to select a broker, a cryptocurrency chain, a timeframe, and a lookback period. It then fetches OHLCV (Open, High, Low, Close, Volume) data, calculates RSI, and checks if the RSI conditions are met for each token. The results are displayed, and users can choose to perform another scan or exit.

## Features
- Support for multiple brokers (Binance, Bybit, etc.)
- Fetches tokens from different chains (Ethereum, Solana, etc.)
- Calculates RSI and checks conditions: recent touch of RSI 70 and currently in 40-60 RSI value.
- Handles keyboard interruption gracefully
- Detailed logging of the scanning process

# Setup

## Prerequisites
Ensure you have Python installed on your system. You can download it from python.org.

## File Structure
The project consists of the following files:
- ```main.py```: Main script to orchestrate the entire process.
- ```broker.py```: Handles broker-specific operations.
- ```chain.py```: Manages chain-related operations.
- ```rsi.py```: Contains RSI calculation and condition checking.
- ```token_list.py```: Fetches and filters tokens from exchanges.
- ```ohlcv.py```: Fetches OHLCV data.

## Running the Script
Ensure Dependencies: Make sure the required libraries (ccxt, requests, pandas, ta, logging) are installed. You can install them using the provided pip command.

## Install Dependencies
1. Create a virtual environment:

```
bash
python -m venv myenv
source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
```

2. Create a requirements.txt file with the following content:

```
ccxt
requests
pandas
ta
logging
```
3. Install the required libraries:
```
bash
pip install -r requirements.txt
```

## Running the Script
1. Ensure Dependencies: Make sure the required libraries are installed using the requirements.txt file.

2. Run the Script:
```
bash
python main.py
```

3. Follow the Prompts:
- Select a broker from the list of supported brokers.
- Select a cryptocurrency chain from the list of top chains.
- Choose a timeframe for the OHLCV data (e.g., 15 minutes, 1 hour).
- Enter the lookback period (number of candles).
- The script will scan the tokens, calculate the RSI, and display tokens that meet the criteria.

4. Handle Keyboard Interruptions:
- If you need to interrupt the scanning process, press Ctrl + C.
- The script will display the tokens that met the criteria before the interruption.

5. Perform Another Scan or Exit:
- After the scanning process is complete, you'll be prompted to perform another scan or exit.
- Follow the prompts to continue scanning or exit the script.

## Logging
The script uses a custom logging format to provide detailed information about the scanning process, including the start time, end time, total number of symbols, and progress through the tokens being scanned.
