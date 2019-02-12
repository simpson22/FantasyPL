"""The web scraper for ttps://fantasy.premierleague.com/drf API"""
import requests
import json

modes = dict(raw_data='bootstrap-static',
             player='element-summary',
             fixtures='fixtures', )


def fantasy_request(mode='bootstrap-static', element=None):

    if element is not None:
        file_element = element
        element = '/' + element
    else:
        element = ''
        file_element = ''
    try:
        request_data = requests.get('https://fantasy.premierleague.com/drf/' + modes[mode] + element)
        request_data.raise_for_status()
    except requests.exceptions.RequestException as e:
        print('Could not request data:', e, sep='\n')
        success = 0
    else:
        # Open and write to a raw_data.json file, dumping request object as json
        try:
            with open('data\\' + mode + '\\' + mode + file_element + '.json', 'w') as write_file:
                json.dump(request_data.json(), write_file)
        except EnvironmentError as e:
            print('Could not write ' + mode + ' file', e, sep='\n')
            success = 0
        else:
            print(mode + ' successfully extracted')
            success = 1
    return success


if __name__ == '__main__':
    print('Please enter one of the following modes')
    print(modes)
    kwargs = [str(x) for x in input().split()]
    status = fantasy_request(*kwargs)
    if status:
        print('scraper ran successfully')
    else:
        print('scraper ran with errors')
