import pygame

import game_infos
import ingame_windows
import image
import player_name


class StartGamePanel:

    def __init__(self):
        self.panel = image.load_image('assets/accueil/panels/start_game/panel.png')

        self.new_game_button = image.load_image('assets/accueil/panels/start_game/new_game_button.png')
        self.new_game_button_rect = image.get_custom_rect(self.new_game_button, 791, 508)
        self.new_game_button_h = image.load_image('assets/accueil/panels/start_game/new_game_button_hover.png')

        self.load_game_button = image.load_image('assets/accueil/panels/start_game/load_game_button.png')
        self.load_game_button_rect = image.get_custom_rect(self.load_game_button, 130, 508)
        self.load_game_button_h = image.load_image('assets/accueil/panels/start_game/load_game_button_hover.png')

        self.x_button = image.load_image('assets/accueil/panels/start_game/x_button.png')
        self.x_button_rect = image.get_custom_rect(self.x_button, 1144, 68)
        self.x_button_h = image.load_image('assets/accueil/panels/start_game/x_button_hover.png')

    def update(self, surface, possouris, basic_accueil):
        surface.blit(self.panel, (0, 0))

        # Bouton NEW GAME
        self.update_button(self.new_game_button, self.new_game_button_rect, self.new_game_button_h, surface, possouris, basic_accueil)

        # Bouton LOAD GAME
        self.update_button(self.load_game_button, self.load_game_button_rect, self.load_game_button_h, surface, possouris, basic_accueil)

        # Bouton NEW GAME
        self.update_button(self.x_button, self.x_button_rect, self.x_button_h, surface, possouris, basic_accueil)

        if not (self.x_button_rect.collidepoint(possouris) or self.new_game_button_rect.collidepoint(possouris)
                or self.load_game_button_rect.collidepoint(possouris)):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def update_button(self, button, button_rect, button_hover, surface, possouris, basic_accueil):
        if button_rect.collidepoint(possouris) and not basic_accueil:
            surface.blit(button_hover, button_rect)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            surface.blit(button, button_rect)


class ClassicGamePanel:

    def __init__(self, game):
        self.game = game

        # LOADING FONTS --------------------------------------------
        #   # Basic fonts
        self.font = pygame.font.Font('assets/fonts/impact.ttf', 50)
        self.font_size2 = pygame.font.Font('assets/fonts/impact.ttf', 25)
        self.font_size3 = pygame.font.Font('assets/fonts/(Unranked) Bdeogale.ttf', 70)
        self.money_font = pygame.font.Font('assets/fonts/Impact.ttf', 45)
        self.actions_font = pygame.font.Font('assets/fonts/Impact.ttf', 90)
        #   # Pokemon fonts
        self.pokemon_name_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 25)
        self.pokemon_level_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 15)
        self.pokemon_hp_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 18)
        self.font_pokemon_info_values = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 19)
        self.font_pokemon_info_lv = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 42)
        self.font_pokemon_info_name = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 23)
        self.font_pokemon_type = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 15)
        

        # LOADING IMAGES --------------------------------------------

        # Elements permanents
        self.background = pygame.image.load('assets/game/panels/classic_panel/background.png')
        self.sac = image.load_image('assets/game/panels/classic_panel/sac.png', True, (200, 200))

        # Elements spontanés
        #    # Player infos
        self.mode_changement_pseudo_image = pygame.image.load('assets/game/panels/classic_panel/mode_changement_pseudo.png')
        self.player_name_hover = pygame.image.load("assets/game/panels/classic_panel/player_name_hover.png")
        self.curseur_changement_pseudo = image.CursorChangePseudoMode()
        self.player_name_image = self.font.render(self.game.player.name, False, (15, 0, 124))
        self.player_name_indication = self.font_size2.render("(cliquer pour modifier)", False, (15, 0, 124))
        self.player_lv_image = self.font_size3.render(str(self.game.player.level), False, (124, 124, 124))
        #   # Pokemon infos
        self.pokemon_info_popup = pygame.image.load('assets/game/panels/classic_panel/pokemon_infos.png')
        self.pokemon_info_popup_unknown = pygame.image.load('assets/game/panels/classic_panel/pokemon_info_unknown.png')
        self.pokemon_info_popup_x_button_hover = pygame.image.load('assets/game/panels/classic_panel/pokemon_infos_x_button_hover.png')
        #   # Pokemon team
        self.logo_pk_suppr = pygame.image.load('assets/game/panels/classic_panel/logo_suppr_pk.png')
        self.logo_pk_suppr_hover = pygame.image.load('assets/game/panels/classic_panel/logo_suppr_pk_hover.png')
        self.interface_sombre_team = pygame.image.load('assets/game/panels/classic_panel/item_to_pokemon.png')
        self.item_pk_hover_use = pygame.image.load('assets/game/panels/classic_panel/item_use_pk_hover.png')
        self.item_pk_hover_give = pygame.image.load('assets/game/panels/classic_panel/item_give_pk_hover.png')
        self.item_pk_hover_error = pygame.image.load('assets/game/panels/classic_panel/item_error_pk_hover.png')
        self.item_pk_hover_give_error = pygame.image.load('assets/game/panels/classic_panel/item_error_give_pk_hover.png')
        #   # Buttons
        self.sac_button_hover = self.create_rect_alpha((218, 215), (113, 64, 30))  # pygame.Rect(667, 465, 218, 215)

        # GENERATING RECTS --------------------------------------------

        #   # Player rects
        self.player_name_rect = pygame.Rect(656, 12, 399, 51)
        #   # Pokemon rects
        self.pokemon_info_popup_rect = pygame.Rect(898, 6, 374, 215)
        self.POKEMON_INFO_OBJ_RECT = pygame.Rect(1168, 143, 70, 70)
        self.pokemon_info_obj_rect = pygame.Rect(1168, 143, 70, 70)
        self.PK_RECTS = (pygame.Rect(900, 275, 369, 69), pygame.Rect(900, 348, 369, 69), pygame.Rect(900, 421, 369, 69),
                         pygame.Rect(900, 494, 369, 69), pygame.Rect(900, 567, 369, 69), pygame.Rect(900, 640, 369, 69))

        self.pk_rects = [pygame.Rect(900, 275, 369, 69), pygame.Rect(900, 348, 369, 69), pygame.Rect(900, 421, 369, 69),
                         pygame.Rect(900, 494, 369, 69), pygame.Rect(900, 567, 369, 69), pygame.Rect(900, 640, 369, 69)]
        #   # Button rects
        self.sac_button_rect = pygame.Rect(667, 465, 218, 215)
        self.logo_pk_suppr_rect = pygame.Rect(1085, 46, 150, 150)

        # SET VARIABLES --------------------------------------------
        #   # Pokemon infos
        self.pokemon_info_mode = False
        self.pokemon_info_i = 0
        self.pk_info_obj_move_mode = False
        #   # Pokemon move mode
        self.pk_move_mode = False
        self.moving_pk = [False, False, False, False, False, False]
        self.rel_possouris_pk_move_mode = [0, 0]
        self.saved_possouris = (0, 0)

        # IMPORT/INSTANCES --------------------------------------------
        self.alphabet_pixels = player_name.alphabet_pixels

        self.current_ig_window_name = 'Unknown'
        self.ingame_window = ingame_windows.IngameWindow(self.current_ig_window_name, self.game)

        self.buttons = image.ClassicGamePanelButtons()

    # UPDATES -----------------------------

    def update(self, surface, possouris):
        # BACKGROUND
        surface.blit(self.background, (0, 0))

        # PLAYER INFOS
        self.update_player_infos(surface, possouris)

        # PLAYER TEAM
        self.update_team_pokemons(surface, possouris)

        # PANEL BUTTONS
        self.buttons.update(surface, possouris, self.ingame_window)

        if self.sac_button_rect.collidepoint(possouris) and not self.ingame_window.main_window_rect.collidepoint(possouris):
            surface.blit(self.sac_button_hover, (667, 465))
        surface.blit(self.sac, (675, 475))

        # Interactions
        self.update_cursor(possouris)

        self.update_player_name_editing_mode(surface)

        # POKEMON INFO
        self.update_pokemon_info(surface, possouris)

        if self.ingame_window.sac_panel.emp_move_mode and not self.ingame_window.main_window_rect.collidepoint(
                possouris):
            surface.blit(self.interface_sombre_team, (0, 0))

        # INGAME WINDOW
        self.ingame_window.update(surface, possouris)

    def update_player_infos(self, surface, possouris):
        # PLAYER NAME
        self.update_player_name(surface, possouris)

        # PLAYER LEVEL
        self.update_player_lv(surface)

        # PLAYER MONEY
        surface.blit(self.money_font.render(str(self.game.player.money), False, (255, 255, 255)), (767, 71))

        # PLAYER ACTIONS_LEFT
        surface.blit(self.actions_font.render(str(self.game.player.actions), False, (0, 0, 0)), (385, 12))

    def update_player_lv(self, surface):
        self.player_lv_image = self.font_size3.render(str(self.game.player.level), False, (124, 124, 124))
        if self.game.player.level >= 10:
            surface.blit(self.player_lv_image, (955, 73))
        else:
            surface.blit(self.player_lv_image, (965, 73))

    def update_player_name(self, surface, possouris):
        surface.blit(self.font.render(self.game.player.name, False, (15, 0, 124)), (662, 10))
        if self.game.player.name_editing_mode:
            self.curseur_changement_pseudo.update(surface, player_name.get_pixels(self.game.player.name))
        if not self.game.player.name_edited:
            surface.blit(self.player_name_indication, (760, 30))

        if self.player_name_rect.collidepoint(possouris):
            if not self.ingame_window.main_window_rect.collidepoint(possouris):
                if self.pokemon_info_mode:
                    if not self.pokemon_info_popup_rect.collidepoint(possouris):
                        surface.blit(self.player_name_hover, (0, 0))
                else:
                    surface.blit(self.player_name_hover, (0, 0))

    def update_player_name_editing_mode(self, surface):
        if self.game.player.name_editing_mode:
            surface.blit(self.mode_changement_pseudo_image, (0, 0))

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

    def update_pokemon(self, surface, possouris, i):
        if self.game.player.team[i] is not None:
            if not self.ingame_window.starters_panel.pk_move_mode and not self.ingame_window.sac_panel.emp_move_mode and not self.ingame_window.spawn_panel.spawning_pk_move_mode:
                if not self.pk_move_mode and not self.ingame_window.main_window_rect.collidepoint(
                        possouris) and not self.ingame_window.window_pos_modif_mode:
                    if self.game.mouse_pressed[1] and self.pk_rects[i].collidepoint(possouris):
                        self.pk_move_mode = True
                        self.moving_pk[i] = True
                        self.rel_possouris_pk_move_mode = [0, 0]
                        self.saved_possouris = possouris

                if self.pk_move_mode and self.moving_pk[i]:
                    if not self.logo_pk_suppr_rect.collidepoint(possouris):
                        surface.blit(self.logo_pk_suppr, (0, 0))

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
                        elif self.logo_pk_suppr_rect.collidepoint(possouris):
                            if not self.game.player.get_nb_team_members() <= 1:
                                self.game.player.team[i] = None

                        self.pk_move_mode = False
                        self.moving_pk[i] = False
                        self.pk_rects = [pygame.Rect(900, 275, 369, 69), pygame.Rect(900, 348, 369, 69),
                                         pygame.Rect(900, 421, 369, 69), pygame.Rect(900, 494, 369, 69),
                                         pygame.Rect(900, 567, 369, 69), pygame.Rect(900, 640, 369, 69)]
                    else:
                        self.rel_possouris_pk_move_mode = (possouris[0] - self.saved_possouris[0],
                                                           possouris[1] - self.saved_possouris[1])
                        self.pk_rects[i].x = self.PK_RECTS[i].x + self.rel_possouris_pk_move_mode[0]
                        self.pk_rects[i].y = self.PK_RECTS[i].y + self.rel_possouris_pk_move_mode[1]

                        if self.logo_pk_suppr_rect.collidepoint(possouris):
                            surface.blit(self.logo_pk_suppr_hover, (0, 0))

            if self.game.player.team[i] is not None:
                surface.blit(self.game.player.team[i].icon_image, (self.pk_rects[i].x, self.pk_rects[i].y - 5),
                             (0, 0, 64, 64))
                surface.blit(self.pokemon_name_font.render(self.game.player.team[i].name, False, (0, 0, 0)),
                             (self.pk_rects[i].x + 70, self.pk_rects[i].y + 13))
                level = self.pokemon_level_font.render('Lv.' + str(self.game.player.team[i].level), False, (0, 0, 0))
                surface.blit(level, (self.pk_rects[i].x + 60, self.pk_rects[i].y + 42))

                type_color = game_infos.get_type_color(self.game.player.team[i].get_type())
                type_name_to_print = game_infos.get_type_name_to_print(self.game.player.team[i].get_type())
                type1_render = self.font_pokemon_type.render(type_name_to_print, False, type_color)
                surface.blit(type1_render, ((self.pk_rects[i].x + level.get_width() + 65, self.pk_rects[i].y + 42)))

                type2 = self.game.player.team[i].get_type2()
                if not type2 == 'NoType':
                    type2_color = game_infos.get_type_color(type2)
                    type2_name_to_print = game_infos.get_type_name_to_print(type2)
                    surface.blit(self.font_pokemon_type.render(type2_name_to_print, False, type2_color),
                                 ((self.pk_rects[i].x + level.get_width() + type1_render.get_width() + 68, self.pk_rects[i].y + 42)))


                pygame.draw.rect(surface, (35, 35, 35),
                                 pygame.Rect(self.pk_rects[i].x + 205, self.pk_rects[i].y + 26, 150, 17))
                pygame.draw.rect(surface, (42, 214, 0), pygame.Rect(self.pk_rects[i].x + 205,
                                                                    self.pk_rects[i].y + 26,
                                                                    self.game.player.team[i].health / self.game.player.team[
                                                                        i].pv * 150,
                                                                    17))
                surface.blit(
                    self.pokemon_hp_font.render(str(self.game.player.team[i].health) + "/" + str(self.game.player.team[i].pv),
                                                False, (0, 0, 0)), (self.pk_rects[i].x + 205, self.pk_rects[i].y + 40))

        if i in (0, 2, 4):
            color = (255, 255, 255)
        else:
            color = (163, 171, 255)

        if not self.ingame_window.main_window_rect.collidepoint(possouris):
            if self.pk_rects[i].collidepoint(possouris):
                surface.blit(self.create_rect_alpha((369, 69), color), (self.pk_rects[i].x, self.pk_rects[i].y))

                if self.ingame_window.sac_panel.emp_move_mode:
                    if self.game.player.team[i] is not None:
                        if self.ingame_window.sac_panel.selected_item.target_pokemon == 'All' or\
                                self.game.player.team[i].name == self.ingame_window.sac_panel.selected_item.target_pokemon:

                            if 'Use' in self.ingame_window.sac_panel.selected_item.fonctionnement:
                                surface.blit(self.item_pk_hover_use, (self.PK_RECTS[i].x - 3, self.PK_RECTS[i].y - 2))
                            elif 'Give' in self.ingame_window.sac_panel.selected_item.fonctionnement:
                                if self.game.player.team[i].objet_tenu is None:
                                    surface.blit(self.item_pk_hover_give, (self.PK_RECTS[i].x - 3, self.PK_RECTS[i].y - 2))
                                else:
                                    surface.blit(self.item_pk_hover_give_error,
                                                 (self.PK_RECTS[i].x - 3, self.PK_RECTS[i].y - 2))
                            else:
                                surface.blit(self.item_pk_hover_error, (self.PK_RECTS[i].x - 3, self.PK_RECTS[i].y - 2))
                        else:
                            surface.blit(self.item_pk_hover_error, (self.PK_RECTS[i].x - 3, self.PK_RECTS[i].y - 2))

    def update_pokemon_info(self, surface, possouris):
        if self.pokemon_info_mode:
            if pygame.Rect(1210, 9, 59, 59).collidepoint(possouris):
                surface.blit(self.pokemon_info_popup_x_button_hover, (0, 0))
            else:
                surface.blit(self.pokemon_info_popup, (0, 0))

            if self.game.player.team[self.pokemon_info_i] is not None:
                surface.blit(pygame.transform.scale(self.game.player.team[self.pokemon_info_i].icon_image, (280, 140)),
                             (900, 0), (0, 0, 140, 140))
                surface.blit(self.font_pokemon_info_name.render(self.game.player.team[self.pokemon_info_i].name, False,
                                                                (0, 0, 0)), (1038, 15))
                surface.blit(
                    self.font_pokemon_info_values.render(str(self.game.player.team[self.pokemon_info_i].pv), False,
                                                         (2, 137, 0)), (1070, 43))
                surface.blit(
                    self.font_pokemon_info_values.render(str(self.game.player.team[self.pokemon_info_i].attack), False,
                                                         (189, 0, 0)), (1070, 66))
                surface.blit(
                    self.font_pokemon_info_values.render(str(self.game.player.team[self.pokemon_info_i].defense), False,
                                                         (191, 200, 0)), (1070, 89))
                surface.blit(
                    self.font_pokemon_info_values.render(str(self.game.player.team[self.pokemon_info_i].speed), False,
                                                         (0, 139, 230)), (1070, 112))
                surface.blit(
                    self.font_pokemon_info_lv.render(str(self.game.player.team[self.pokemon_info_i].level), False,
                                                     (0, 0, 0)), (965, 139))

                if self.game.player.team[self.pokemon_info_i].objet_tenu is not None:

                    if self.pokemon_info_obj_rect.collidepoint(possouris):
                        surface.blit(self.create_rect_alpha((70, 70), (255, 255, 255)), self.pokemon_info_obj_rect)
                    surface.blit(
                        pygame.transform.scale(self.game.player.team[self.pokemon_info_i].objet_tenu.icon_image,
                                               (70, 70)),
                        (self.pokemon_info_obj_rect.x + 2, self.pokemon_info_obj_rect.y))
            else:
                surface.blit(self.pokemon_info_popup_unknown, (0, 0))

    def update_cursor(self, possouris):
        if self.get_interactions(possouris=possouris):
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    # INTERACTIONS -----------------------------

    def get_interactions(self, possouris):
        if not self.ingame_window.main_window_rect.collidepoint(possouris):

            if self.player_name_rect.collidepoint(possouris):
                if self.pokemon_info_mode:
                    if not self.pokemon_info_popup_rect.collidepoint(possouris):
                        return True
                    else:
                        return False
                else:
                    return True

            elif self.buttons.is_hovering_button(possouris):
                return True
            elif self.is_hovering_team_pokemon(possouris):
                return True
            elif self.sac_button_rect.collidepoint(possouris):
                return True
            elif self.is_hovering_pokemon_info_popup_buttons(possouris):
                return True
            else:
                return False

        else:
            if self.ingame_window.is_minimized:
                return False
            elif self.ingame_window.is_open:
                if self.ingame_window.is_hovering_buttons(possouris):
                    return True
                else:
                    return False

    def create_rect_alpha(self, dimensions, color):
        rect = pygame.Surface(dimensions)
        rect.set_alpha(90)
        rect.fill(color)
        return rect

    def change_pk_place(self, i1, i2):
        if not i1 == i2:
            self.game.player.team[i1], self.game.player.team[i2] = self.game.player.team[i2], self.game.player.team[i1]
            if self.pokemon_info_mode:
                if self.pokemon_info_i == i1:
                    self.pokemon_info_i = i2

    def is_hovering_team_pokemon(self, possouris):
        if not self.pk_rects[0].collidepoint(possouris) and not self.pk_rects[1].collidepoint(possouris):
            if not self.pk_rects[2].collidepoint(possouris) and not self.pk_rects[3].collidepoint(possouris):
                if not self.pk_rects[4].collidepoint(possouris) and not self.pk_rects[5].collidepoint(possouris):
                    return False
        return True

    def is_hovering_pokemon_info_popup_buttons(self, possouris):
        if pygame.Rect(1210, 9, 59, 59).collidepoint(possouris):
            return True
        elif pygame.Rect(1166, 141, 74, 74).collidepoint(possouris) and self.game.player.team[
            self.pokemon_info_i] is not None and self.game.player.team[self.pokemon_info_i].objet_tenu is not None:
            return True

        return False
