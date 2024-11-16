import requests


def get_top_chains():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 20,
        'page': 1
    }
    response = requests.get(url, params=params)
    return response.json()


def get_tokens_for_chain(chain_id):
    url = f"https://api.coingecko.com/api/v3/coins/{chain_id}"
    response = requests.get(url)
    return response.json()


def main():
    top_chains = get_top_chains()
    print("Top 10 Cryptocurrency Chains:")
    for index, coin in enumerate(top_chains):
        print(f"{index + 1}. {coin['name']}")

    choice = int(input("Select a chain (1-10): ")) - 1
    if 0 <= choice < len(top_chains):
        selected_chain = top_chains[choice]
        chain_id = selected_chain['id']
        tokens = get_tokens_for_chain(chain_id)

        print(f"\nTokens for {selected_chain['name']}:")
        for token in tokens['tickers']:
            print(f"- {token['base']}/{token['target']}")
    else:
        print("Invalid selection. Please run the script again and select a valid chain.")


if __name__ == "__main__":
    main()
