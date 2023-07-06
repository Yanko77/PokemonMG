import pygame
pygame.font.init()
import image


class IngameWindow:

    def __init__(self, name):
        self.is_open = False
        self.is_minimized = False

        self.window_pos_modif_mode = False

        self.name = name[0].upper() + name[1:].lower()
        self.icon = pygame.image.load('assets/game/ingame_windows/' + self.name + '/icon.png')

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

        self.min_window_hover = pygame.image.load('assets/game/ingame_windows/basic/min_main_hover.png')

        self.main_window_rect = self.basic_window.get_rect()
        self.main_window_rect.x = 20
        self.main_window_rect.w = 872
        self.main_window_rect.h = 528

        self.main_window_bar_rect = self.basic_window_bar_rect

        self.main_window_pos = [1, 1]

        self.buttons = image.IngameWindowButtons()

        self.title_font = pygame.font.Font('assets/fonts/Impact.ttf', 30)
        self.title = self.title_font.render(self.name, False, (0, 0, 0))
        self.title_marge = 75

    def update(self, surface, possouris):
        self.update_main_window_rect()

        if self.is_open:
            if self.is_minimized:
                surface.blit(self.min_window, self.main_window_pos)
                surface.blit(self.icon, (self.main_window_pos[0]-20, self.main_window_pos[1]+3))
                surface.blit(self.title, (self.main_window_pos[0] + self.title_marge-20, self.main_window_pos[1] + 0))

                if self.min_window_rect.collidepoint(possouris):
                    surface.blit(self.min_window_hover, self.main_window_pos)
            else:
                surface.blit(self.basic_window, self.main_window_pos)
                surface.blit(self.title, (self.main_window_pos[0] + self.title_marge, self.main_window_pos[1] + 0))
                surface.blit(self.icon, self.main_window_pos)
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
        self.title = self.title_font.render(self.name, False, (0, 0, 0))
        self.icon = pygame.image.load('assets/game/ingame_windows/' + self.name + '/icon.png')
        self.update_title_marge()

    def update_title_marge(self):
        if self.name == 'Spawn':
            self.title_marge = 75
        if self.name == 'Train':
            self.title_marge = 70
        if self.name == 'Grind':
            self.title_marge = 95
        if self.name == 'Items':
            self.title_marge = 70
        if self.name == 'Evolutions':
            self.title_marge = 75

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
