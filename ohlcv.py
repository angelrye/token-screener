import ccxt
import pandas as pd
import logging


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
