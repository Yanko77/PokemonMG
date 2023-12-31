import random
from player import Player

import pygame

import accueil
import panels
from game_round import Round


class Game:
    def __init__(self):
        self.is_playing = False
        self.is_accueil = True

        self.is_starter_selected = False

        self.pressed = {pygame.K_LSHIFT: False}
        self.mouse_pressed = {1: False,
                              3: False}

        self.player = Player()
        self.player_random_names = ['Romuald', 'Tyranocif', 'Ventilateur', 'Pissenlit', 'Guy le bandit', 'xXGamer-12Xx',
                                    "Moi c'est Kevin", 'Limonde']

        self.accueil = accueil.Accueil()

        self.all_starters = {'feu': ['Salameche', 'Poussifeu'],
                             'eau': ['Carapuce', 'Gobou'],
                             'plante': ['Bulbizarre', 'Arcko']}
        self.starters = [random.choice(self.all_starters['plante']),
                         random.choice(self.all_starters['feu']),
                         random.choice(self.all_starters['eau'])
                         ]

        self.classic_panel = panels.ClassicGamePanel(self)
        self.round = Round()

        self.save_file = open('save.txt', 'r+')

    def update(self, screen, possouris):

        if self.is_playing:
            self.classic_panel.update(screen, possouris)
        else:
            if self.is_accueil:
                self.accueil.update(screen)
            else:
                self.is_playing = True

    def init_new_game(self):
        self.is_starter_selected = False
        self.classic_panel.ingame_window.update_name('Starters')
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

    def player_lv_up(self):
        self.player.level += 1
        self.classic_panel.update_player_lv()
