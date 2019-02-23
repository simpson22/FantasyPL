import json
import os


def find_read_modes():
    """Find a file to filepath mapping in the data directory.

    Returns:
        Dictionary containing file : filepath mapping"""
    read_modes = {}
    for folder, subFolders, files in os.walk('data'):
        current_modes = {(file.split('.')[0]): '{}\\{}'.format(folder, file) for file in files}
        read_modes.update(current_modes)
    return read_modes


def read_json_data(file_location):
    """Opens file and returns json object

    Args:
        Filename or direct Filepath string

    Returns:
        Json object of the data from file."""
    if '.' not in file_location:
        file_location = readLocations[file_location]
    json_data = json.load(open(file_location, 'r'))
    return json_data


def find_json_objects(json_data):
    """Iterates over data and returns a list of object names, if not a list of objects return first element"""
    object_list = []
    try:
        for json_object in json_data:
            if type(json_object) is str:
                object_list.append(json_object)
            else:
                print('Already at object level, first object is: \n{}'.format(str(json_data[0])))
                object_list = [x['id'] for x in json_data]
                break
    except TypeError as e:
        print('Could not find iterable json object\njson_data: {}\n{}'.format(json_data, e))
    return object_list


def show_json_item(fpl_object, json_data):
    """Find the first item in the fpl object and returns it."""
    try:
        json_item = json_data[int(fpl_object) - 1]
        print('Object id {} returned'.format(fpl_object))
    except ValueError:
        json_series = json_data[fpl_object]
        try:
            json_item = json_series[0]
            print('First item from {} returned'.format(fpl_object))
        except KeyError:
            json_item = json_series
            print('Nested dictionary found')
        except TypeError:
            json_item = json_series
            print('Un-Iterable object found')
    return json_item


readLocations = find_read_modes()

if __name__ == '__main__':
    print('Select a file to analyse\n' + str(readLocations.keys()))
    fplData = read_json_data(input())
    fplObjects = find_json_objects(fplData)
    if fplObjects:
        print('Select an object to inspect\n' + str(fplObjects))
        fplItem = show_json_item(input(), fplData)
        print(fplItem)
    print('parser ran successfully')
