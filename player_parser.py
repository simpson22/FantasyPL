"""Requests and Writes all Individual player data from  https://fantasy.premierleague.com/"""

import fpl_scraper_utils as fs
import fpl_parser_utils as fp

# Read fixture data, gather difficulty ratings for all fixtures
readMode = 'fixtures'
fixtureData = fp.read_json_data(fp.readLocations[readMode])

interestedFixtureKeys = ['id', 'team_h_difficulty', 'team_a_difficulty']
fixtureList = []
fixture = {}

for fixture_element in fixtureData:
    for key in interestedFixtureKeys:
        fixture[key] = fixture_element[key]
    fixtureList.append(dict(fixture))

# Read player data prepare to gather player data on each fixture played so far
requestMode = 'player'
elements = list(range(115, 116))

for element in elements:
    requestData = fs.fantasy_request(requestMode, element)
    fs.write_json_file(requestMode, element, write_data=requestData)

readMode = requestMode + str(elements[0])

playerData = fp.read_json_data(fp.readLocations[readMode])

interestedHistoryKeys = ['element',
                         'round',
                         'fixture',
                         'was_home',
                         'total_points', ]
playerHistoryList = []
playerHistory = {}

# Create list array for each fixture played, gathering key statistics and finding the difficulty fixture
for history_element in playerData['history']:
    for key in interestedHistoryKeys:
        playerHistory[key] = history_element[key]
    for fixture in fixtureList:
        if playerHistory['fixture'] == fixture['id']:
            if playerHistory['was_home']:
                playerHistory['difficulty'] = fixture['team_h_difficulty']
            else:
                playerHistory['difficulty'] = fixture['team_a_difficulty']
    playerHistoryList.append(dict(playerHistory))

print(playerHistoryList)

# TODO
# For each played fixture, find recent scores and see correlation with current fixture score
# For each played fixture, find fixture difficulty and see correlation with current fixture score
# Segregate data into positions and teams? Plot Data
# Modify optimiser score metric to take into account new metrics to predict upcoming performance


