import requests
import json

# Try to download fpl static data, print response code and any error
try:
    requestData = requests.get('https://fantasy.premierleague.com/drf/bootstrap-static')
    requestData.raise_for_status()
except requests.exceptions.RequestException as e:
    print('Could not request data:', e, sep='\n')
    success = 0
else:
    # Open and write to a raw_data.json file, dumping request object as json
    try:
        with open('data\\raw_data.json', 'w') as write_file:
            json.dump(requestData.json(), write_file)
    except EnvironmentError as e:
        print('Could not write to file', e, sep='\n')
        success = 0
    else:
        success = 1

if __name__ == '__main__':
    if success:
        print('scraper ran successfully')
    else:
        print('scraper ran with errors')
