import ccxt
import pandas as pd
import ta
import time


def fetch_ohlcv(symbol, timeframe):
    """Fetches OHLCV data for a given symbol and timeframe"""
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

    recent_rsi_touch = df.tail(recent_period)['rsi'].eq(70).any()
    current_rsi = df.iloc[-1]['rsi']

    if recent_rsi_touch and 40 < current_rsi < 60:
        return True, current_rsi
    return False, current_rsi


def get_bybit_symbols():
    """Fetches the list of symbols from Bybit"""
    exchange = ccxt.bybit()
    markets = exchange.fetch_markets()
    symbols = [market['symbol']
               for market in markets if 'USDT' in market['quote']]
    return symbols


def main():
    symbols = get_bybit_symbols()
    timeframe = '1h'  # Adjust as needed (e.g., '1h', '1d')
    recent_period = 10  # Adjust the number of recent periods to check for RSI touch

    results = []
    total_symbols = len(symbols)

    for i, symbol in enumerate(symbols):
        try:
            print(f"Processing {symbol} ({i + 1}/{total_symbols})...")
            meets_conditions, current_rsi = check_rsi_conditions(
                symbol, timeframe, recent_period)
            if meets_conditions:
                results.append((symbol, current_rsi))
        except Exception as e:
            print(f"Error processing {symbol}: {e}")

        # Avoid hitting API rate limits
        time.sleep(1)

    if results:
        print("Tokens that meet the RSI conditions:")
        for result in results:
            print(f"Symbol: {result[0]}, Current RSI: {result[1]}")
    else:
        print("No tokens meet the RSI conditions at this time.")


if __name__ == "__main__":
    main()
