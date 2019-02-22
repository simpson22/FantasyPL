"""The web scraper for https://fantasy.premierleague.com/drf API"""
import requests
import json

requestModes = dict(raw_data='bootstrap-static',
                    player='element-summary',
                    fixtures='fixtures', )


def fantasy_request(mode='bootstrap-static', element=''):
    """Provide a mode, and element if applicable, requests the data from FPL API, return success code and data."""
    if element is not '':
        element = '/' + str(element)
    try:
        data = requests.get('https://fantasy.premierleague.com/drf/' + requestModes[mode] + element)
        data.raise_for_status()
        print('{}{} successfully requested'.format(mode, element))
        return data
    except KeyError as e:
        print('Incorrect key {} provided'.format(e))
    except requests.exceptions.RequestException as e:
        print('Could not request data: \n{}'.format(e))


def write_json_file(write_data, mode=None, element=''):
    """Provide a mode and element if applicable, writes the FPL API json format to a standard file location
     returning status"""
    element = str(element)
    file_location = 'data\\' + mode + '\\' + mode + element + '.json'
    try:
        with open(file_location, 'w') as file:
                json.dump(write_data.json(), file)
        print('{} successfully saved'.format(file_location))
    except EnvironmentError as e:
        print('Could not write to {}\n{}'.format(file_location, e))
    except AttributeError as e:
        print('Write data is not recognised as json: {}'.format(e))


if __name__ == '__main__':
    print('Please enter one of the following modes\n{}'.format(str(requestModes)))
    inputMode = [str(x) for x in input().split()]
    requestData = fantasy_request(*inputMode)
    write_json_file(requestData, *inputMode)
    print('scraper ran successfully')

