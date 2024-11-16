import time
from broker import Binance, Bybit  # Import specific brokers here
from chain import get_top_chains, get_tokens_for_chain
from rsi import calculate_rsi


def get_top_brokers():
    brokers = {
        "Kraken": None,  # Add broker class when implemented
        "Coinbase": None,  # Add broker class when implemented
        "Crypto.com": None,  # Add broker class when implemented
        "Gemini": None,  # Add broker class when implemented
        "Binance": Binance(),
        "Bybit": Bybit(),
        "Huobi": None,  # Add broker class when implemented
        "Bitfinex": None,  # Add broker class when implemented
        "OKEx": None,  # Add broker class when implemented
        "eToro": None  # Add broker class when implemented
    }
    return brokers


def main():
    brokers = get_top_brokers()
    print("Top 10 Cryptocurrency Brokers:")
    broker_names = list(brokers.keys())
    for index, broker in enumerate(broker_names):
        print(f"{index + 1}. {broker}")

    broker_choice = int(input("Select a broker (1-10): ")) - 1
    selected_broker = brokers[broker_names[broker_choice]]

    if selected_broker is None:
        print("Broker not implemented yet. Please select another broker.")
        return

    top_chains = get_top_chains()
    print("\nTop 10 Cryptocurrency Chains:")
    for index, chain in enumerate(top_chains):
        print(f"{index + 1}. {chain['name']}")

    chain_choice = int(input("Select a chain (1-10): ")) - 1
    selected_chain = top_chains[chain_choice]
    chain_id = selected_chain['id']

    timeframes = ['15m', '30m', '1h', '4h', '1d']
    print("\nSelect a timeframe:")
    for index, timeframe in enumerate(timeframes):
        print(f"{index + 1}. {timeframe}")

    timeframe_choice = int(input("Select a timeframe (1-5): ")) - 1
    selected_timeframe = timeframes[timeframe_choice]

    lookback = int(input("Enter the lookback period (number of candles): "))

    tokens = get_tokens_for_chain(chain_id)

    print("\nScanning tokens...")
    matching_tokens = []
    for token in tokens['tickers']:
        print(f"Scanning {token['base']}/{token['target']}...", end='\r')
        data = selected_broker.get_rsi_data(
            token['base'], selected_timeframe, lookback)

        if not data:
            continue

        closes = [float(candle[4]) for candle in data]
        rsi_values = [calculate_rsi(closes[i:i + 14])
                      for i in range(len(closes) - 14)]
        if any(rsi >= 70 for rsi in rsi_values) and 40 < rsi_values[-1] < 60:
            matching_tokens.append(f"{token['base']}/{token['target']}")

        time.sleep(0.5)  # To avoid hitting API rate limits

    print("\nTokens that meet the criteria:")
    for matching_token in matching_tokens:
        print(matching_token)


if __name__ == "__main__":
    main()
