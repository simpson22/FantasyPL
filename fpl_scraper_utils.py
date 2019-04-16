"""Functions to retrieve and write data from 'https://fantasy.premierleague.com/drf/ with mode definitions"""
import requests
import json

requestModeMapping = dict(raw_data='bootstrap-static',
                          player='element-summary',
                          fixtures='fixtures', )


def fantasy_request(mode='raw_data', element=''):
    """Makes a request to FPL and returns the data.
    
    Args:
        mode: str() referring to the requestMode.
        element: str() or int() referring to API element if iterable.
        
    Returns:
        Response object in json format.
    """
    if element is not '':
        element = '/' + str(element)
    try:
        data = requests.get('https://fantasy.premierleague.com/drf/{}{}'.format(requestModeMapping[mode], element))
        data.raise_for_status()
        print('{}{} successfully requested'.format(mode, element))
        return data.json()
    except KeyError as e:
        print('Incorrect key {} provided'.format(e))
    except requests.exceptions.RequestException as e:
        print('Could not request data: \n{}'.format(e))


def write_json_file(write_data, mode=None, element=''):
    """Write a json file to specified location.

    Args:
        write_data: The json format data to be written.
        mode: str() pointing to write point and filename.
        element: str() or int() to be appended to filename.
    """
    element = str(element)
    file_location = 'data\\{0}\\{0}{1}.json'.format(mode, element)
    try:
        with open(file_location, 'w') as file:
                json.dump(write_data, file)
        print('{} successfully saved'.format(file_location))
    except EnvironmentError as e:
        print('Could not write to {}\n{}'.format(file_location, e))
    except AttributeError as e:
        print('Write data is not recognised as json: {}'.format(e))


def main():
    """Ask user for mode, performs request and writes json file"""
    print('Please enter one of the following modes\n{}'.format(str(requestModeMapping)))
    input_mode = [str(x) for x in input().split()]
    request_data = fantasy_request(*input_mode)
    write_json_file(request_data, *input_mode)
    print('scraper ran successfully')


if __name__ == '__main__':
    main()
