"""The simplified team selection model using PuLP"""

from pulp import *
import team_selector as ts
import player as pl

myTeam = pl.u_PlayerListArray
playerIds = []
playerPoints = {}
playerVariables = {}

while True:
    print(len(myTeam), 'Candidates remaining\nWould you like to filter the candidate pool y/n')
    answer = input()
    if answer == 'y':
        myTeam = ts.filter_players(pl.u_PlayerListArray)
    else:
        break

for players in myTeam:
    playerIds.append(players['id'])
    playerPoints[players['id']] = players['total_points']

problem = LpProblem('The FPL Team Problem', LpMaximize)
playerVariables = LpVariable.dicts("Player", playerIds, 0, 1, LpInteger)

problem += lpSum([playerPoints[i]*playerVariables[i] for i in playerIds])

problem += lpSum([playerVariables[i] for i in playerIds]) == 11

problem.writeLP("FPL_Team_Problem.lp")

problem.solve()

print("Status:", LpStatus[problem.status])
for v in problem.variables():
    if v.varValue == 1.0:
        print(v.name, "=", v.varValue)
print("Total number of points achieved by the team = ", value(problem.objective))

if __name__ == '__main__':
    print('team optimiser ran successfully')
