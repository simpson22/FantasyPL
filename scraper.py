"""The web scraper for ttps://fantasy.premierleague.com/drf API"""
import requests
import json

requestModes = dict(raw_data='bootstrap-static',
                    player='element-summary',
                    fixtures='fixtures', )


def fantasy_request(mode='bootstrap-static', element=''):
    """Provide a mode, and element if applicable, requests the data from FPL API, return success code and data."""
    data = None
    if element is not '':
        element = '/' + element
    try:
        data = requests.get('https://fantasy.premierleague.com/drf/' + requestModes[mode] + element)
        data.raise_for_status()
    except requests.exceptions.RequestException as e:
        print('Could not request data:', e, sep='\n')
        success = 0
    else:
        success = 1
        print(mode + ' successfully requested')
    return success, data


def write_json_file(mode, element='', write_data=None):
    """Provide a mode and element if applicable, writes the FPL API json format to a standard file location
     returning status"""
    file_location = 'data\\' + mode + '\\' + mode + element + '.json'
    try:
        with open(file_location, 'w') as file:
                json.dump(write_data.json(), file)
    except EnvironmentError as e:
        print('Could not write to ' + file_location, e, sep='\n')
        success = 0
    else:
        print(file_location + ' successfully saved')
        success = 1
    return success


if __name__ == '__main__':
    print('Please enter one of the following modes')
    print(requestModes)
    inputMode = [str(x) for x in input().split()]
    requestStatus, requestData = fantasy_request(*inputMode)
    writeStatus = write_json_file(*inputMode, write_data=requestData)
    if requestStatus and writeStatus:
        print('scraper ran successfully')
    else:
        print('scraper ran with errors')
