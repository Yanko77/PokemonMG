import pygame
from pokemon import Pokemon
import spawn
from objet import Objet


class Player:

    def __init__(self):
        self.level = 0
        self.name = "Nom"

        self.team = [None,
                     None,
                     None,
                     None,
                     None,
                     None]
        self.sac_page1 = [None, None, None, None, None, None, Objet('CD'), None, None, None, None, None]
        self.sac_page2 = [None, None, None, None, None, None, None, None, None, None, None, None]

    def evol_pk(self, i=0):
        if self.team[i] is not None:
            self.team[i] = self.team[i].evolution()

    def get_nb_team_members(self):
        nb_team_members = 0
        for member in self.team:
            if member is not None:
                nb_team_members += 1

        return nb_team_members

    def is_team_empty(self):
        if self.get_nb_team_members() == 0:
            return True
        return False


if __name__ == "__main__":

    player = Player()
    player.evol_pk()
