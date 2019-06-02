import json
import operator
from botocore.vendored import requests
from datetime import datetime

# Setup
currency1 = 'BTC'
currency2 = ['USD', 'USDT']
exchanges = [
    "Bitfinex",
    "Binance",
    "Poloniex",
    "Coinbase",
    "BitTrex" 
]
api_key = 'c32565db2e025bfaba2a25ccc2068d5aa44ddaefd51277bfd833e5649606defc'


# Define Functions
def get_coin_price(currency1, currency2, exchange, api_key):
    url = 'https://min-api.cryptocompare.com/data/price?fsym={}&tsyms={}&api_key={}&e={}'.format(
        currency1, 
        currency2, 
        api_key, 
        exchange
    )
    
    headers = {
        'Content-Type': "application/json"
    }
    response = requests.request("GET", url, headers=headers).json()
    
    return response

def find_arbitarage_opportunities(currency1, currency2, exchanges, api_key):
    
    usd_exchange = ['Coinbase', 'BitTrex', 'Bitfinex']
    usdt_exchange = ['Binance', 'Poloniex']
    exchange_list = []
    value_list = []
    
    # create price list
    for exchange in exchanges:
        if exchange in usd_exchange:
            coin_price = get_coin_price(currency1, currency2[0], exchange, api_key)['USD']
        else:
            coin_price = get_coin_price(currency1, currency2[1], exchange, api_key)['USDT']
        value_list.append(coin_price)
        
    # create exchange list
    for i in range(0, len(exchanges)):
        exchange_list.append(exchanges[i])
        
    # create dictionary
    response = dict(zip(exchange_list, value_list))
    
    # min and max
    max_value = max(response.values())
    max_exchange = max(response.items(), key=operator.itemgetter(1))[0]
    min_value = min(response.values())
    min_exchange = min(response.items(), key=operator.itemgetter(1))[0]
    
    # fees
    
    
    # time
    now = datetime.now()
    timestamp = str(now.month) + '-' + str(now.day) + '-' + str(now.year) + ' / ' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second)
    
    # gains
    dollar_dif = round(max_value - min_value)
    percent_gain = ((max_value - min_value)/min_value)*100
    
    
    
    # create output
    output = create_output(
        response, 
        max_value, 
        max_exchange,
        min_value, 
        min_exchange,
        timestamp,
        dollar_dif,
        percent_gain
    )
    
    return output

def get_btc_values_and_spreads(exchange_and_values):
    
    all_spreads = {}
    
    for key, value in exchange_and_values.items():
        spreads = {}
        temp_key = key
        temp_value = value
        
        for key2, value2 in exchange_and_values.items():
            temp_spread = {
                key2: value-value2
            }
            spreads.update(temp_spread)
        
        temp_dict = {
            temp_key: {
                "value": temp_value,
                "spreads": spreads
            }
        }
        
        all_spreads.update(temp_dict)
        
    return all_spreads 
    
def create_output(exchange_and_values, max_value, max_exchange, min_value, min_exchange, timestamp, dollar_dif, percent_gain):
    output = {
        'BTC': get_btc_values_and_spreads(exchange_and_values),
        'max_exchange': max_exchange,
        'max_value': max_value,
        'min_exchange': min_exchange,
        'min_value': min_value,
        'timestamp': timestamp,
        'dollar_dif': dollar_dif,
        'percent_gain': percent_gain
    }
    
    return output

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(find_arbitarage_opportunities(currency1, currency2, exchanges, api_key))
    }

