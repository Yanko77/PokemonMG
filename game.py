import random

import pygame

import accueil
import image


class Game:
    def __init__(self):
        self.is_playing = False
        self.is_accueil = True

        self.pressed = {pygame.K_LSHIFT: False}

        self.player_name = "Nom"
        self.change_player_name_mode = False

        self.accueil = accueil.Accueil()
        self.classic_panel = image.ClassicGamePanel(self.player_name)

        self.all_starters = {'feu': ['Salameche', 'Poussifeu'],
                             'eau': ['Carapuce', 'Gobou'],
                             'plante': ['Bulbizarre', 'Arcko']}
        self.starters = [random.choice(self.all_starters['feu']),
                         random.choice(self.all_starters['eau']),
                         random.choice(self.all_starters['plante'])]

        self.save_file = open('save.txt', 'r+')

    def update(self, screen):

        if self.is_playing:
            self.classic_panel.update(screen)
            if self.change_player_name_mode:
                self.classic_panel.update_player_name(self.player_name)
                screen.blit(self.classic_panel.mode_changement_pseudo_image, (0, 0))
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
