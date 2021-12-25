from tournament import *
from team import *
from mersennetwister import *
import json

data_result = open('data/teams.json')
chance = json.load(data_result)

def create_teams():
    teams = []

    for i in chance:
        team = Team(i, chance[i])
        teams.append(team)

    return teams

teams = create_teams()

tour = Tournament(10000, teams, Mersenne())
tour.batch_execute()
tour.tournament_results()
