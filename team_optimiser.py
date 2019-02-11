"""The Fantasy team selection model using PuLP"""

from pulp import *
import team_selector as ts
import player as pl

myTeam = pl.u_PlayerListArray

while True:
    print(len(myTeam), 'Candidates remaining\nWould you like to filter the candidate pool y/n')
    answer = input()
    if answer == 'y':
        myTeam = ts.filter_players(pl.u_PlayerListArray)
    else:
        break

playerIds = []
playerPoints = {}
playerCost = {}
playerGKP = {}
playerDEF = {}
playerMID = {}
playerFWD = {}

for players in myTeam:
    playerIds.append(players['id'])
    playerPoints[players['id']] = players['total_points']
    playerCost[players['id']] = players['now_cost']
    playerGKP[players['id']] = 0
    playerDEF[players['id']] = 0
    playerMID[players['id']] = 0
    playerFWD[players['id']] = 0
    if players['element_type'] == 1:
        playerGKP[players['id']] = 1
    elif players['element_type'] == 2:
        playerDEF[players['id']] = 1
    elif players['element_type'] == 3:
        playerMID[players['id']] = 1
    else:
        playerFWD[players['id']] = 1

allTeamArray = {i: 0 for i in range(1, 21)}

for team in allTeamArray:
    playerTeam = {}
    for players in myTeam:
        if players['team_code'] == team:
            playerTeam[players['id']] = 1
        else:
            playerTeam[players['id']] = 0
    allTeamArray[team] = playerTeam

problem = LpProblem('The FPL Team Problem', LpMaximize)
playerVariables = LpVariable.dicts("Player", playerIds, 0, 1, LpInteger)

problem += lpSum([playerPoints[i]*playerVariables[i] for i in playerIds])

problem += lpSum([playerGKP[i]*playerVariables[i] for i in playerIds]) == 1
problem += lpSum([playerDEF[i]*playerVariables[i] for i in playerIds]) >= 3
problem += lpSum([playerDEF[i]*playerVariables[i] for i in playerIds]) <= 5
problem += lpSum([playerMID[i]*playerVariables[i] for i in playerIds]) >= 3
problem += lpSum([playerMID[i]*playerVariables[i] for i in playerIds]) <= 5
problem += lpSum([playerFWD[i]*playerVariables[i] for i in playerIds]) >= 1
problem += lpSum([playerFWD[i]*playerVariables[i] for i in playerIds]) <= 3

for team in allTeamArray:
    teamArray = allTeamArray[team]
    problem += lpSum([teamArray[i] * playerVariables[i] for i in playerIds]) <= 3

problem += lpSum([playerCost[i]*playerVariables[i] for i in playerIds]) <= 850

problem += lpSum([playerVariables[i] for i in playerIds]) == 11

problem.writeLP("FPL_Team_Problem.lp")
problem.solve()

print("Status:", LpStatus[problem.status])
print("Total number of points achieved by the team = ", value(problem.objective))

for v in problem.variables():
    if v.varValue == 1.0:
        for players in myTeam:
            if players['id'] == int(v.name[7:]):
                print(players)

if __name__ == '__main__':
    print('team optimiser ran successfully')
