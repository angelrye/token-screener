import ccxt
import pandas as pd
import ta
import time
import re
import requests
import argparse
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def fetch_solana_tokens_from_registry():
    """Fetches the list of Solana ecosystem tokens from the Solana token registry"""
    response = requests.get(
        "https://raw.githubusercontent.com/solana-labs/token-list/main/src/tokens/solana.tokenlist.json")
    data = response.json()
    tokens = [token['symbol'] + '/USDT' for token in data['tokens']
              if token['chainId'] == 101]
    return tokens


def fetch_ohlcv(symbol, timeframe):
    """Fetches OHLCV data for a given symbol and timeframe"""
    logging.info(
        f"Fetching OHLCV data for {symbol} with timeframe {timeframe}")
    exchange = ccxt.bybit()
    data = exchange.fetch_ohlcv(symbol, timeframe)
    df = pd.DataFrame(
        data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    return df


def calculate_rsi(df, period=14):
    """Calculates RSI for a given DataFrame"""
    df['rsi'] = ta.momentum.rsi(df['close'], window=period)
    return df


def check_rsi_conditions(symbol, timeframe, recent_period=10):
    """Checks if the RSI conditions are met for a given symbol and timeframe"""
    df = fetch_ohlcv(symbol, timeframe)
    df = calculate_rsi(df)

    recent_rsi_touch = (df.tail(recent_period)['rsi'] >= 70).any()
    current_rsi = df.iloc[-1]['rsi']

    if recent_rsi_touch and 40 < current_rsi < 60:
        return True, current_rsi
    return False, current_rsi


def fetch_solana_tokens(exchange):
    """Fetches the list of Solana ecosystem tokens from Bybit"""
    markets = exchange.fetch_markets()
    solana_tokens_from_registry = fetch_solana_tokens_from_registry()
    solana_tokens = [market['symbol']
                     for market in markets if market['symbol'] in solana_tokens_from_registry]
    # Exclude symbols matching the pattern ending in "-C" or "-P"
    excluded_pattern = re.compile(r'.*-.*-.*-[CP]$')
    solana_tokens = [
        symbol for symbol in solana_tokens if not excluded_pattern.search(symbol)]
    return solana_tokens


def main(timeframe):
    logging.info("Script started")
    start_time = datetime.now()

    exchange = ccxt.bybit()
    symbols = fetch_solana_tokens(exchange)
    recent_period = 10  # Adjust the number of recent periods to check for RSI touch

    results = []
    total_symbols = len(symbols)

    logging.info(f"Total SOLANA Symbols: {total_symbols}")

    try:
        for i, symbol in enumerate(symbols):
            logging.info(f"Processing {symbol} ({i + 1}/{total_symbols})...")
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
                logging.info(f"Symbol: {result[0]}, Current RSI: {result[1]}")
        else:
            logging.info("No tokens meet the RSI conditions at this time.")

        end_time = datetime.now()
        logging.info("Script finished")
        logging.info(f"Total running time: {end_time - start_time}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze Solana ecosystem tokens based on RSI conditions.")
    parser.add_argument("--timeframe", type=str, required=True,
                        help="Timeframe for fetching OHLCV data (e.g., '1h', '4h', '1d')")
    args = parser.parse_args()

    logging.info(f"Timeframe argument received: {args.timeframe}")

    main(args.timeframe)
