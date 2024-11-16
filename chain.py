import requests


def get_top_chains(limit=10):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': limit,
        'page': 1
    }
    response = requests.get(url, params=params)
    return response.json()
