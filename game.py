import random

import fight
import objet
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

        self.player = Player(self)

        self.accueil = accueil.Accueil()

        self.next_pk_id = 1

        self.all_starters = {'feu': ['Salameche', 'Poussifeu'],
                             'eau': ['Carapuce', 'Gobou'],
                             'plante': ['Bulbizarre', 'Arcko']}
        self.starters = [random.choice(self.all_starters['plante']),
                         random.choice(self.all_starters['feu']),
                         random.choice(self.all_starters['eau'])
                         ]

        self.classic_panel = GamePanel(self)
        self.round = Round(self)
        self.notifs = Notif()

        self.save_file = open('save.txt', 'r+')

        self.general_seed = self.round.get_random_seed()
        self.items_list = self.get_all_items_list()

        self.next_fighting_dresseur = self.get_fighting_dresseur()

        self.current_fight = None

    def update(self, screen, possouris):

        if self.is_playing:
            if self.is_fighting:
                self.current_fight.update(screen, possouris)
            else:
                self.classic_panel.update(screen, possouris)
        else:
            if self.is_accueil:
                self.accueil.update(screen)
            else:
                self.is_playing = True

        # Affichage des notifications
        self.notifs.update(screen)

    def notif(self, text, color):
        self.notifs.new_notif(text, color)

    def get_fighting_dresseur(self):
        r = random.Random()
        return r.choice(fight.DRESSEUR_LIST)(self)

    def init_new_game(self):
        self.is_starter_selected = False
        self.classic_panel.ingame_window.update_panel('Starters')
        self.classic_panel.ingame_window.minimize()
        self.classic_panel.ingame_window.open()

    def reset_save_file(self):
        template = open('save_file_template.txt', 'r')
        template_lines = template.read()

        self.save_file.truncate()
        self.save_file.write(template_lines)

    def create_new_game(self):
        self.init_new_game()
        self.reset_save_file()
        print(self.starters)

    '''def load_game(self):
        self.save_file'''

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


if __name__ == '__main__':
    game = Game()
    for list_name in game.items_list.keys():
        for item in game.items_list[list_name]:
            print(item.name, f'({list_name})')
