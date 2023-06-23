import pygame
from pokemon import Pokemon


class Player:

    def __init__(self):
        self.team = [Pokemon('salameche', 12)]

    def evol_pk(self, i=0):
        self.team[i] = self.team[i].evolution()
        print(self.team[i].get_stats())


if __name__ == "__main__":

    player = Player()
    player.evol_pk()