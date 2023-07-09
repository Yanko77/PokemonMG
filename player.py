import pygame
from pokemon import Pokemon


class Player:

    def __init__(self):
        self.level = 0
        self.name = "Nom"

        self.team = [None, None, None, None, None, None]

    def evol_pk(self, i=0):
        self.team[i] = self.team[i].evolution()


if __name__ == "__main__":

    player = Player()
    player.evol_pk()