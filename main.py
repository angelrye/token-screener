import time
import logging
from datetime import datetime
from broker import Binance, Bybit
from chain import get_top_chains
from token_list import get_binance_tokens, get_bybit_tokens
from ohlcv import fetch_ohlcv
from rsi import check_rsi_conditions

logging.basicConfig(level=logging.INFO)


def get_top_brokers():
    brokers = {
        "Binance": Binance(),
        "Bybit": Bybit(),
        "Kraken": None,  # Add broker class when implemented
        "Coinbase": None,  # Add broker class when implemented
        "Crypto.com": None,  # Add broker class when implemented
        "Gemini": None,  # Add broker class when implemented
        "Huobi": None,  # Add broker class when implemented
        "Bitfinex": None,  # Add broker class when implemented
        "OKEx": None,  # Add broker class when implemented
        "eToro": None  # Add broker class when implemented
    }
    return brokers


def select_from_list(options, prompt):
    for index, option in enumerate(options):
        print(f"{index + 1}. {option}")
    print("0. Exit")

    choice = int(input(prompt))
    if choice == 0:
        print("Exiting...")
        exit()
    return choice - 1


def main():
    while True:
        brokers = get_top_brokers()
        print("Top 10 Cryptocurrency Brokers:")
        broker_names = list(brokers.keys())
        broker_choice = select_from_list(
            broker_names, "Select a broker (0 to Exit): ")
        selected_broker = brokers[broker_names[broker_choice]]

        if selected_broker is None:
            print("Broker not implemented yet. Please select another broker.")
            continue

        top_chains = get_top_chains()
        print("\nTop 10 Cryptocurrency Chains:")
        chain_names = [chain['name'] for chain in top_chains]
        chain_choice = select_from_list(
            chain_names, "Select a chain (0 to Exit): ")
        selected_chain = top_chains[chain_choice]['id']

        timeframes = ['15m', '30m', '1h', '4h', '1d']
        print("\nSelect a timeframe:")
        timeframe_choice = select_from_list(
            timeframes, "Select a timeframe (0 to Exit): ")
        selected_timeframe = timeframes[timeframe_choice]

        lookback = int(
            input("Enter the lookback period (number of candles) (0 to Exit): "))
        if lookback == 0:
            print("Exiting...")
            exit()

        if broker_names[broker_choice] == "Binance":
            tokens = get_binance_tokens(selected_chain)
        elif broker_names[broker_choice] == "Bybit":
            tokens = get_bybit_tokens(selected_chain)
        else:
            print("Broker token fetch not implemented yet. Please select another broker.")
            continue

        start_time = datetime.now()
        logging.info(f"\nScanning tokens... (Start time: {start_time})")
        total_symbols = len(tokens)
        logging.info(f"Total Symbols: {total_symbols}")

        matching_tokens = []
        try:
            for i, token in enumerate(tokens):
                logging.info(
                    f"Processing {token} ({i + 1}/{total_symbols})...")

                df = fetch_ohlcv(token, selected_timeframe)
                meets_condition, current_rsi = check_rsi_conditions(
                    df, lookback)

                if meets_condition:
                    matching_tokens.append((token, current_rsi))
        except KeyboardInterrupt:
            print("\nScanning interrupted by user.")
        finally:
            end_time = datetime.now()
            logging.info(f"\nScanning completed. (End time: {end_time})")
            logging.info(f"Total running time: {end_time - start_time}")

            print("\nTokens that meet the criteria:")
            for matching_token, rsi_value in matching_tokens:
                print(f"{matching_token} - Current RSI: {rsi_value}")

            another_scan = input(
                "Do you want to do another scan? (Y/n): ").strip().lower()
            if another_scan != 'y':
                print("Exiting...")
                break


if __name__ == "__main__":
    main()
