import requests
import json

# Download fpl static data
dataRequest = requests.get('https://fantasy.premierleague.com/drf/bootstrap-static')

# Raise an exception if bad status code
dataRequest.raise_for_status()

# Open and write to a raw_data.json file, dumping request object as json
with open('data\\raw_data.json', 'w') as write_file:
        json.dump(dataRequest.json(), write_file)

print('scraper ran successfully')
