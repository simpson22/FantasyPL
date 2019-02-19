import json
import os


def find_read_modes():
    """Walks the data directory and returns mode, filepath dictionary"""
    read_modes = {}
    for folder, subFolders, files in os.walk('data'):
        for file in files:
            filename = file.split('.')
            read_modes[filename[0]] = folder + '\\' + file
    return read_modes


def read_json_data(file_location):
    """Opens file containing json data and returns json object."""
    json_data = json.load(open(file_location, 'r'))
    return json_data


def find_json_objects(json_data):
    """Iterates over data and returns a list of object names, if not a list of objects return first element"""
    object_list = []
    is_object = 0
    try:
        for json_object in json_data:
            if type(json_object) is str:
                object_list.append(json_object)
                is_object = 1
            else:
                print('Already at object level, first object is: \n' + str(json_data[0]))
                break
    except TypeError as e:
        print('Could not find json objects',  e, sep='\n')
        object_list = json_data
    return object_list, is_object


def show_json_item(fpl_object, json_data):
    """Find the first item in the fpl object and returns it."""
    try:
        json_item = json_data[0]
    except KeyError:
        json_series = json_data[fpl_object]
        json_item = json_series[0]
    return json_item


readLocations = find_read_modes()

if __name__ == '__main__':
    print('Select a file to analyse\n' + str(readLocations.keys()))
    fplData = read_json_data(readLocations[input()])
    fplObjects, isObject = find_json_objects(fplData)
    if isObject == 1:
        print('Select an object to inspect\n' + str(fplObjects))
        fplItem = show_json_item(input(), fplData)
        print(fplItem)
    print('parser ran successfully')
