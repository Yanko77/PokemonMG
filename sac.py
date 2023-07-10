import pygame


class SacIngamePanel:

    def __init__(self):
        self.background1 = pygame.image.load("assets/game/ingame_windows/Sac d'objets/background1.png")
        self.background2 = pygame.image.load("assets/game/ingame_windows/Sac d'objets/background2.png")
        self.emp_hover = pygame.image.load("assets/game/ingame_windows/Sac d'objets/emp_hover.png")
        self.all_emp_rect = {
            1: pygame.Rect(463, 46, 100, 100),
            2: pygame.Rect(570, 46, 100, 100),
            3: pygame.Rect(677, 46, 100, 100),
            4: pygame.Rect(784, 46, 100, 100),
            5: pygame.Rect(463, 153, 100, 100),
            6: pygame.Rect(570, 153, 100, 100),
            7: pygame.Rect(677, 153, 100, 100),
            8: pygame.Rect(784, 153, 100, 100),
            9: pygame.Rect(463, 260, 100, 100),
            10: pygame.Rect(570, 260, 100, 100),
            11: pygame.Rect(677, 260, 100, 100),
            12: pygame.Rect(784, 260, 100, 100)
        }
        self.page = 1

    def update(self, surface, possouris, window_pos):
        if self.page == 1:
            surface.blit(self.background1, window_pos)
        elif self.page == 2:
            surface.blit(self.background2, window_pos)

        self.update_rect_pos(window_pos)
        self.update_emp(surface, possouris, window_pos, 1)
        self.update_emp(surface, possouris, window_pos, 2)
        self.update_emp(surface, possouris, window_pos, 3)
        self.update_emp(surface, possouris, window_pos, 4)
        self.update_emp(surface, possouris, window_pos, 5)
        self.update_emp(surface, possouris, window_pos, 6)
        self.update_emp(surface, possouris, window_pos, 7)
        self.update_emp(surface, possouris, window_pos, 8)
        self.update_emp(surface, possouris, window_pos, 9)
        self.update_emp(surface, possouris, window_pos, 10)
        self.update_emp(surface, possouris, window_pos, 11)
        self.update_emp(surface, possouris, window_pos, 12)
        self.update_rect_pos(window_pos)

    def update_rect_pos(self, window_pos):
        self.all_emp_rect = {
            1: pygame.Rect(463 + window_pos[0], 46 + window_pos[1], 100, 100),
            2: pygame.Rect(570 + window_pos[0], 46 + window_pos[1], 100, 100),
            3: pygame.Rect(677 + window_pos[0], 46 + window_pos[1], 100, 100),
            4: pygame.Rect(784 + window_pos[0], 46 + window_pos[1], 100, 100),
            5: pygame.Rect(463 + window_pos[0], 153 + window_pos[1], 100, 100),
            6: pygame.Rect(570 + window_pos[0], 153 + window_pos[1], 100, 100),
            7: pygame.Rect(677 + window_pos[0], 153 + window_pos[1], 100, 100),
            8: pygame.Rect(784 + window_pos[0], 153 + window_pos[1], 100, 100),
            9: pygame.Rect(463 + window_pos[0], 260 + window_pos[1], 100, 100),
            10: pygame.Rect(570 + window_pos[0], 260 + window_pos[1], 100, 100),
            11: pygame.Rect(677 + window_pos[0], 260 + window_pos[1], 100, 100),
            12: pygame.Rect(784 + window_pos[0], 260 + window_pos[1], 100, 100)
        }

    def update_emp(self, surface, possouris, window_pos, i):
        if i in [1, 5, 9]:
            x = 0
        elif i in [2, 6, 10]:
            x = 107
        elif i in [3, 7, 11]:
            x = 214
        else:
            x = 321

        if i in [1, 2, 3, 4]:
            y = 0
        elif i in [5, 6, 7, 8]:
            y = 107
        else:
            y = 214

        if self.all_emp_rect[i].collidepoint(possouris):
            surface.blit(self.emp_hover, (window_pos[0] + x, window_pos[1] + y))

    def is_hovering_buttons(self, possouris):
        if self.all_emp_rect[1].collidepoint(possouris) or self.all_emp_rect[2].collidepoint(possouris) or \
                self.all_emp_rect[3].collidepoint(possouris) or self.all_emp_rect[4].collidepoint(possouris) or \
                self.all_emp_rect[5].collidepoint(possouris) or self.all_emp_rect[6].collidepoint(possouris) or \
                self.all_emp_rect[7].collidepoint(possouris) or self.all_emp_rect[8].collidepoint(possouris) or \
                self.all_emp_rect[9].collidepoint(possouris) or self.all_emp_rect[10].collidepoint(possouris) or \
                self.all_emp_rect[11].collidepoint(possouris) or self.all_emp_rect[12].collidepoint(possouris):
            return True
        return False

    def change_page(self, num):
        self.page = num
