import requests
import json

# Try to download fpl static data, print response code and any error
try:
    dataRequest = requests.get('https://fantasy.premierleague.com/drf/bootstrap-static')
    dataRequest.raise_for_status()
except requests.exceptions.RequestException as e:
    print('Could not request data:', e, sep='\n')
    success = 0
else:
    # Open and write to a raw_data.json file, dumping request object as json
    with open('data\\raw_data.json', 'w') as write_file:
        json.dump(dataRequest.json(), write_file)
    success = 1

if success:
    print('scraper ran successfully')
else:
    print('scraper ran with errors')
