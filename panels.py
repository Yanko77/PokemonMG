import pygame
import ingame_windows
import image


class StartGamePanel:

    def __init__(self):
        self.panel = pygame.image.load('assets/accueil/panels/start_game/panel.png')

        self.new_game_button = pygame.image.load('assets/accueil/panels/start_game/new_game_button.png')
        self.new_game_button_rect = self.new_game_button.get_rect()
        self.new_game_button_rect.x = 791
        self.new_game_button_rect.y = 508
        self.new_game_button_h = pygame.image.load('assets/accueil/panels/start_game/new_game_button_hover.png')

        self.load_game_button = pygame.image.load('assets/accueil/panels/start_game/load_game_button.png')
        self.load_game_button_rect = self.load_game_button.get_rect()
        self.load_game_button_rect.x = 130
        self.load_game_button_rect.y = 508
        self.load_game_button_h = pygame.image.load('assets/accueil/panels/start_game/load_game_button_hover.png')

        self.x_button = pygame.image.load('assets/accueil/panels/start_game/x_button.png')
        self.x_button_rect = self.x_button.get_rect()
        self.x_button_rect.x = 1144
        self.x_button_rect.y = 68
        self.x_button_h = pygame.image.load('assets/accueil/panels/start_game/x_button_hover.png')

    def update(self, surface, possouris, basic_accueil):
        surface.blit(self.panel, (0, 0))

        if self.new_game_button_rect.collidepoint(possouris) and not basic_accueil:
            surface.blit(self.new_game_button_h, self.new_game_button_rect)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            surface.blit(self.new_game_button, self.new_game_button_rect)

        if self.load_game_button_rect.collidepoint(possouris) and not basic_accueil:
            surface.blit(self.load_game_button_h, self.load_game_button_rect)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            surface.blit(self.load_game_button, self.load_game_button_rect)

        if self.x_button_rect.collidepoint(possouris) and not basic_accueil:
            surface.blit(self.x_button_h, self.x_button_rect)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            surface.blit(self.x_button, self.x_button_rect)

        if not (self.x_button_rect.collidepoint(possouris) or self.new_game_button_rect.collidepoint(possouris)
                or self.load_game_button_rect.collidepoint(possouris)):

            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


class ClassicGamePanel:

    def __init__(self, player, game):
        self.is_pname_modif = False
        self.change_player_name_mode = False

        self.game = game

        self.background = pygame.image.load('assets/game/panels/classic_panel/background.png')
        self.mode_changement_pseudo_image = pygame.image.load('assets/game/panels/classic_panel/'
                                                              'mode_changement_pseudo.png')
        self.sac = pygame.image.load('assets/game/panels/classic_panel/sac.png')
        self.sac = pygame.transform.scale(self.sac, (200, 200))
        self.curseur_changement_pseudo = image.CursorChangePseudoMode()

        self.font = pygame.font.Font('assets/fonts/impact.ttf', 50)
        self.font_size2 = pygame.font.Font('assets/fonts/impact.ttf', 25)
        self.font_size3 = pygame.font.Font('assets/fonts/(Unranked) Bdeogale.ttf', 70)

        self.pokemon_name_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 25)
        self.pokemon_level_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 15)
        self.pokemon_hp_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 18)

        self.player = player
        self.player_name = self.player.name

        self.player_name_image = self.font.render(self.player_name, False, (15, 0, 124))
        self.player_name_indication = self.font_size2.render("(cliquer pour modifier)", False, (15, 0, 124))
        self.player_lv_image = self.font_size3.render(str(self.player.level), False, (124, 124, 124))

        self.player_name_rect = pygame.Rect(656, 12, 399, 51)
        self.player_name_hover = pygame.image.load("assets/game/panels/classic_panel/player_name_hover.png")

        self.alphabet_pixels = {}

        self.current_ig_window_name = 'Unknown'
        self.ingame_window = ingame_windows.IngameWindow(self.current_ig_window_name, self.game)

        self.buttons = image.ClassicGamePanelButtons()
        self.sac_button_hover = self.create_rect_alpha((218, 215), (113, 64, 30))  # pygame.Rect(667, 465, 218, 215)
        self.sac_button_rect = pygame.Rect(667, 465, 218, 215)

        self.PK_RECTS = [pygame.Rect(900, 275, 369, 69), pygame.Rect(900, 348, 369, 69), pygame.Rect(900, 421, 369, 69),
                         pygame.Rect(900, 494, 369, 69), pygame.Rect(900, 567, 369, 69), pygame.Rect(900, 640, 369, 69)]

        self.pk_rects = [pygame.Rect(900, 275, 369, 69), pygame.Rect(900, 348, 369, 69), pygame.Rect(900, 421, 369, 69),
                         pygame.Rect(900, 494, 369, 69), pygame.Rect(900, 567, 369, 69), pygame.Rect(900, 640, 369, 69)]
        self.pk_move_mode = False
        self.moving_pk = [False, False, False, False, False, False]
        self.rel_possouris_pk_move_mode = [0, 0]
        self.saved_possouris = (0, 0)

    def update(self, surface, possouris):

        surface.blit(self.background, (0, 0))
        surface.blit(self.font.render(self.player.name, False, (15, 0, 124)), (662, 10))
        if self.change_player_name_mode:
            self.curseur_changement_pseudo.update(surface, self.calcul_player_name_pixels())
        if not self.is_pname_modif:
            surface.blit(self.player_name_indication, (760, 30))

        if self.player.level >= 10:
            surface.blit(self.player_lv_image, (955, 73))
        else:
            surface.blit(self.player_lv_image, (965, 73))

        self.update_team_pokemons(surface, possouris)
        self.buttons.update(surface, possouris, self.ingame_window)
        if self.sac_button_rect.collidepoint(possouris) and not self.ingame_window.main_window_rect.collidepoint(possouris):
            surface.blit(self.sac_button_hover, (667, 465))
        surface.blit(self.sac, (675, 475))


        # Interactions
        if not self.ingame_window.main_window_rect.collidepoint(possouris):

            if self.player_name_rect.collidepoint(possouris):
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                surface.blit(self.player_name_hover, (0, 0))
            elif self.buttons.is_hovering_button(possouris):
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif self.is_hovering_team_pokemon(possouris):
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif self.sac_button_rect.collidepoint(possouris):
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        else:
            if self.ingame_window.is_minimized:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif self.ingame_window.is_open:
                if self.ingame_window.is_hovering_buttons(possouris):
                    if not pygame.mouse.get_cursor() == pygame.SYSTEM_CURSOR_HAND:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    if not pygame.mouse.get_cursor() == pygame.SYSTEM_CURSOR_ARROW:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if self.change_player_name_mode:
            surface.blit(self.mode_changement_pseudo_image, (0, 0))

        self.ingame_window.update(surface, possouris)

    def update_player_name(self, current_player_name):
        if not self.player_name == current_player_name:
            self.player_name = current_player_name

    def update_player_lv(self):
        self.player_lv_image = self.font_size3.render(str(self.player.level), False, (124, 124, 124))

    def create_rect_alpha(self, dimensions, color):
        rect = pygame.Surface(dimensions)
        rect.set_alpha(90)
        rect.fill(color)
        return rect

    def change_pk_place(self, i1, i2):
        if not i1 == i2:
            self.player.team[i1], self.player.team[i2] = self.player.team[i2], self.player.team[i1]

    def update_pokemon(self, surface, possouris, i):
        if self.player.team[i] is not None:
            if not self.pk_move_mode and not self.ingame_window.main_window_rect.collidepoint(possouris) and not self.ingame_window.window_pos_modif_mode:
                if self.game.mouse_pressed[1] and self.pk_rects[i].collidepoint(possouris):
                    self.pk_move_mode = True
                    self.moving_pk[i] = True
                    self.rel_possouris_pk_move_mode = [0, 0]
                    self.saved_possouris = possouris

            if self.pk_move_mode and self.moving_pk[i]:
                if not self.game.mouse_pressed[1]:
                    if self.PK_RECTS[0].collidepoint(possouris):
                        self.change_pk_place(i, 0)
                    elif self.PK_RECTS[1].collidepoint(possouris):
                        self.change_pk_place(i, 1)
                    elif self.PK_RECTS[2].collidepoint(possouris):
                        self.change_pk_place(i, 2)
                    elif self.PK_RECTS[3].collidepoint(possouris):
                        self.change_pk_place(i, 3)
                    elif self.PK_RECTS[4].collidepoint(possouris):
                        self.change_pk_place(i, 4)
                    elif self.PK_RECTS[5].collidepoint(possouris):
                        self.change_pk_place(i, 5)

                    self.pk_move_mode = False
                    self.moving_pk[i] = False
                    self.pk_rects = [pygame.Rect(900, 275, 369, 69), pygame.Rect(900, 348, 369, 69),
                                     pygame.Rect(900, 421, 369, 69), pygame.Rect(900, 494, 369, 69),
                                     pygame.Rect(900, 567, 369, 69), pygame.Rect(900, 640, 369, 69)]
                else:
                    self.rel_possouris_pk_move_mode = (possouris[0] - self.saved_possouris[0], possouris[1] - self.saved_possouris[1])
                    self.pk_rects[i].x = self.PK_RECTS[i].x + self.rel_possouris_pk_move_mode[0]
                    self.pk_rects[i].y = self.PK_RECTS[i].y + self.rel_possouris_pk_move_mode[1]

            surface.blit(self.player.team[i].icon_image, (self.pk_rects[i].x, self.pk_rects[i].y-5), (0, 0, 64, 64))
            surface.blit(self.pokemon_name_font.render(self.player.team[i].name, False, (0, 0, 0)), (self.pk_rects[i].x+70, self.pk_rects[i].y + 13))
            surface.blit(self.pokemon_level_font.render('Lv.' + str(self.player.team[i].level), False, (0, 0, 0)), (self.pk_rects[i].x+60, self.pk_rects[i].y + 42))

            pygame.draw.rect(surface, (35, 35, 35),
                             pygame.Rect(self.pk_rects[i].x + 200, self.pk_rects[i].y + 26, 150, 17))
            pygame.draw.rect(surface, (42, 214, 0), pygame.Rect(self.pk_rects[i].x + 200,
                                                                self.pk_rects[i].y + 26,
                                                                self.player.team[i].health / self.player.team[i].pv * 150,
                                                                17))
            surface.blit(self.pokemon_hp_font.render(str(self.player.team[i].health) + "/" + str(self.player.team[i].pv),
                                                     False, (0, 0, 0)), (self.pk_rects[i].x + 200, self.pk_rects[i].y + 40))

            if i in [0, 2, 4]:
                color = (255, 255, 255)
            else:
                color = (163, 171, 255)

            if not self.ingame_window.main_window_rect.collidepoint(possouris):
                if self.pk_rects[i].collidepoint(possouris):
                    surface.blit(self.create_rect_alpha((369, 69), color), (self.pk_rects[i].x, self.pk_rects[i].y))

    def is_hovering_team_pokemon(self, possouris):
        if not self.pk_rects[0].collidepoint(possouris) and not self.pk_rects[1].collidepoint(possouris):
            if not self.pk_rects[2].collidepoint(possouris) and not self.pk_rects[3].collidepoint(possouris):
                if not self.pk_rects[4].collidepoint(possouris) and not self.pk_rects[5].collidepoint(possouris):
                    return False
        return True

    def update_team_pokemons(self, surface, possouris):
        # Pokemon 1
        self.update_pokemon(surface, possouris, 0)
        # Pokemon 2
        self.update_pokemon(surface, possouris, 1)
        # Pokemon 3
        self.update_pokemon(surface, possouris, 2)
        # Pokemon 4
        self.update_pokemon(surface, possouris, 3)
        # Pokemon 5
        self.update_pokemon(surface, possouris, 4)
        # Pokemon 6
        self.update_pokemon(surface, possouris, 5)

    def calcul_player_name_pixels(self):
        pixels = 0
        for c in self.player_name:
            pixels += self.alphabet_pixels[c]
            pixels += 5

        return pixels

    def def_alphabet_pixels(self, alphabet_pixels):
        self.alphabet_pixels = alphabet_pixels
