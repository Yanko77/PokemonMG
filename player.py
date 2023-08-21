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
        self.sac_page1 = [Objet('Poke_Ball', 3),
                          Objet('Super_Bonbon', 3),
                          Objet('PV_Plus', 2),
                          Objet('Collier_Agathe', 2),
                          Objet('Potion', 2),
                          Objet('Hyper_Potion', 2),
                          Objet('Potion_Max', 2),
                          Objet('PV_Plus', 2),
                          Objet('Proteine', 2),
                          Objet('Fer', 2),
                          Objet('Carbone', 2),
                          Objet('Eau_Fraiche', 2)]
        self.sac_page2 = [None,
                          None,
                          None,
                          None,
                          None,
                          None,
                          None,
                          None,
                          None,
                          None,
                          None,
                          None]

        self.money = 1000

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

    def is_sac_page_full(self, page_num):
        sac_page = self.sac_page1
        if page_num == 1:
            sac_page = self.sac_page1
        elif page_num == 2:
            sac_page = self.sac_page2

        for objet in sac_page:
            if objet is None:
                return False

        return True

    def get_sac_empty_emp(self, page_num):
        sac_page = self.sac_page1
        if page_num == 1:
            sac_page = self.sac_page1
        elif page_num == 2:
            sac_page = self.sac_page2

        empty_emp_i = 0
        for emp in sac_page:
            if emp is None:
                return empty_emp_i

            empty_emp_i += 1

if __name__ == "__main__":

    player = Player()
    player.evol_pk()
