"""
Fichier gérant le joueur.
"""

# Importation des modules

import pygame.key

import objet
import pokemon
from objet import Objet

# Définition des classes


class Player:
    """
    Classe représentant le joueur.
    """

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

        self.money = 10000000

    def edit_name(self, key):
        """
        Méthode d'édition du nom du joueur.

        @in : key, int → valeur associée à la touche appuyée. Voir pygame.key.
        """
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
        """
        Méthode de réinitialisation du nom du joueur.
        """
        self.name = ""
        self.game.classic_panel.update_player_name()

    def reset_actions(self):
        """
        Méthode de réinitialisation du nombre d'actions.
        """
        self.actions = self.max_actions

    def swap_sac_items(self, i1, i2):
        """
        Fonction qui echange la place de 2 items dans le sac.

        @in : i1, int → indice de l'objet 1 dans le sac
        @in : i2, int → indice de l'objet 2 dans le sac
        """
        if not i1 == i2:
            self.sac[i1 - 1], self.sac[i2 - 1] = self.sac[i2 - 1], self.sac[i1 - 1]

    def find_sac_item(self, item):
        """
        Methode qui renvoie l'index de l'item recherché dans le sac.
        Renvoie None s'il n'est pas présent.

        @in : item, objet.Objet
        @out: i, int ;
              None
        """

        for i in range(len(self.sac)):
            sac_item = self.sac[i]

            if sac_item is not None:
                if sac_item.name == item.name:
                    return i

    def find_sac_item_by_str(self, item_name):
        """
        Methode qui renvoie l'index de l'item recherché dans le sac à partir de son nom.
        Renvoie None s'il n'est pas présent;

        @in : item, objet.Objet
        @out: i, int ;
              None
        """

        for i in range(len(self.sac)):
            sac_item = self.sac[i]

            if sac_item is not None:
                if sac_item.name == item_name:
                    return i

    def add_sac_item(self, item):
        """
        Fonction qui ajoute au sac un objet et qui le stack si possible.

        @in : item, objet.Objet
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
            self.sac[item_place].quantite += item.quantite

    def remove_item_sac(self, index):
        """
        Retire un objet du sac.
        Ne tient pas compte de la quantité de l'objet.

        @in : index, int → indice de l'objet dans le sac.
        """

        self.sac[index] = None

    def add_team_pk(self, pk, i=0):
        """
        Méthode qui ajoute un pokémon à l'équipe.

        Essaye de le placer à l'indice voulu.
        Si c'est impossible, le place à la suite.
        Si c'est impossible, ne fait rien.

        @in : pk, pokemon.Pokemon
        @in: i, int → indice voulu
        """
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
        """
        Méthode d'utilisation de points d'actions.
        Le nombre de points d'actions est pris en parametre d'entrée.

        @in : amount, int
        """
        self.actions -= amount

        if amount > 1:
            text = f'{amount} actions utilisées'
        else:
            text = f'{amount} action utilisée'

        self.game.notif(text=text, color=(225, 0, 0))

    def payer(self, price: int) -> bool:
        """
        Methode qui permet au joueur de payer la somme rentrée en paramètre d'entrée.
        Renvoie True s'il a payé, False sinon.

        @in : price, int
        """
        if self.money >= price:
            self.money -= price
            return True
        else:
            return False

    def level_up(self, nb_lv=1):
        """
        Méthode d'augmentation du niveau du joueur.

        @in : nb_lv, int → Nombre de niveau d'augmentation du joueur voulu.
        """
        self.level += nb_lv

    def add_money(self, amount):
        """
        Méthode d'ajout d'argent au porte-monnaie du joueur.

        @in : amount, int → Valeur ajoutée
        """
        self.money += amount

    def rise_max_actions_value(self, amount):
        """
        Méthode d'augmentation du nombre d'actions maximum réalisables par tour.

        @in : amount, int
        """
        self.max_actions += amount
        self.actions += amount

    def get_nb_team_members(self):
        """
        Méthode qui retourne le nombre de pokémon présent dans l'équipe.
        """
        nb_team_members = 0
        for member in self.team:
            if member is not None:
                nb_team_members += 1

        return nb_team_members

    def is_team_empty(self):
        """
        Retourne True si l'équipe est vide, False sinon.

        @out : bool
        """
        if self.get_nb_team_members() == 0:
            return True
        return False

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
        Methode qui éxécute toutes les modifications dues au changement de tour de jeu
        """
        self.reset_actions()
        self.level_up()
        if self.find_sac_item(objet.Objet("Piquants", self.game)) is not None:
            self.money -= 1000

        for item in self.sac:
            if item is not None:
                item.set_sell_price()

