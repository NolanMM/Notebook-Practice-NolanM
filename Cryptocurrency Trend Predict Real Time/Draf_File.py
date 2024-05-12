import configparser
import json
import pytz
from datetime import datetime
from requests import Request, Session
from dateutil import parser
import pprint

# Coinmarketcap API url
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
api = 'YOUR_API_KEY'  # Replace this with your API key
parameters = {'slug': 'bitcoin',
              'convert': 'USD'}  # API parameters to pass in for retrieving specific cryptocurrency data

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api
}  # Headers for the API request


# Function to get the info
def get_info():
    config = configparser.ConfigParser()
    config.read('coinmarket.ini')
    api_key = config['DEFAULT']['API_KEY']

    session = Session() # Create new session object to manage API requests
    session.headers.update(headers) #Update the session headers with the specified headers

    response = session.get(url, params=parameters) # Receiving the response from the API

    info = json.loads(response.text)

    pprint.pprint(info) # Displaying JSON data in a visually pleasing format on the terminal for improved readability


def get_info_historical():
    # Read the API key from the coinmarket.ini file
    config = configparser.ConfigParser()
    config.read('coinmarket.ini')
    api_key = config['DEFAULT']['API_KEY']

    # Send the request and retrieve the response
    session = Session()
    session.headers.update(headers)
    response = session.get(url, params=parameters)
    info = json.loads(response.text)

    # Extract the desired information from the response
    data = info['data']['1']
    name = data['name']
    symbol = data['symbol']
    rank = data['cmc_rank']
    total_supply = data['total_supply']
    circulating_supply = data['circulating_supply']
    market_cap = data['quote']['USD']['market_cap']
    price = data['quote']['USD']['price']
    market_cap_dominance = data['quote']['USD']['market_cap_dominance']
    percent_change_1h = data['quote']['USD']['percent_change_1h']
    percent_change_24h = data['quote']['USD']['percent_change_24h']
    volume_24h = data['quote']['USD']['volume_24h']
    volume_change_24h = data['quote']['USD']['volume_change_24h']
    timestamp = info['status']['timestamp']

    # Convert the timestamp to a timezone-aware datetime object
    timestamp_local = parser.parse(timestamp).astimezone(pytz.timezone('Turkey'))

    # Format the timestamp as desired
    formatted_timestamp = timestamp_local.strftime('%Y-%m-%d %H:%M:%S')

    # Print the information
    print(
        f'Name: {name}, Symbol: {symbol}, Price: {price:,.2f}, Percent change (1h): {percent_change_1h}, Percent change (24h): {percent_change_24h}, Total supply: {total_supply}, Circulating supply: {circulating_supply}, Market capitalization: {market_cap}, Market capitalization dominance: {market_cap_dominance}, Volume (24h): {volume_24h}, Volume change (24h): {volume_change_24h}, Timestamp: {formatted_timestamp}')


get_info_historical()
get_info()
