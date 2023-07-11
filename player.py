import pygame
from pokemon import Pokemon


class Player:

    def __init__(self):
        self.level = 0
        self.name = "Nom"

        self.team = [Pokemon('arcko', 100), Pokemon('gobou', 100), Pokemon('poussifeu', 100), Pokemon('poussifeu', 100), Pokemon('poussifeu', 5), Pokemon('poussifeu', 5)]
        self.sac_page1 = [None, None, None, None, None, None, None, None, None, None, None, None]
        self.sac_page2 = [None, None, None, None, None, None, None, None, None, None, None, None]

    def evol_pk(self, i=0):
        self.team[i] = self.team[i].evolution()


if __name__ == "__main__":

    player = Player()
    player.evol_pk()
