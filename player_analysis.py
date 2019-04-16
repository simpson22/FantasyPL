"""Requests and Writes all Individual player data from  https://fantasy.premierleague.com/"""

import fpl_scraper_utils as su
import fpl_parser_utils as pu
import matplotlib.pyplot as plt
from collections import Counter

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
elements = list(range(1, 601))

round_points = []
last3_points = []
weighted_history_points = []
fixture_difficulty = []

for element in elements:
    requestData = su.fantasy_request(requestMode, element)
    su.write_json_file(requestData, requestMode, element)

    readMode = requestMode + str(element)

    readLocations = pu.find_read_modes()

    playerData = pu.read_json_data(readLocations[readMode])

    interestedHistoryKeys = ['element',
                             'round',
                             'fixture',
                             'was_home',
                             'minutes',
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

    for game_round in playerHistoryList:
        if game_round['round'] > 3 and game_round['minutes'] >= 60 and game_round['round_points'] > 3:
            round_points.append(game_round['round_points'])
            last3_points.append(game_round['last3_points'] / 3)
            weighted_history_points.append(game_round['weighted_history_points'])
            fixture_difficulty.append(game_round['difficulty'])

c1 = Counter(zip(last3_points, round_points))
c2 = Counter(zip(weighted_history_points, round_points))
c3 = Counter(zip(fixture_difficulty, round_points))
s1 = [c1[(xx, yy)] for xx, yy in zip(last3_points, round_points)]
s2 = [c2[(xx, yy)] for xx, yy in zip(weighted_history_points, round_points)]
s3 = [c3[(xx, yy)] for xx, yy in zip(fixture_difficulty, round_points)]

plt.figure(1)
plt.subplot(131)
plt.scatter(last3_points, round_points, s=s1, color='r')
plt.xlabel('Recent Stats')
plt.ylabel('Round_Points')

plt.subplot(132)
plt.scatter(weighted_history_points, round_points, s=s2, color='b')
plt.xlabel('Historic Stats')
plt.ylabel('Round_Points')

plt.subplot(133)
plt.scatter(fixture_difficulty, round_points, s=s3, color='g')
plt.xlabel('Fixture Difficulty')
plt.ylabel('Round_Points')
plt.show()

# TODO
# For each played fixture, find fixture difficulty and see correlation with current fixture score
# Segregate data into positions and teams? Plot Data
# Modify optimiser score metric to take into account new metrics to predict upcoming performance


