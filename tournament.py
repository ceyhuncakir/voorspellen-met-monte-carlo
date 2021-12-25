from team import *
from termcolor import colored
import numpy as np
from tabulate import tabulate

class Tournament:
    def __init__(self, n, teams, random_number_generator):
        """
        initialisatie van de tournament klassen

        :param teams: (list)
            een lijst met teams
        :param n: (int)
            geeft aan hoevaak de tournament simulatie gerunt moet worden
        :param random_number_generator: random number generator
            object om nummers te genereren
        """
        self.teams = teams
        self.matches = []
        self.schedule_matches()
        self.results = self.initialize_results()
        self.random_number_generator = random_number_generator
        self.n = n
        self.all_results = {}
        self.n = n

    def initialize_results(self):
        """
        dit functie zorgt er voor dat alle resultaten voor de teams gehouden kunnen worden

        :return: (dict)
            een lege dict met alle teams
        """
        results = {}
        for team in self.teams:
            results[team.name] = 0
        return results

    def schedule_matches(self):
        """
        dit functie zorgt er voor dat alle mogelijke matchups gemaakt kunnen worden tussen teams
        """
        for team in self.teams:
            for other_team in self.teams:
                if team != other_team:
                    match = [team, other_team]
                    self.matches.append(match)

    def play_all_matches(self):
        """
        dit functie zorgt er voor dat alle teams met alle mogelijke combinaties tegen elkaar kunnen spelen
        """
        for match in self.matches:
            home = match[0]
            away = match[1]
            self.play_match(home, away)

    def play_match(self, home, away):
        """
        dit functie zorgt er voor dat er een game gespeelt kan worden tussen twee teams

        :param home: (team)
            de team dat thuis speelt
        :param away: (team)
            de team die uit speelt
        """
        result = home.chance_list[away.name][self.random_number_generator.randomly()]
        # 0 = Home win
        # 1 = Draw
        # 2 (else) = Away wins
        if result == 0:
            self.results[home.name] += 3
        elif result == 1:
            self.results[home.name] += 1
            self.results[away.name] += 1
        else:
            self.results[away.name] += 3

    def batch_execute(self):
        """
        dit functie zorgt er voor dat er een batch aan simulaties gerunned kunnen worden
        """
        for i in range(self.n):
            self.play_all_matches()
            self.parse_results(i)
            self.results = self.initialize_results()

    def tournament_results(self):
        """
        dit functie laat alle wedstrijd resultaten zien
        """
        tournaments_played = len(self.all_results)
        headers = [colored(position + 1, "green") + colored("e positie", "green") for position in range(len(self.teams))]
        places = {}
        table = []

        for position in range(len(self.teams)):
            places[position] = []

        for result in self.all_results:
            for positie in range(len(self.all_results[result])):
                places[positie].append(self.all_results[result][positie])

        for team in self.teams:
            table_row = [colored(team.name, "yellow")]
            for j in places:
                table_row.append(f'{round(places[j].count(team.name) / tournaments_played * 100, 2)}%')
            table.append(table_row)

        print(tabulate(table, headers=headers), "\n")

    def parse_results(self, run):
        """
        dit functie parsed de tournament uitslagen

        :param run: (int)
            het getal
        """
        tournament_result = {key: value for key, value in sorted(self.results.items(), key=lambda item: item[1], reverse=True)}
        self.all_results[run] = list(tournament_result.keys())
