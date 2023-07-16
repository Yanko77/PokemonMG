import pygame


class SacIngamePanel:

    def __init__(self, game):
        self.game = game

        self.background1 = pygame.image.load("assets/game/ingame_windows/Sac d'objets/background1.png")
        self.background2 = pygame.image.load("assets/game/ingame_windows/Sac d'objets/background2.png")
        self.emp_hover = pygame.image.load("assets/game/ingame_windows/Sac d'objets/emp_hover.png")
        self.page1_hover = pygame.image.load("assets/game/ingame_windows/Sac d'objets/page1_hover.png")
        self.page2_hover = pygame.image.load("assets/game/ingame_windows/Sac d'objets/page2_hover.png")
        self.page1_rect = pygame.Rect(331, 40, 52, 52)
        self.page2_rect = pygame.Rect(387, 40, 52, 52)

        self.ALL_EMP_RECT = {
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

        self.emp_move_mode = False
        self.emp_moving = [False, False, False, False, False, False, False, False, False, False, False, False]
        self.rel_possouris = [0, 0]
        self.saved_posouris = [0, 0]

    def update(self, surface, possouris, window_pos):
        if self.page == 1:
            surface.blit(self.background1, window_pos)
        elif self.page == 2:
            surface.blit(self.background2, window_pos)

        if pygame.Rect(331+window_pos[0], 40+window_pos[1], 52, 52).collidepoint(possouris):
            surface.blit(self.page1_hover, window_pos)
        elif pygame.Rect(387+window_pos[0], 40+window_pos[1], 52, 52).collidepoint(possouris):
            surface.blit(self.page2_hover, window_pos)

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
        self.ALL_EMP_RECT = {
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
        self.page1_rect = pygame.Rect(331+window_pos[0], 40+window_pos[1], 52, 52)
        self.page2_rect = pygame.Rect(387+window_pos[0], 40+window_pos[1], 52, 52)

    def change_item_place(self, i1, i2):
        if not i1 == i2:
            if self.page == 1:
                self.game.player.sac_page1[i1-1], self.game.player.sac_page1[i2-1] = self.game.player.sac_page1[i2-1], self.game.player.sac_page1[i1-1]
            elif self.page == 2:
                self.game.player.sac_page2[i1-1], self.game.player.sac_page2[i2-1] = self.game.player.sac_page2[i2-1], self.game.player.sac_page2[i1-1]

    def update_emp(self, surface, possouris, window_pos, i):
        current_page = self.game.player.sac_page1
        if self.page == 1:
            current_page = self.game.player.sac_page1
        elif self.page == 2:
            current_page = self.game.player.sac_page2

        if current_page[i-1] is not None:
            if not self.emp_move_mode and not self.emp_moving[i-1]:
                if self.game.mouse_pressed[1] and self.all_emp_rect[i].collidepoint(possouris):
                    self.emp_move_mode = True
                    self.emp_moving[i-1] = True
                    self.rel_possouris = [0, 0]
                    self.saved_posouris = possouris

            if self.emp_move_mode and self.emp_moving[i-1]:
                if not self.game.mouse_pressed[1]:
                    if self.all_emp_rect[1].collidepoint(possouris):
                        self.change_item_place(i, 1)
                    elif self.all_emp_rect[2].collidepoint(possouris):
                        self.change_item_place(i, 2)
                    elif self.all_emp_rect[3].collidepoint(possouris):
                        self.change_item_place(i, 3)
                    elif self.all_emp_rect[4].collidepoint(possouris):
                        self.change_item_place(i, 4)
                    elif self.all_emp_rect[5].collidepoint(possouris):
                        self.change_item_place(i, 5)
                    elif self.all_emp_rect[6].collidepoint(possouris):
                        self.change_item_place(i, 6)
                    elif self.all_emp_rect[7].collidepoint(possouris):
                        self.change_item_place(i, 7)
                    elif self.all_emp_rect[8].collidepoint(possouris):
                        self.change_item_place(i, 8)
                    elif self.all_emp_rect[9].collidepoint(possouris):
                        self.change_item_place(i, 9)
                    elif self.all_emp_rect[10].collidepoint(possouris):
                        self.change_item_place(i, 10)
                    elif self.all_emp_rect[11].collidepoint(possouris):
                        self.change_item_place(i, 11)
                    elif self.all_emp_rect[12].collidepoint(possouris):
                        self.change_item_place(i, 12)

                    self.emp_move_mode = False
                    self.emp_moving[i-1] = False
                else:
                    self.rel_possouris = (possouris[0] - self.saved_posouris[0], possouris[1] - self.saved_posouris[1])
                    self.all_emp_rect[i].x = self.ALL_EMP_RECT[i].x + self.rel_possouris[0]
                    self.all_emp_rect[i].y = self.ALL_EMP_RECT[i].y + self.rel_possouris[1]

        if self.all_emp_rect[i].collidepoint(possouris):
            surface.blit(self.emp_hover, (self.all_emp_rect[i].x, self.all_emp_rect[i].y))

        if self.page == 1:
            if self.game.player.sac_page1[i-1] is not None:
                surface.blit(pygame.transform.scale(self.game.player.sac_page1[i-1].icon_image, (100, 100)), self.all_emp_rect[i])
        elif self.page == 2:
            if self.game.player.sac_page2[i-1] is not None:
                surface.blit(pygame.transform.scale(self.game.player.sac_page2[i - 1].icon_image, (100, 100)),
                             self.all_emp_rect[i])

    def is_hovering_buttons(self, possouris, window_pos):
        if self.all_emp_rect[1].collidepoint(possouris) or self.all_emp_rect[2].collidepoint(possouris) or \
                self.all_emp_rect[3].collidepoint(possouris) or self.all_emp_rect[4].collidepoint(possouris) or \
                self.all_emp_rect[5].collidepoint(possouris) or self.all_emp_rect[6].collidepoint(possouris) or \
                self.all_emp_rect[7].collidepoint(possouris) or self.all_emp_rect[8].collidepoint(possouris) or \
                self.all_emp_rect[9].collidepoint(possouris) or self.all_emp_rect[10].collidepoint(possouris) or \
                self.all_emp_rect[11].collidepoint(possouris) or self.all_emp_rect[12].collidepoint(possouris) or \
                pygame.Rect(331+window_pos[0], 40+window_pos[1], 52, 52).collidepoint(possouris) or \
                pygame.Rect(387+window_pos[0], 40+window_pos[1], 52, 52).collidepoint(possouris):
                    return True
        return False

    def change_page(self, num):
        self.page = num
