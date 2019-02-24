import fpl_parser_utils as pu
import fpl_scraper_utils as su

# Load the elements data and initialise an array and list
fplData = pu.read_json_data('raw_data')
su.write_json_file(fplData['elements'], 'elements')

fplPlayerData = pu.read_json_data('elements')
playerInfo = {}
u_PlayerListArray = []

# List the data points we are interested in extracting
interestedKeys = ['id',
                  'web_name',
                  'team_code',
                  'status',
                  'element_type',
                  'now_cost',
                  'total_points', ]

# For each player in the fpl player data, and for each key in interested keys add the data to our dictionary,
# create a new data point Pts/£ and append this player dictionary to our playerListArray
for player in fplPlayerData:
    for keys in interestedKeys:
        playerInfo[keys] = player[keys]
    playerInfo['u_Pts/£'] = round(playerInfo['total_points'] / playerInfo['now_cost'] * 10, 2)
    u_PlayerListArray.append(dict(playerInfo))

# Sort our list of players by the new Pts/£, placing into a new list
u_PlayerInfoSorted = sorted(u_PlayerListArray, key=lambda a: a['u_Pts/£'], reverse=True)

if __name__ == '__main__':
    for player in u_PlayerInfoSorted[:5]:
        print(player)
    print(len(u_PlayerListArray), 'Players stored')
    print('player ran successfully')


