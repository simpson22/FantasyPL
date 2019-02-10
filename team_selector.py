import player as pl
import re


def filter_player_array(player_array, attribute, condition='eq', constraint=None):
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
            if int(players[attribute]) >= constraint:
                filtered_players.append(dict(players))
            else:
                number_excluded += 1
        else:
            if int(players[attribute]) <= constraint:
                filtered_players.append(dict(players))
            else:
                number_excluded += 1
    print(number_excluded, 'removed based on their', attribute, 'and', len(filtered_players), 'remain')
    return filtered_players


def check_player_attributes(player_array):
    valid_attributes = []
    for attributes in player_array[0]:
        valid_attributes.append(attributes)
    return valid_attributes


def filter_players_input(player_array):
    user_filter = []
    valid_attributes = check_player_attributes(player_array)
    valid_conditions = ['eq', 'lt', 'gt', ]
    while len(user_filter) != 3:
        print('Please input your filter options selecting a player attribute, the condition and constraint:')
        print('Valid Attributes are:', valid_attributes, '\n Valid Conditions are:', valid_conditions, sep='\n')
        print('e.g. status eq a, or, now_cost gt 50')
        user_filter = [str(x) for x in input().split()]
        if re.search('[0-9]', user_filter[2]) is not None:
            user_filter[2] = float(user_filter[2])
    else:
        return user_filter


def filter_players(player_array):
    user_filter = filter_players_input(player_array)
    user_players = filter_player_array(player_array, user_filter[0], user_filter[1], user_filter[2])
    return user_players


if __name__ == '__main__':
    uFilter = filter_players_input(pl.u_PlayerListArray)
    filter_player_array(pl.u_PlayerListArray, uFilter[0], uFilter[1], uFilter[2])
    print('team_selector ran successfully')
