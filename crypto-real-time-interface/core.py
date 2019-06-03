import requests
import json
import operator

def top_five_spreads_route():

    response = get_prices_and_spreads()
    largest_five_spreads = calculate_top_five_spreads(response["BTC"])
    response = json.dumps(largest_five_spreads)

    return response

def calculate_top_spread():
    # gets the response object and returns it entirely
    response = get_prices_and_spreads()
    response = json.dumps(response)

    return response

def get_prices_and_spreads():

    url = 'YOUR AWS URL HERE'
    headers = {
        'Content-Type': "application/json"
    }
    response = requests.request("GET", url, headers=headers).json()

    return response

def calculate_top_five_spreads(exchanges):
    combined_dict = {}
    five_pairs = []
    five_spreads = []
    for key in exchanges:
        combined_dict.update(exchanges[key]['spreads'])
    
    largest_spread = max(combined_dict.items(), key=operator.itemgetter(1))[0:]
    largest_five_spreads = dict(sorted(combined_dict.items(), key=operator.itemgetter(1), reverse=True)[:5])
    
    for key in largest_five_spreads:
        five_pairs.append(key)

    for key in largest_five_spreads:
        five_spreads.append(largest_five_spreads[key])

    response = {
        "largest_five_pairs": five_pairs,
        "largest_five_spreads": five_spreads,
        "combined_dict": largest_five_spreads
    }

    return response
