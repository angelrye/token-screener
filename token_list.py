import re
import ccxt
import requests


def get_exchange_tokens(exchange):
    markets = exchange.fetch_markets()
    tokens = [market['symbol']
              for market in markets if market['quote'] == 'USDT']
    return tokens


def fetch_all_tokens():
    url = "https://api.coingecko.com/api/v3/coins/list?include_platform=true&status=active"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    return []


def fetch_solana_tokens_from_registry():
    """Fetches the list of Solana ecosystem tokens from the Solana token registry"""
    response = requests.get(
        "https://raw.githubusercontent.com/solana-labs/token-list/main/src/tokens/solana.tokenlist.json")
    data = response.json()
    # Exclude symbols matching the pattern ending in "-C" or "-P"
    solana_tokens = [token['symbol'].upper(
    ) + '/USDT' for token in data['tokens']]

    excluded_pattern = re.compile(r'.*-.*-.*-[CP]$')

    solana_tokens = [
        symbol for symbol in solana_tokens if not excluded_pattern.search(symbol)]

    return solana_tokens


def filter_tokens_by_chain(all_tokens, chain_platform):
    filtered_tokens = []
    for token in all_tokens:
        if 'platforms' in token and chain_platform in token['platforms']:
            filtered_tokens.append(token['symbol'].upper() + '/USDT')
    return filtered_tokens


def get_chain_platform(chain_name):
    chain_platforms = {
        "ethereum": 'ethereum',
        "solana": 'solana',
        "tron": 'tron',
        "binancecoin": 'binance-smart-chain',
        "bitcoin": 'bitcoin',
        "base": 'base',
        "arbitrum": 'arbitrum-one',
        "avalanche-2": 'avalanche',
        "sui": 'sui',
        "optimism": 'optimism'
    }
    return chain_platforms.get(chain_name, '')


def get_tokens(exchange, chain_name):

    filtered_tokens = []

    if chain_name == "solana":
        filtered_tokens = fetch_solana_tokens_from_registry()
    else:
        all_tokens = fetch_all_tokens()
        chain_platform = get_chain_platform(chain_name)
        filtered_tokens = filter_tokens_by_chain(all_tokens, chain_platform)

    exchange_tokens = get_exchange_tokens(exchange)
    unique_tokens = list(set(filtered_tokens))

    return [token for token in unique_tokens if token in exchange_tokens]


def get_binance_tokens(chain_name):
    exchange = ccxt.binance()
    return get_tokens(exchange, chain_name)


def get_bybit_tokens(chain_name):
    exchange = ccxt.bybit()
    return get_tokens(exchange, chain_name)
