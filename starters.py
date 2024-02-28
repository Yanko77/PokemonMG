import pygame
import pokemon
pygame.font.init()


class StartersPanel:

    def __init__(self, game):
        self.game = game

        self.background = pygame.image.load('assets/game/ingame_windows/Starters/background.png')
        self.button_aide = pygame.image.load('assets/game/ingame_windows/Starters/button_aide.png')
        self.button_aide_rect = pygame.Rect(800, 444, 42, 42)
        self.button_aide_hover = pygame.image.load('assets/game/ingame_windows/Starters/button_aide_hover.png')

        self.pokeballs = [pygame.image.load('assets/game/ingame_windows/Starters/pokeball1.png'),
                          pygame.image.load('assets/game/ingame_windows/Starters/pokeball2.png'),
                          pygame.image.load('assets/game/ingame_windows/Starters/pokeball3.png')]

        self.PK_RECTS = [pygame.Rect(80, 84, 190, 190), pygame.Rect(362, 84, 190, 190), pygame.Rect(642, 84, 190, 190)]
        self.pk_rects = [pygame.Rect(80, 84, 190, 190), pygame.Rect(362, 84, 190, 190), pygame.Rect(642, 84, 190, 190)]

        self.pk_hover = pygame.image.load('assets/game/ingame_windows/Starters/pokeball_hover.png')
        self.pk_hover = pygame.transform.scale(self.pk_hover, (190, 190))

        self.starters = [pokemon.Pokemon(self.game.starters[0], 5, self.game),
                         pokemon.Pokemon(self.game.starters[1], 5, self.game),
                         pokemon.Pokemon(self.game.starters[2], 5, self.game)]
        self.pk_decouverts = [False, False, False]

        self.pk_name_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 30)
        self.pk_move_mode = False
        self.pk_moving = [False, False, False]
        self.rel_possouris_pk_move_mode = [0, 0]
        self.saved_possouris = [0, 0]

    def update(self, surface, possouris, window_pos):
        self.update_rect_pos(window_pos)

        surface.blit(self.background, window_pos)

        if self.button_aide_rect.collidepoint(possouris):
            surface.blit(self.button_aide_hover, window_pos)
        else:
            surface.blit(self.button_aide, window_pos)

        self.update_pokemon(surface, possouris, window_pos, 0)
        self.update_pokemon(surface, possouris, window_pos, 1)
        self.update_pokemon(surface, possouris, window_pos, 2)


    def create_rect_alpha(self, dimensions, color):
        rect = pygame.Surface(dimensions)
        rect.set_alpha(90)
        rect.fill(color)
        return rect

    def update_rect_pos(self, window_pos):
        self.button_aide_rect = pygame.Rect(800 + window_pos[0], 444 + window_pos[1], 42, 42)
        self.PK_RECTS = [pygame.Rect(80 + window_pos[0], 84 + window_pos[1], 190, 190),
                         pygame.Rect(362 + window_pos[0], 84 + window_pos[1], 190, 190),
                         pygame.Rect(642 + window_pos[0], 84 + window_pos[1], 190, 190)]
        self.pk_rects = [pygame.Rect(80 + window_pos[0], 84 + window_pos[1], 190, 190),
                         pygame.Rect(362 + window_pos[0], 84 + window_pos[1], 190, 190),
                         pygame.Rect(642 + window_pos[0], 84 + window_pos[1], 190, 190)]

    def reset_player_team(self, i):
        if not 0 == i:
            self.game.player.team[0] = None
        if not 1 == i:
            self.game.player.team[1] = None
        if not 2 == i:
            self.game.player.team[2] = None
        if not 3 == i:
            self.game.player.team[3] = None
        if not 4 == i:
            self.game.player.team[4] = None
        if not 5 == i:
            self.game.player.team[5] = None

    def update_pokemon(self, surface, possouris, window_pos, i):
        if not self.pk_move_mode and not self.pk_moving[i]:
            if self.game.mouse_pressed[1] and self.pk_rects[i].collidepoint(possouris):
                if self.pk_decouverts[i]:
                    self.pk_move_mode = True
                    self.pk_moving[i] = True
                    self.rel_possouris_pk_move_mode = [0, 0]
                    self.saved_possouris = possouris

        if self.pk_move_mode and self.pk_moving[i]:
            if not self.game.mouse_pressed[1]:

                if self.game.classic_panel.PK_RECTS[0].collidepoint(possouris):
                    self.select_starter(i, 0)
                elif self.game.classic_panel.PK_RECTS[1].collidepoint(possouris):
                    self.select_starter(i, 1)
                elif self.game.classic_panel.PK_RECTS[2].collidepoint(possouris):
                    self.select_starter(i, 2)
                elif self.game.classic_panel.PK_RECTS[3].collidepoint(possouris):
                    self.select_starter(i, 3)
                elif self.game.classic_panel.PK_RECTS[4].collidepoint(possouris):
                    self.select_starter(i, 4)
                elif self.game.classic_panel.PK_RECTS[5].collidepoint(possouris):
                    self.select_starter(i, 5)
                else:
                    self.pk_rects = [pygame.Rect(80 + window_pos[0], 84 + window_pos[1], 190, 190),
                                     pygame.Rect(362 + window_pos[0], 84 + window_pos[1], 190, 190),
                                     pygame.Rect(642 + window_pos[0], 84 + window_pos[1], 190, 190)]

                self.pk_moving[i] = False
                self.pk_move_mode = False
            else:
                self.rel_possouris_pk_move_mode = (possouris[0] - self.saved_possouris[0], possouris[1]- self.saved_possouris[1])
                self.pk_rects[i].x = self.PK_RECTS[i].x + self.rel_possouris_pk_move_mode[0]
                self.pk_rects[i].y = self.PK_RECTS[i].y + self.rel_possouris_pk_move_mode[1]

        if self.pk_rects[i].collidepoint(possouris):
            surface.blit(self.create_rect_alpha((210, 210), (255, 255, 255)), (self.pk_rects[i].x - 10, self.pk_rects[i].y - 5))

        if self.pk_decouverts[i]:
            if self.starters[i].name == 'Bulbizarre':
                surface.blit(pygame.transform.scale(self.starters[i].icon_image, (500, 250)),
                             (self.pk_rects[i].x - 40, self.pk_rects[i].y - 50), (0, 0, 250, 250))
            else:
                surface.blit(pygame.transform.scale(self.starters[i].icon_image, (500, 250)), (self.pk_rects[i].x - 30, self.pk_rects[i].y - 50), (0, 0, 250, 250))
            surface.blit(self.pk_name_font.render(self.starters[i].name, False, (255, 255, 255)), ((250-self.pk_name_font.render(self.starters[i].name, False, (255, 255, 255)).get_rect().w)/2 + window_pos[0]+50+(282*i), 318+window_pos[1]))

        else:
            surface.blit(self.pokeballs[i], (0+window_pos[0], 0+window_pos[1]))

    def select_starter(self, i_starter, i_team=0):
        self.game.player.team[i_team] = self.starters[i_starter]
        self.game.is_starter_selected = True
        self.reset_player_team(i_team)

        # self.game.classic_panel.ingame_window.init_train_panel()

    def decouvrir_pk(self, i):
        self.pk_decouverts[i] = True

    def left_clic_interactions(self, possouris):
        if self.pk_rects[0].collidepoint(possouris):
            self.decouvrir_pk(0)
        elif self.pk_rects[1].collidepoint(possouris):
            self.decouvrir_pk(1)
        elif self.pk_rects[2].collidepoint(possouris):
            self.decouvrir_pk(2)

    def is_hovering_buttons(self, possouris):
        if self.pk_rects[0].collidepoint(possouris) or self.pk_rects[1].collidepoint(possouris) \
                or self.pk_rects[2].collidepoint(possouris) or self.button_aide_rect.collidepoint(possouris):
            return True
