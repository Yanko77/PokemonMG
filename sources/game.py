import pygame

from notif import Notif
from accueil import Accueil


class Game:

    def __init__(self, screen):
        self.screen = screen

        self.is_playing = False
        self.is_accueil = True
        self.is_fighting = False

        self.pressed = {
            pygame.K_LSHIFT: False
        }

        self.mouse_pressed = {
            1: False,
            3: False
        }

        self._notif = None
        self.accueil = Accueil(self)

    def update(self, possouris):
        if not self.is_playing:
            self.accueil.update(possouris)
        else:
            pass

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

    def left_clic_interactions(self, possouris):
        if self.is_accueil:
            self.accueil.left_clic_interactions(possouris)

    def is_hovering_buttons(self, possouris):
        if self.is_accueil:
            return self.accueil.is_hovering_buttons(possouris)
