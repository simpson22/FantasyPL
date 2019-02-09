import player as pl
import numpy as np

print(pl.u_PlayerListArray)


def filter_players(player_array, attribute, constraint, condition='eq'):
    # Function which removes players based on arguments
    filtered_players = []
    number_excluded = 0
    for players in player_array:
        if type(constraint) is str or condition == 'eq':
            if players[attribute] == constraint:
                filtered_players.append(dict(players))
            else:
                number_excluded += 1
        elif condition == 'gt':
            if players[attribute] >= constraint:
                filtered_players.append(dict(players))
            else:
                number_excluded += 1
        else:
            if players[attribute] <= constraint:
                filtered_players.append(dict(players))
            else:
                number_excluded += 1
    print(number_excluded, 'removed based on their', attribute, 'and', len(filtered_players), 'remain')
    return filtered_players


availablePlayers = filter_players(pl.u_PlayerListArray, 'element_type', 2)
budget = 100
squadLimit = 11
teamLimit = 3
positionLimits = {1: 1, 2: 5, 3: 5, 4: 3}
attributes = ['id',
              'total_points',
              'now_cost',
              'team_code',
              'element_type', ]

x = np.zeros((len(availablePlayers), len(attributes)), dtype=np.float)
pl = 0
at = 0

for players in availablePlayers:
    for values in attributes:
        x[pl, at] = (players[values])
        at += 1
    pl += 1
    at = 0

np.savetxt('data\\array.csv', x, delimiter=',', fmt='%.3d')

print('team_selector ran successfully')
