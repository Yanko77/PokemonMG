"""
Cleaning effectué
"""

import pygame

from panel import Panel


class Accueil:

    def __init__(self, game):
        self.game = game

        self.intro = Intro(self.game)
        self.homescreen = HomeScreen(self.game)

    def update(self, possouris):
        if not self.intro.end:
            self.intro.update()
        else:
            self.homescreen.update(possouris)

    def left_clic_interactions(self, possouris):
        if self.intro.end:
            self.homescreen.left_clic_interactions(possouris)

    def is_hovering_buttons(self, possouris):
        if self.intro.end:
            return self.homescreen.is_hovering_buttons(possouris)


class HomeScreen(Panel):

    def __init__(self, game):
        super().__init__(game=game,
                         path='assets/game/panels/accueil/home_screen/')

        # Variables pour animations
        self.fading = True
        self.compteur = -255

        # Images
        self.background = self.img_load('background')

        self.jouer_button = self.img_load('buttons/jouer')
        self.jouer_button_h = self.img_load('buttons/jouer_')

        self.parametres_button = self.img_load('buttons/parametres')
        self.parametres_button_h = self.img_load('buttons/parametres_')

        self.credits_button = self.img_load('buttons/credits')
        self.credits_button_h = self.img_load('buttons/credits_')

        self.quitter_button = self.img_load('buttons/quitter')
        self.quitter_button_h = self.img_load('buttons/quitter_')

        self.new_game_button = self.img_load('buttons/new_game')
        self.new_game_button_h = self.img_load('buttons/new_game_')

        self.load_game_button = self.img_load('buttons/load_game')
        self.load_game_button_h = self.img_load('buttons/load_game_')

        self.back_button = self.img_load('buttons/back')
        self.back_button_rect = pygame.Rect(810, 229, 59, 59)

        # Emplacements de boutons
        self.buttons_rect = [
            pygame.Rect(472, 293, 340, 56),
            pygame.Rect(472, 379, 340, 56),
            pygame.Rect(472, 465, 340, 56),
            pygame.Rect(472, 551, 340, 56)
        ]
        self.buttons = []

        self.page = ''

        self.pages_buttons = {
            'main': [
                (self.jouer_button, self.jouer_button_h, 'jouer'),
                (self.parametres_button, self.parametres_button_h, 'parametres'),
                (self.credits_button, self.credits_button_h, 'credits'),
                (self.quitter_button, self.quitter_button_h, 'quitter')
            ],
            'jouer': [
                (self.new_game_button, self.new_game_button_h, 'new_game'),
                (self.load_game_button, self.load_game_button_h, 'load_game'),
            ],
            'parametres': [],
            'credits': []
        }

        self.set_page('main')

    @property
    def is_main_page(self):
        return self.page == 'main'

    @property
    def end(self):
        return self.compteur >= 55

    def update(self, possouris):
        self.update_background()

        self.update_buttons(possouris)

        if not self.end:
            self.compteur += 1.5

    def update_background(self):
        if self.fading:
            if self.compteur < 0:
                self.background.set_alpha(255 + self.compteur)
            else:
                self.fading = False

        self.game.screen.blit(self.background, (0, 0))

    def update_buttons(self, possouris):

        i = 0
        for button in self.buttons:
            y = self.buttons_rect[i].y

            if self.compteur < 40:
                y += 40 - self.compteur

            if not self.end:
                button[0].set_alpha(self.compteur * 5)

            if self.buttons_rect[i].collidepoint(possouris) and self.end:
                self.game.screen.blit(button[1], (self.buttons_rect[i].x, y))
            else:
                self.game.screen.blit(button[0], (self.buttons_rect[i].x, y))

            i += 1

        # Back button
        if not self.is_main_page:
            if self.back_button_rect.collidepoint(possouris):
                self.game.screen.blit(self.back_button, self.back_button_rect, (59, 0, 59, 59))
            else:
                self.game.screen.blit(self.back_button, self.back_button_rect, (0, 0, 59, 59))

    def set_page(self, page_name):
        self.page = page_name
        self.buttons = self.pages_buttons[self.page]

        if self.end:
            self.compteur = 0

    def left_clic_interactions(self, possouris):
        if self.end:
            i = 0
            for button in self.buttons:
                if self.buttons_rect[i].collidepoint(possouris):
                    if button[2] in self.pages_buttons:
                        self.set_page(button[2])
                    else:
                        if button[2] == 'quitter':
                            pygame.event.post(pygame.event.Event(pygame.QUIT))
                        elif button[2] == 'new_game':
                            self.game.new_game()
                        elif button[2] == 'load_game':
                            self.game.load_game()

                i += 1

            if not self.is_main_page:
                if self.back_button_rect.collidepoint(possouris):
                    self.set_page('main')

    def is_hovering_buttons(self, possouris):
        if self.end:
            for i in range(len(self.buttons)):
                if self.buttons_rect[i].collidepoint(possouris):
                    return True

            if not self.is_main_page:
                if self.back_button_rect.collidepoint(possouris):
                    return True

        return False


class Intro:

    def __init__(self, game):
        self.game = game

        self.logo = pygame.image.load('assets/game/panels/accueil/intro/logo.png').convert_alpha()

        self.compteur = -150

    @property
    def end(self):
        return self.compteur >= 699

    def update(self):
        if self.compteur > 0:

            if self.compteur < 254:
                self.logo.set_alpha(self.compteur)
            elif 700 > self.compteur > 300:
                self.logo.set_alpha(555 - self.compteur)

            y = 200 - self.compteur
            if y < 0:
                y = 0

            self.game.screen.blit(self.logo, (0, y))

        self.compteur += 2
