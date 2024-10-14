"""
Cleaning effectué
"""


import pygame
from config import FPS


NOTIF_FONT = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 40)
NOTIF_TEXT_MARGE = 5
NOTIF_RECT_MARGE = 5


class Notif:

    def __init__(self, game, text, color=(0, 0, 0), duration=3):
        self.game = game

        self.text = NOTIF_FONT.render(text, False, color).convert_alpha()

        self.rect = pygame.Rect(
            self.game.screen.get_width() - self.text.get_width() - NOTIF_RECT_MARGE - NOTIF_TEXT_MARGE*2,
            NOTIF_RECT_MARGE,
            self.text.get_width() + NOTIF_TEXT_MARGE * 2,
            self.text.get_height() + NOTIF_TEXT_MARGE * 2
        )

        self.text_rect = pygame.Rect(
            self.game.screen.get_width() - self.text.get_width() - NOTIF_RECT_MARGE - NOTIF_TEXT_MARGE,
            NOTIF_RECT_MARGE + NOTIF_TEXT_MARGE,
            self.text.get_width() + NOTIF_TEXT_MARGE,
            self.text.get_height() + NOTIF_TEXT_MARGE
        )

        self.duration = duration

        self.fading_up = False
        self.fading_down = False

        self.alpha = 0
        self.start_fade()

    @property
    def end(self):
        return self.duration < 0

    def update(self):
        self.update_fading()

        self.game.screen.blit(self.render(), (0, 0))

        self.duration -= 1 / FPS

    def update_fading(self):
        if self.fading_up:
            self.alpha += 255 / FPS
            if self.alpha >= 255:
                self.fading_up = False

        elif self.fading_down:
            self.alpha -= 255 / FPS
            if self.alpha <= 255:
                self.fading_up = False

        if self.duration <= 1:
            self.start_fade()

    def start_fade(self):
        if self.alpha == 0:
            self.fading_up = True
        else:
            self.fading_down = True

    def render(self):
        surface = pygame.Surface(self.game.screen.get_size(), pygame.SRCALPHA)

        # surface.set_colorkey((0, 0, 1))
        # surface.fill((0, 0, 1))

        notif_background = pygame.Surface(self.rect.size).convert_alpha()
        notif_background.fill((255, 255, 255))

        notif_background.set_alpha(self.alpha)
        self.text.set_alpha(self.alpha)

        surface.blit(notif_background, self.rect)
        surface.blit(self.text, self.text_rect)

        return surface
