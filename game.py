import random

import pygame

import accueil
import image


class Game:
    def __init__(self, alphabet_pixels):
        self.is_playing = False
        self.is_accueil = True

        self.pressed = {pygame.K_LSHIFT: False}

        self.player_name = "Nom"
        self.player_random_names = ['Romuald', 'Tyranocif', 'Ventilateur', 'Pissenlit', 'Guy le bandit', 'xXGamer-12Xx',
                                    "Moi c'est Kevin", 'Limonde']

        self.accueil = accueil.Accueil()
        self.classic_panel = image.ClassicGamePanel(self.player_name)
        self.classic_panel.def_alphabet_pixels(alphabet_pixels)

        self.all_starters = {'feu': ['Salameche', 'Poussifeu'],
                             'eau': ['Carapuce', 'Gobou'],
                             'plante': ['Bulbizarre', 'Arcko']}
        self.starters = [random.choice(self.all_starters['feu']),
                         random.choice(self.all_starters['eau']),
                         random.choice(self.all_starters['plante'])]

        self.save_file = open('save.txt', 'r+')

    def update(self, screen, possouris):

        if self.is_playing:
            self.classic_panel.update(screen, possouris)
            if self.classic_panel.change_player_name_mode:
                self.classic_panel.update_player_name(self.player_name)
        else:
            if self.is_accueil:
                self.accueil.update(screen)
            else:
                self.is_playing = True

    def reset_save_file(self):
        template = open('save_file_template.txt', 'r')
        template_lines = template.read()

        self.save_file.truncate()
        self.save_file.write(template_lines)

    def create_new_game(self):
        self.reset_save_file()
        print(self.starters)
