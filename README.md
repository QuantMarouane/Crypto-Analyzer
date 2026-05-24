import requests
def get_bitcoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        response = requests.get(url)
        data = response.json()
        price = data['bitcoin']['usd']
        print(f"Current Bitcoin price is: {price} USD")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_bitcoin_price()
