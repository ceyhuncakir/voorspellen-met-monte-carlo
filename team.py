class Team:
    def __init__(self, name, chance):
        """
        initialiseert de team classen

        :param name: (str)
            de naam van het team
        :param chance: (str)
            dict met alle kansen voor all de teams
        """

        self.name = name
        self.chance = chance
        self.chance_list = self.chance_list()
        self.check_chance()

    def chance_list(self):
        """
        dit functie zet de chances in een lijst.

        :return: (dict)
            dict met alle chances
        """

        chances_list = {}

        for i in self.chance:
            chance_list = self.chance[i][0] * [0] + self.chance[i][1] * [1] + self.chance[i][2] * [2]
            chances_list[i] = chance_list

        return chances_list

    def check_chance(self):
        """
        dit functie bekijkt of de change gesumt 100 is. zo niet throwdt die een value error
        """
        for i in self.chance:
            if sum(self.chance[i]) != 100:
                raise ValueError('chance gesumt is niet 100%')
