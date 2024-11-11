import ccxt
import pandas as pd
import ta
import time
import re
import requests
import argparse
import logging
from datetime import datetime


# def configure_logging(debug):
#     if debug:
#         logging.basicConfig(level=logging.DEBUG,
#                             format='%(asctime)s - %(levelname)s - %(message)s')
#     else:
#         logging.basicConfig(level=logging.INFO,
#                             format='%(asctime)s - %(message)s')
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def fetch_solana_tokens_from_registry():
    """Fetches the list of Solana ecosystem tokens from the Solana token registry"""
    response = requests.get(
        "https://raw.githubusercontent.com/solana-labs/token-list/main/src/tokens/solana.tokenlist.json")
    data = response.json()
    return data['tokens']


def categorize_tokens(tokens):
    categories = {
        'All': [],
        'Stablecoins': [],
        'Ethereum': [],
        'DeFi': [],
        'Utility': [],
        'Community': [],
        'Meme': [],
        'NFTs': [],
        'Wormhole': [],
        'Games': [],
        'LP-Token': [],
        'Wrapped': [],
        'Leverage': [],
        'Security': [],
        'Stocks': [],
        'Currency': [],
        'Others': []
    }

    for token in tokens:
        if token['chainId'] == 101:
            symbol = token['symbol'] + '/USDT'
            tags = ','.join(token.get('tags', [])).lower()

            categories['All'].append(symbol)

            if 'stable' in tags:
                categories['Stablecoins'].append(symbol)
            elif 'ethereum' in tags:
                categories['Ethereum'].append(symbol)
            elif 'defi' in tags:
                categories['DeFi'].append(symbol)
            elif 'utility' in tags:
                categories['Utility'].append(symbol)
            elif 'community' in tags:
                categories['Community'].append(symbol)
            elif 'meme' in tags:
                categories['Meme'].append(symbol)
            elif 'nft' in tags:
                categories['NFTs'].append(symbol)
            elif 'wormhole' in tags:
                categories['Wormhole'].append(symbol)
            elif 'game' in tags:
                categories['Games'].append(symbol)
            elif 'lp-token' in tags:
                categories['LP-Token'].append(symbol)
            elif 'wrapped' in tags:
                categories['Wrapped'].append(symbol)
            elif 'leverage' in tags:
                categories['Leverage'].append(symbol)
            elif 'security' in tags:
                categories['Security'].append(symbol)
            elif 'stocks' in tags:
                categories['Stocks'].append(symbol)
            elif 'currency' in tags:
                categories['Currency'].append(symbol)
            else:
                categories['Others'].append(symbol)

    return categories


def fetch_ohlcv(symbol, timeframe):
    """Fetches OHLCV data for a given symbol and timeframe"""
    logging.info(
        f"Fetching OHLCV data for {symbol} with timeframe {timeframe}")
    exchange = ccxt.bybit()

    try:
        data = exchange.fetch_ohlcv(symbol, timeframe)
        df = pd.DataFrame(
            data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        return df
    except ccxt.BaseError as e:
        logging.error(f"Error fetching OHLCV data for {symbol}: {e}")
        return None


def calculate_rsi(df, period=14):
    """Calculates RSI for a given DataFrame"""
    if df is None:
        logging.error("Cannot calculate RSI because the DataFrame is None")
        return None

    try:
        df['rsi'] = ta.momentum.rsi(df['close'], window=period)
        return df
    except Exception as e:
        logging.error(f"Error calculating RSI: {e}")
        return None


def check_rsi_conditions(symbol, timeframe, recent_period=10):
    """Checks if the RSI conditions are met for a given symbol and timeframe"""
    df = fetch_ohlcv(symbol, timeframe)
    df = calculate_rsi(df)

    if df is None:
        return False, None

    recent_rsi_touch = (df.tail(recent_period)['rsi'] >= 70).any()
    current_rsi = df.iloc[-1]['rsi']

    if recent_rsi_touch and 40 < current_rsi < 60:
        return True, current_rsi
    return False, current_rsi


def fetch_solana_tokens(exchange, category, tokens_registry):
    """Fetches the list of Solana ecosystem tokens from Bybit based on category"""
    markets = exchange.fetch_markets()

    # Save the symbols to a file
    # with open('symbols_usdt.txt', 'w') as f:
    #     for symbol in usdt_tokens:
    #         f.write(f"{symbol}\n")
    # logging.info(f"USDT Symbols have been saved to symbols_usdt.txt")

    solana_tokens = [market['symbol']
                     for market in markets if market['symbol'] in tokens_registry[category]]
    # Exclude symbols matching the pattern ending in "-C" or "-P"
    excluded_pattern = re.compile(r'.*-.*-.*-[CP]$')
    solana_tokens = [
        symbol for symbol in solana_tokens if not excluded_pattern.search(symbol)]
    return solana_tokens


def main():
    # configure_logging(debug)
    logging.info("Script started")
    start_time = datetime.now()

    exchange = ccxt.bybit()
    solana_tokens_from_registry = fetch_solana_tokens_from_registry()
    categorized_tokens = categorize_tokens(solana_tokens_from_registry)

    while True:
        timeframes = ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w']
        for idx, timeframe in enumerate(timeframes):
            print(f"{idx + 1}. {timeframe}")
        print(f"{len(timeframes) + 1}. Exit")

        selected_idx = int(
            input("Select Timeframe: ")) - 1

        if selected_idx == len(timeframe):
            break

        timeframe = timeframes[selected_idx]

        # Adjust the number of recent periods to check for RSI touch
        recent_period = int(input(
            "Input how many candles to lookback/recent period: "))

        print("\nSelect a category to scan or 'Exit' to quit:")
        for idx, category in enumerate(categorized_tokens.keys()):
            print(f"{idx + 1}. {category}")
        print(f"{len(categorized_tokens) + 1}. Exit")

        selected_idx = int(
            input("Enter the number of the category you want to scan: ")) - 1

        if selected_idx == len(categorized_tokens):
            break

        category = list(categorized_tokens.keys())[selected_idx]

        symbols = fetch_solana_tokens(exchange, category, categorized_tokens)

        results = []
        total_symbols = len(symbols)

        logging.info(f"Total Symbols in {category}: {total_symbols}")

        try:
            for i, symbol in enumerate(symbols):
                logging.info(
                    f"Processing {symbol} ({i + 1}/{total_symbols})...")
                meets_conditions, current_rsi = check_rsi_conditions(
                    symbol, timeframe, recent_period)
                if meets_conditions:
                    results.append((symbol, current_rsi))

                # Avoid hitting API rate limits
                time.sleep(1)
        except KeyboardInterrupt:
            logging.warning("Script interrupted by user.")
        finally:
            if results:
                logging.info("Tokens that meet the RSI conditions:")
                for result in results:
                    logging.info(
                        f"Symbol: {result[0]}, Current RSI: {result[1]}")
            else:
                logging.info(
                    "No tokens meet the RSI conditions at this time.")

        end_time = datetime.now()
        logging.info(f"Script finished scanning {category} category.")
        logging.info(f"Total running time: {end_time - start_time}")

        if input("Scan another category? Y/N: ").lower() == 'y':
            continue
        else:
            break


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(
    #     description="Analyze Solana ecosystem tokens based on RSI conditions.")
    # parser.add_argument("--timeframe", type=str, default="1h",
    #                     help="Timeframe for fetching OHLCV data (e.g., '1h', '4h', '1d')")
    # parser.add_argument("--debug", action="store_true",
    #                     help="Enable debug mode")
    # args = parser.parse_args()

    # logging.info(f"Timeframe argument received: {args.timeframe}")

    # main(args.timeframe, args.debug)
    # main(args.timeframe)
    main()
