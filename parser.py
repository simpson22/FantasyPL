import json
import scraper as sc

fileLocations = dict(sc.modes)
fileLocations['raw_data'] = 'data\\raw_data\\raw_data.json'
fileLocations['fixtures'] = 'data\\fixtures\\fixtures.json'
fileLocations['player'] = 'data\\player\\player1.json'


def read_json_data(file_location):
    """Opens file containing json data and returns json object."""
    json_data = json.load(open(file_location, 'r'))
    return json_data


def find_json_objects(json_data):
    """Iterates over data and returns a list of object names."""
    object_list = []
    for json_object in json_data:
        object_list.append(str(json_object))
    return object_list


def show_first_json_item(fpl_object, json_data):
    """Find the first item in the fpl object and returns it."""
    json_series = json_data[fpl_object]
    json_item = json_series[0]
    return json_item


if __name__ == '__main__':
    print('Select a file to analyse\n' + str(fileLocations.keys()))
    fplData = read_json_data(fileLocations[input()])
    fplObjects = find_json_objects(fplData)
    print('Select an object to inspect\n' + str(fplObjects))
    fplItem = show_first_json_item(input(), fplData)
    print(fplItem)
    print('parser ran successfully')
