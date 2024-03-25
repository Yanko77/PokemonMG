import pygame.key

import objet
import player_name
import pokemon
from objet import Objet


class Player:

    def __init__(self, game):
        self.game = game

        self.level = 0
        self.name = "Nom"

        self.actions = 3
        self.max_actions = 3

        self.always_shiny_on = False

        self.team = [None,
                     None,
                     None,
                     None,
                     None,
                     None]

        self.sac = [None,
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
                    None,
                    None,
                    None]

        self.money = 1000

    def edit_name(self, key):
        if self.game.pressed[pygame.K_LSHIFT]:
            character = pygame.key.name(key).upper()
        else:
            character = pygame.key.name(key)

        if character in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" and self.game.classic_panel.player_name_text.get_width() < 385:
            self.name += character
        elif character == "backspace":
            self.name = self.name[:-1]
        elif character == "space":
            self.name += " "

        self.game.classic_panel.update_player_name()

    def reset_name(self):
        self.name = ""
        self.game.classic_panel.update_player_name()

    def reset_actions(self):
        self.actions = self.max_actions

    def evol_pk(self, i=0):
        if self.team[i] is not None:
            self.team[i] = self.team[i].evolution()

    def swap_sac_items(self, i1, i2):
        """
        Fonction qui echange la place de 2 items dans le sac
        """
        if not i1 == i2:
            self.sac[i1 - 1], self.sac[i2 - 1] = self.sac[i2 - 1], self.sac[i1 - 1]

    def find_sac_item(self, item):
        """
        Methode qui renvoie l'index de l'item recherché dans le sac.
        Renvoie None s'il n'est pas présent
        """

        for i in range(len(self.sac)):
            sac_item = self.sac[i]

            if sac_item is not None:
                if sac_item.name == item.name:
                    return i

    def add_sac_item(self, item):
        """
        Fonction qui ajoute au sac un objet et qui le stack si possible
        """

        item_place = self.find_sac_item(item)

        if item_place is None:  # Si l'item n'est pas déjà présent dans le sac
            i = 0
            while i < len(self.sac) and self.sac[i] is not None:

                if i == len(self.sac) - 1 and self.sac[i] is not None:
                    i = 100
                else:
                    i += 1

            if i != 100:
                self.sac[i] = objet.Objet(item.name, self.game, item.quantite)

        else:
            print(item.quantite)
            self.sac[item_place].quantite += item.quantite

    def add_team_pk(self, pk, i=0):
        if self.get_nb_team_members() < 6:
            if self.team[i] is None:
                self.team[i] = pk
            else:
                i = 0
                place_found = False
                while not place_found and i < 6:
                    if self.team[i] is None:
                        self.team[i] = pk
                        place_found = True

                    i += 1

    def use_action(self, amount=1):
        self.actions -= amount

        if amount > 1:
            text = f'{amount} actions utilisées'
        else:
            text = f'{amount} action utilisée'

        self.game.notif(text=text, color=(225, 0, 0))

    def payer(self, price: int) -> bool:
        """
        Methode qui permet au joueur de payer
        Renvoie True s'il a payé, False sinon
        """
        if self.money >= price:
            self.money -= price
            return True
        else:
            return False

    def level_up(self, nb_lv=1):
        self.level += nb_lv

    def add_money(self, amount):
        self.money += amount

    def rise_max_actions_value(self):
        self.max_actions += 1
        self.actions += 1

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

    def get_moyenne_team(self):
        levels_list = []
        for pk in self.team:
            if pk is not None:
                levels_list.append(pk.get_level())

        if not levels_list:
            return 0
        else:
            return sum(levels_list) // len(levels_list)

    def get_level(self):
        return self.level

    def get_actions(self):
        return self.actions

    def get_max_actions(self):
        return self.max_actions

    def get_money(self):
        return self.money

    def next_turn(self):
        """
        Methode qui execute toutes les modifications dues au changement de tour de jeu
        """
        self.reset_actions()
        self.level_up()
        if self.find_sac_item(objet.Objet("Piquants", self)) is not None:
            self.money -= 1000

        for item in self.sac:
            if item is not None:
                item.set_sell_price()




if __name__ == "__main__":
    player = Player()
