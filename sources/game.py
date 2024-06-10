import pygame

from notif import Notif


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

    def update(self, possouris):
        self.update_notifs()

    def update_notifs(self):
        if self._notif is not None:
            self._notif.update()

            if self._notif.end:
                self._notif = None

    def notif(self, text, color=(0, 0, 0), duration=3):
        self._notif = Notif(self, text, color, duration)
