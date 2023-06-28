import pygame
pygame.font.init()
import image


class IngameWindow:

    def __init__(self):
        self.is_open = False
        self.is_minimized = False

        self.basic_window = pygame.image.load('assets/game/ingame_windows/basic/main.png')

        self.main_window_rect = self.basic_window.get_rect()
        # self.main_window_rect.x =

        self.main_window_pos = (1, 1)

        self.buttons = image.IngameWindowButtons()

    def update(self, surface, possouris):
        self.update_main_window_rect()

        if self.is_open:
            if not self.is_minimized:
                surface.blit(self.basic_window, self.main_window_rect)
                self.buttons.update(surface, possouris)

            # else:

    def is_hovering_buttons(self, posouris):
        if self.buttons.is_hovering_buttons(posouris):
            return True
        return False

    def update_main_window_rect(self):
        if self.is_open:
            if self.is_minimized:
                ...
            else:
                self.main_window_rect = self.basic_window.get_rect()
        else:
            self.main_window_rect = pygame.Rect(0, 0, 0, 0)

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False
