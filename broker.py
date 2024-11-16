import ccxt


class Broker:
    def __init__(self):
        self.exchange = None

    def get_rsi_data(self, token_id, timeframe, lookback):
        raise NotImplementedError(
            "This method should be overridden by subclasses")


class Binance(Broker):
    def __init__(self):
        self.exchange = ccxt.binance()

    def get_rsi_data(self, token_id, timeframe, lookback):
        symbol = token_id.upper() + '/USDT'
        try:
            ohlcv = self.exchange.fetch_ohlcv(
                symbol, timeframe, limit=lookback)
            return ohlcv
        except ccxt.base.errors.BadSymbol:
            print(f"Error: {symbol} is not available on Binance.")
            return None


class Bybit(Broker):
    def __init__(self):
        self.exchange = ccxt.bybit()

    def get_rsi_data(self, token_id, timeframe, lookback):
        symbol = token_id.upper() + '/USDT'
        try:
            ohlcv = self.exchange.fetch_ohlcv(
                symbol, timeframe, limit=lookback)
            return ohlcv
        except ccxt.base.errors.BadSymbol:
            print(f"Error: {symbol} is not available on Bybit.")
            return None
