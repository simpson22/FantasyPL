import json

# Open the raw_data.json in read only, json format, and initialise list
fplData = json.load(open('data\\raw_data.json', 'r'))
fplObjectList = []

# Create a list of all the object types in fpl data
for fplObject in fplData:
    fplObjectList.append(str(fplObject))

# For each object type write the data to a new file
for filename in fplObjectList:
    with open('data\\' + filename + '.json', 'w') as write_file:
        json.dump(fplData[filename], write_file)

if __name__ == '__main__':
    print('parser ran successfully')
