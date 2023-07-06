import pygame
pygame.font.init()
import image


class IngameWindow:

    def __init__(self, name):
        self.is_open = False
        self.is_minimized = False

        self.window_pos_modif_mode = False

        self.name = name[0].upper() + name[1:].lower()

        self.basic_window = pygame.image.load('assets/game/ingame_windows/basic/main.png')
        self.basic_window_pos = [1, 1]

        self.basic_window_rect = self.basic_window.get_rect()
        self.basic_window_rect.x = 20 + self.basic_window_pos[0]
        self.basic_window_rect.y = 0 + self.basic_window_pos[1]
        self.basic_window_rect.w = 870
        self.basic_window_rect.h = 528

        self.basic_window_bar_rect = pygame.Rect(20, 0, 870, 39)

        self.min_window = pygame.image.load('assets/game/ingame_windows/basic/min_main.png')
        self.min_window_pos = [22, 675]

        self.min_window_rect = self.min_window.get_rect()
        self.min_window_rect.x = self.min_window_pos[0]
        self.min_window_rect.y = self.min_window_pos[1]

        self.main_window_rect = self.basic_window.get_rect()
        self.main_window_rect.x = 20
        self.main_window_rect.w = 872
        self.main_window_rect.h = 528

        self.main_window_bar_rect = self.basic_window_bar_rect

        self.main_window_pos = [1, 1]

        self.buttons = image.IngameWindowButtons()

        self.title_font = pygame.font.Font('assets/fonts/Impact.ttf', 30)
        self.title = self.title_font.render(self.name, False, (0, 0, 0))

    def update(self, surface, possouris):
        self.update_main_window_rect()

        if self.is_open:
            if self.is_minimized:
                surface.blit(self.min_window, self.main_window_pos)
            else:
                surface.blit(self.basic_window, self.main_window_pos)
                surface.blit(self.title, (self.main_window_pos[0] + 75, self.main_window_pos[1] + 0))
                self.buttons.update(surface, possouris)

    def is_hovering_buttons(self, posouris):
        if self.buttons.is_hovering_buttons(posouris):
            return True
        return False

    def update_main_window_rect(self):
        if self.is_open:
            if self.is_minimized:
                self.main_window_rect = self.min_window.get_rect()
                self.main_window_rect.x = self.min_window_pos[0]
                self.main_window_rect.y = self.min_window_pos[1]
                self.main_window_pos = self.min_window_pos

                self.main_window_bar_rect = pygame.Rect(0, 0, 0, 0)
            else:
                self.main_window_rect = self.basic_window.get_rect()
                self.main_window_rect.x = 20 + self.main_window_pos[0]
                self.main_window_rect.y = 0 + self.main_window_pos[1]
                self.main_window_rect.w = 870
                self.main_window_rect.h = 528
                self.main_window_pos = self.basic_window_pos

                self.main_window_bar_rect = pygame.Rect(20+self.main_window_pos[0], 0+self.main_window_pos[1], 870, 39)
                self.buttons.x_button_rect.x = 854 + self.main_window_pos[0]
                self.buttons.x_button_rect.y = 4 + self.main_window_pos[1]
                self.buttons.min_button_rect.x = 816 + self.main_window_pos[0]
                self.buttons.min_button_rect.y = 4 + self.main_window_pos[1]
        else:
            self.main_window_rect = pygame.Rect(0, 0, 0, 0)
            self.main_window_bar_rect = pygame.Rect(0, 0, 0, 0)

    def update_name(self, new_name):
        self.name = new_name[0].upper() + new_name[1:].lower()

    def open(self):
        self.is_open = True

    def close(self):
        self.update_main_window_rect()
        self.is_open = False
        self.is_minimized = False

    def minimize(self):
        self.update_main_window_rect()
        self.is_minimized = True

    def maximize(self):
        self.update_main_window_rect()
        self.is_minimized = False
