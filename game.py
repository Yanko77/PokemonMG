import random

import fight
import objet
import starters
import csv
from player import Player
from notif import Notif

import pygame
import accueil
from game_panel import GamePanel
from fight import Fight
from game_round import Round


class Game:
    def __init__(self):
        self.is_playing = False
        self.is_accueil = True
        self.is_fighting = False

        self.is_starter_selected = False

        self.pressed = {pygame.K_LSHIFT: False}
        self.mouse_pressed = {1: False,
                              3: False}

        self.items_list = self.get_all_items_list()
        self.pokemons_list = self.init_pokemons_list()
        self.special_pokemons_list = self.init_special_pokemons_list()

        self.player = Player(self)

        self.accueil = accueil.Accueil(self)

        self.next_pk_id = 1

        self.all_starters = {'feu': ['Salameche', 'Poussifeu'],
                             'eau': ['Carapuce', 'Gobou'],
                             'plante': ['Bulbizarre', 'Arcko']}
        self.starters = [random.choice(self.all_starters['plante']),
                         random.choice(self.all_starters['feu']),
                         random.choice(self.all_starters['eau'])
                         ]

        self.starter_panel = starters.StarterPanel(self)

        self.classic_panel = GamePanel(self)
        self.round = Round(self)
        self.notifs = Notif()

        self.general_seed = self.round.get_random_seed()

        self.next_fighting_dresseur = self.get_fighting_dresseur()

        self.current_fight = None

        self.bool_game_over = False

    def update(self, screen, possouris):

        if self.is_playing:
            if self.is_starter_selected:
                if self.is_fighting:
                    self.current_fight.update(screen, possouris)
                else:
                    self.classic_panel.update(screen, possouris)
            else:
                self.starter_panel.update(screen, possouris)
        else:
            if self.is_accueil:
                self.accueil.update(screen, possouris)
            else:
                self.is_playing = True

        # Affichage des notifications
        self.notifs.update(screen)

    def notif(self, text, color):
        self.notifs.new_notif(text, color)

    def get_fighting_dresseur(self):
        r = random.Random()
        # return r.choice(fight.DRESSEUR_LIST)(self)
        return fight.Red(self)

    def init_new_game(self):
        self.is_starter_selected = False

    def create_new_game(self):
        self.init_new_game()

    def start_new_game(self):
        self.is_accueil = False
        self.create_new_game()

    def game_over(self):
        self.__init__()

    def start_fight(self, player_pk, dresseur=None, difficult="easy", fight_type='Classic'):
        if fight_type == 'Classic':
            self.init_fight(player_pk, dresseur, difficult, fight_type)
            self.is_fighting = True
        elif fight_type == 'Boss':
            self.init_fight(player_pk, self.next_fighting_dresseur, difficult, fight_type)
            self.is_fighting = True

    def cancel_fight(self):
        self.current_fight = None
        self.is_fighting = False

    def end_fight(self):
        if self.current_fight.fight_type == 'Boss':
            self.next_turn()
        self.current_fight = None
        self.is_fighting = False

    def init_fight(self, player_pk, dresseur=None, difficult='easy', fight_type='Classic'):
        self.current_fight = Fight(self, player_pk, dresseur, difficult, fight_type)

    def next_turn(self):
        self.round.next()
        self.update_random_seed()
        self.player.reset_actions()
        self.player.level_up()
        self.classic_panel.next_turn()
        self.next_fighting_dresseur = self.get_fighting_dresseur()
        # add everything that have to be edited for each turn

    def get_init_pokemon_id(self):
        id = self.next_pk_id
        self.next_pk_id += 1
        return id

    def init_items_list(self):
        with open('all_objets.txt', 'r') as file:
            items_list = []
            for line in file.readlines():
                item_name = line.split()[0]
                if not item_name == '#':
                    items_list.append(objet.Objet(item_name))

            return items_list

    def get_all_items_list(self):
        """
        Retourne le dict: {
            'All': all_items
            'Use': use_items,
            'Give': give_items,
            'Sell': sell_items,
            'Enable': enable_items,
            'Spawnble': spawnable_items
             }

        :return: items_list, dict
        """

        items_list = {
            'All': [],
            'Use': [],
            'Give': [],
            'Sell': [],
            'Enable': [],
            'Spawnable': [],
        }
        for item in self.init_items_list():
            items_list['All'].append(item)
            if item.fonctionnement.split(":")[0] == 'Use':
                items_list['Use'].append(item)
            elif item.fonctionnement.split(":")[0] == 'Give':
                items_list['Give'].append(item)
            elif item.fonctionnement.split(":")[0] == 'Sell':
                items_list['Sell'].append(item)
            elif item.fonctionnement.split(":")[0] == 'Enable':
                items_list['Enable'].append(item)
            if item.boolSpawnable:
                items_list['Spawnable'].append(item)

        return items_list

    def get_items_list(self):
        return self.items_list

    def init_pokemons_list(self):
        with open('all_pokemons.csv', newline='') as file:
            pokemons_list = {}
            lines = csv.reader(file, delimiter=' ', quotechar='|')
            for line in lines:
                if line[0] not in (" ", "", "NAME", "Moyennes"):

                    pokemons_list[line[0]] = (
                        line[0],  # NAME
                        int(line[1]),  # RARITY
                        line[2],  # TYPE
                        int(line[3]),  # PV
                        int(line[4]),  # ATK
                        int(line[5]),  # DEF
                        int(line[6]),  # SPEED
                        int(line[7]),  # EVOLUTION LEVEL
                        line[8],  # EVOLUTION NAME
                        int(line[9]),  # MIN PLAYER LEVEL TO SPAWN
                        line[10],  # TYPE 2
                        int(line[11]),  # MIN LEVEL ON SPAWN
                        int(line[12]),  # MAX LEVEL ON SPAWN
                    )
            print(pokemons_list)
            return pokemons_list

    def init_special_pokemons_list(self):
        with open('special_pokemons.csv', newline='') as file:
            pokemons_list = {}
            lines = csv.reader(file, delimiter=',', quotechar='|')
            for line in lines:
                if line[0] not in (" ", "", "NAME", "Moyennes"):

                    pokemons_list[line[0]] = (
                        line[0],  # NAME
                        int(line[1]),  # RARITY
                        line[2],  # TYPE
                        int(line[3]),  # PV
                        int(line[4]),  # ATK
                        int(line[5]),  # DEF
                        int(line[6]),  # SPEED
                        int(line[7]),  # EVOLUTION LEVEL
                        line[8],  # EVOLUTION NAME
                        int(line[9]),  # MIN PLAYER LEVEL TO SPAWN
                        line[10],  # TYPE 2
                        int(line[11]),  # MIN LEVEL ON SPAWN
                        int(line[12]),  # MAX LEVEL ON SPAWN
                    )
            print(pokemons_list)
            return pokemons_list

    def get_total_items_rarity(self):
        """
        Methode qui renvoie la somme de toutes les raretés des objets du jeu obtenable via spawn
        """
        total_rarity = 0
        for OBJECT in self.get_items_list()['Spawnable']:
            total_rarity += abs(OBJECT.rarity - 100)
        return total_rarity

    def update_random_seed(self):
        self.general_seed = self.round.get_random_seed()

    def save(self):
        pass


if __name__ == '__main__':
    game = Game()
    game.init_pokemons_list()
