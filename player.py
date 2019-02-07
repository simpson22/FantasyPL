import json

# Load the elements data and initialise an array and list
fplPlayerData = json.load(open('data\\elements.json', 'r'))
playerInfo = {}
playerListArray = []

# List the data points we are interested in extracting
interestedKeys = ['id', 'web_name', 'now_cost', 'total_points', 'element_type']

# For each player in the fpl player data, and for each key in interested keys add the data to our dictionary,
# create a new data point Pts/£ and append this player dictionary to our playerListArray
for player in fplPlayerData:
    for keys in interestedKeys:
        playerInfo[keys] = player[keys]
    playerInfo['u_Pts/£'] = round(playerInfo['total_points'] / playerInfo['now_cost'] * 10, 2)
    playerListArray.append(dict(playerInfo))

# Sort our list of players by the new Pts/£, placing into a new list
u_PtsPPound = sorted(playerListArray, key=lambda a: a['u_Pts/£'], reverse=True)

for player in u_PtsPPound[:6]:
    print(player)


print('player ran successfully')
