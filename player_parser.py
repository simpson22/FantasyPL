"""Requests and Writes all Individual player data from  https://fantasy.premierleague.com/"""

import fpl_scraper_utils as su
import fpl_parser_utils as pu
import matplotlib.pyplot as plt

# Read fixture data, gather difficulty ratings for all fixtures
readMode = 'fixtures'
fixtureData = pu.read_json_data(pu.readLocations[readMode])

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
    requestData = su.fantasy_request(requestMode, element)
    su.write_json_file(requestData, requestMode, element)

readMode = requestMode + str(elements[0])

playerData = pu.read_json_data(pu.readLocations[readMode])

interestedHistoryKeys = ['element',
                         'round',
                         'fixture',
                         'was_home',
                         'total_points', ]
playerHistoryList = []
playerHistory = {}

# Create list array for each fixture played, gathering key statistics and finding the difficulty fixture.
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

# Create total, round, history and last3 point statistics.
for game_round in playerHistoryList:
    game_round['round_points'] = game_round['total_points']
    game_round['history_points'] = \
        sum([int(x['round_points']) for x in playerHistoryList if x['round'] < game_round['round']])
    game_round['weighted_history_points'] = \
        round(sum([int(x['round_points']) for x in playerHistoryList if x['round'] < game_round['round']])
                        / game_round['round'], 2)
    game_round['total_points'] = game_round['round_points'] + game_round['history_points']
    game_round['last3_points'] = sum([int(x['round_points']) for
                            x in playerHistoryList if game_round['round'] - 4 < x['round'] < game_round['round']])

print(playerHistoryList)

round_points = []
last3_points = []
weighted_history_points = []
for game_round in playerHistoryList:
    if game_round['round'] > 3:
        round_points.append(game_round['round_points'])
        last3_points.append(game_round['last3_points'] / 3)
        weighted_history_points.append(game_round['weighted_history_points'])

plt.scatter(last3_points, round_points, color='r')
plt.scatter(weighted_history_points, round_points, color='b')
plt.xlabel('Historic Stats')
plt.ylabel('Round_Points')
plt.show()

# TODO
# For each played fixture, find fixture difficulty and see correlation with current fixture score
# Segregate data into positions and teams? Plot Data
# Modify optimiser score metric to take into account new metrics to predict upcoming performance


