"""
Cleaning effectué
"""


import pygame

from notif import Notif
from accueil import Accueil
from starter_picking import StarterPicking
from main_panel import MainPanel
from player import Player


class Game:

    def __init__(self, screen):
        self.screen: pygame.Surface = screen

        self.is_playing = False
        self.is_accueil = True
        self.is_picking_starter = False

        self.pressed = {
            pygame.K_LSHIFT: False
        }

        self.mouse_pressed = {
            1: False,
            3: False
        }

        self.player = Player(self)

        self._notif = None
        self.accueil = Accueil(self)
        self.starter_picking = StarterPicking(self)
        self.main_panel = MainPanel(self)

    def update(self, possouris):

        if self.is_accueil:
            self.accueil.update(possouris)
        elif self.is_picking_starter:
            self.starter_picking.update(possouris)
        elif self.is_playing:
            self.main_panel.update(possouris)

        self.update_notifs()
        self.update_cursor(possouris)

    def update_notifs(self):
        if self._notif is not None:
            self._notif.update()

            if self._notif.end:
                self._notif = None

    def update_cursor(self, possouris):
        if self.is_hovering_buttons(possouris):
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def notif(self, text, color=(0, 0, 0), duration=3):
        self._notif = Notif(self, text, color, duration)

    def new_game(self):
        self.is_accueil = False
        self.is_picking_starter = True

    def left_clic_interactions(self, possouris):
        if self.is_accueil:
            self.accueil.left_clic_interactions(possouris)
        elif self.is_picking_starter:
            self.starter_picking.left_clic_interactions(possouris)

    def is_hovering_buttons(self, possouris):
        if self.is_accueil:
            return self.accueil.is_hovering_buttons(possouris)
        elif self.is_picking_starter:
            return self.starter_picking.is_hovering_buttons(possouris)
        elif self.is_playing:
            return False
