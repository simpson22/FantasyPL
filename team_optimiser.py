"""The Fantasy team selection model using PuLP"""

from pulp import *
import team_selector as ts
import player as pl

myTeam = pl.u_PlayerListArray

# Allows the user to filter the candidate pool before solving
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

# Creates player attribute arrays
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

# Creates player team attribute arrays
for team in allTeamArray:
    playerTeam = {}
    for players in myTeam:
        if players['team_code'] == team:
            playerTeam[players['id']] = 1
        else:
            playerTeam[players['id']] = 0
    allTeamArray[team] = playerTeam

problem = LpProblem('The FPL Team Problem', LpMaximize)
playerVariables = LpVariable.dicts("Player", playerIds, 0, 1, LpInteger)  # Player variables "Player_1" Binary value

problem += lpSum([playerPoints[i]*playerVariables[i] for i in playerIds])  # Player scores

problem += lpSum([playerGKP[i]*playerVariables[i] for i in playerIds]) == 1  # Only 1 Goalkeeper
problem += lpSum([playerDEF[i]*playerVariables[i] for i in playerIds]) >= 3  # More than or equal to 3 Defenders
problem += lpSum([playerDEF[i]*playerVariables[i] for i in playerIds]) <= 5  # Less than or equal to 5 Defenders
problem += lpSum([playerMID[i]*playerVariables[i] for i in playerIds]) >= 3  # More than or equal to 3 Midfielders
problem += lpSum([playerMID[i]*playerVariables[i] for i in playerIds]) <= 5  # Less than or equal to 5 Midfielders
problem += lpSum([playerFWD[i]*playerVariables[i] for i in playerIds]) >= 1  # More than or equal to 1 Striker
problem += lpSum([playerFWD[i]*playerVariables[i] for i in playerIds]) <= 3  # Less than or equal to 3 Strikers

# Less than or equal to 3 players per team
for team in allTeamArray:
    teamArray = allTeamArray[team]
    problem += lpSum([teamArray[i] * playerVariables[i] for i in playerIds]) <= 3

problem += lpSum([playerCost[i]*playerVariables[i] for i in playerIds]) <= 873  # Less than or equal to 85M budget

problem += lpSum([playerVariables[i] for i in playerIds]) == 11  # 11 Players

# Creates the lp problem file and solves the problem
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
