"""
Fichier gérant le panel principal du jeu.
"""

# Importation des modules

import random

import pygame

import fight
import game_infos

import ingame_windows
from notif import Notif

# Définition des classes


class GamePanel:
    """
    Classe qui représente le panel principal du jeu
    """

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
        #   # Pre-loading
        self.player_name_text = self.font.render(self.game.player.name, False, (15, 0, 124))
        #   # Dresseur fonts
        self.dresseur_name_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 30)
        self.dresseur_info_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 21)
        # LOADING IMAGES --------------------------------------------

        # Elements permanents
        self.background = pygame.image.load('assets/game/panels/classic_panel/background.png')
        self.no_action_background = pygame.image.load('assets/game/panels/classic_panel/no_action_background.png')
        self.sac = pygame.image.load('assets/game/panels/classic_panel/sac.png')
        self.sac = pygame.transform.scale(self.sac, (200, 200))

        # Elements spontanés
        #    # Player infos
        self.mode_changement_pseudo_image = pygame.image.load('assets/game/panels/classic_panel/mode_changement_pseudo.png')
        self.player_name_hover = pygame.image.load("assets/game/panels/classic_panel/player_name_hover.png")
        self.player_name_image = self.font.render(self.game.player.name, False, (15, 0, 124))
        self.player_name_indication = self.font_size2.render("(cliquer pour modifier)", False, (15, 0, 124))
        self.player_lv_image = self.font_size3.render(str(self.game.player.level), False, (124, 124, 124))
        #   # Pokemon infos
        self.pokemon_info_popup = pygame.image.load('assets/game/panels/classic_panel/pokemon_infos.png')
        self.pokemon_info_popup_unknown = pygame.image.load('assets/game/panels/classic_panel/pokemon_info_unknown.png')
        self.pokemon_info_popup_x_button_hover = pygame.image.load('assets/game/panels/classic_panel/pokemon_infos_x_button_hover.png')
        #   # Pokemon team
        self.delete_pk_button = pygame.image.load('assets/game/panels/classic_panel/delete_pk_button.png')
        self.delete_pk_button_rect = pygame.Rect(1065, 23, 194, 194)
        self.interface_sombre_team = pygame.image.load('assets/game/panels/classic_panel/item_to_pokemon.png')
        self.item_pk_hover_use = pygame.image.load('assets/game/panels/classic_panel/item_use_pk_hover.png')
        self.item_pk_hover_give = pygame.image.load('assets/game/panels/classic_panel/item_give_pk_hover.png')
        self.item_pk_hover_error = pygame.image.load('assets/game/panels/classic_panel/item_error_pk_hover.png')
        self.item_pk_hover_give_error = pygame.image.load('assets/game/panels/classic_panel/item_error_give_pk_hover.png')
        #   # Buttons
        self.sac_button_hover = self.create_rect_alpha((218, 215), (113, 64, 30))  # pygame.Rect(667, 465, 218, 215)
        self.go_fight_button = pygame.image.load('assets/game/panels/classic_panel/go_fight_button.png')
        self.go_fight_button_v2 = pygame.image.load('assets/game/panels/classic_panel/go_fight_button_v2.png')
        self.go_fight_button_hover = pygame.image.load('assets/game/panels/classic_panel/go_fight_button_hover.png')
        self.go_fight_button_rect = pygame.Rect(-5, -46, 520, 180)
        self.go_fight_button_compteur = 0
        #   # Fight popup
        self.fight_popup = pygame.image.load('assets/game/panels/classic_panel/fight_popup.png')
        self.fight_sac_button = pygame.image.load('assets/game/panels/classic_panel/dresseur_sac_button.png')
        self.fight_sac_button_rect = pygame.Rect(184, 211, 75, 92)
        self.fight_equipe_button = pygame.image.load('assets/game/panels/classic_panel/dresseur_equipe_button.png')
        self.fight_equipe_button_rect = pygame.Rect(265, 211, 75, 92)

        self.fight_popup_x_button = pygame.image.load('assets/game/panels/classic_panel/x_fight_popup_button.png')
        self.fight_popup_x_button_rect = pygame.Rect(557, 82, 70, 70)
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
        self.logo_enable_item_rect = pygame.Rect(1085, 46, 150, 150)

        # SET VARIABLES --------------------------------------------
        #   # Player name
        self.player_name_editing_mode = False
        self.player_name_cursor_compteur = 0
        #   # Pokemon infos
        self.pokemon_info_mode = False
        self.pokemon_info = None
        self.pk_info_obj_move_mode = False
        #   # Pokemon move mode
        self.pk_move_mode = False
        self.moving_pk = [False, False, False, False, False, False]
        self.moving_pk_rel_possouris = [0, 0]
        self.saved_possouris = (0, 0)
        #   # Pokemon hover
        self.current_hover_pokemon_register = {0: False,
                                               1: False,
                                               2: False,
                                               3: False,
                                               4: False,
                                               5: False,
                                               }
        self.current_hover_pokemon = None
        #   # End turn fight
        self.boolFight_popup = None
        self.fight_popup_drop_pk_rect = pygame.Rect(16, 405, 696, 252)
        self.fighting_pk = None

        # IMPORT/INSTANCES --------------------------------------------

        self.ingame_window = ingame_windows.IngameWindow(self.game)

        self.buttons = GamePanelButtons()

    # UPDATES -----------------------------

    def update(self, surface, possouris):
        """
        Methode d'actualisation de l'affichage de l'ecran principal du jeu.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """
        # BACKGROUND
        if self.game.player.actions > 0:
            surface.blit(self.background, (0, 0))
            self.update_player_infos(surface, possouris)  # PLAYER INFOS
        else:
            surface.blit(self.no_action_background, (0, 0))
            self.update_player_infos(surface, possouris)  # PLAYER INFOS
            self.update_go_fight_button(surface, possouris)

        # PLAYER TEAM
        self.update_hover_pokemon()
        if not self.pk_move_mode:
            self.update_team_pokemons(surface, possouris)

        # PANEL BUTTONS
        self.buttons.update(surface, possouris, self.ingame_window)

        if self.sac_button_rect.collidepoint(possouris) and not self.ingame_window.is_hovering(possouris):
            surface.blit(self.sac_button_hover, (667, 465))
        surface.blit(self.sac, (675, 475))

        # Interactions
        self.update_cursor(possouris)

        # POKEMON INFO
        self.update_pokemon_info(surface, possouris)

        if self.ingame_window.sac_panel.emp_move_mode and not self.ingame_window.is_hovering(possouris):
            surface.blit(self.interface_sombre_team, (0, 0))

        # FIGHT POPUP
        if self.boolFight_popup:
            self.update_fight_popup(surface, possouris)

        # INGAME WINDOW
        self.ingame_window.update(surface, possouris)

        if self.pk_move_mode:
            self.update_team_pokemons(surface, possouris)

        self.update_player_name_editing_mode(surface)

    def update_fight_popup(self, surface, possouris):
        """
        Methode d'actualisation de l'affichage du popup FIGHT.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """
        surface.blit(self.fight_popup, (0, 0))

        # BUTTONS
        if self.fight_popup_x_button_rect.collidepoint(possouris):
            surface.blit(self.fight_popup_x_button, self.fight_popup_x_button_rect, (70, 0, 70, 70))
        else:
            surface.blit(self.fight_popup_x_button, self.fight_popup_x_button_rect, (0, 0, 70, 70))

        if self.fight_sac_button_rect.collidepoint(possouris):
            surface.blit(self.fight_sac_button, self.fight_sac_button_rect, (75, 0, 75, 92))
        else:
            surface.blit(self.fight_sac_button, self.fight_sac_button_rect, (0, 0, 75, 92))

        if self.fight_equipe_button_rect.collidepoint(possouris):
            surface.blit(self.fight_equipe_button, self.fight_equipe_button_rect, (75, 0, 75, 92))
        else:
            surface.blit(self.fight_equipe_button, self.fight_equipe_button_rect, (0, 0, 75, 92))

        # Affichage de l'icone du dresseur
        surface.blit(self.game.next_fighting_dresseur.icon, (18, 148))
        # Affichage du nom du dresseur
        surface.blit(self.dresseur_name_font.render(self.game.next_fighting_dresseur.name, False, (40, 40, 40)),
                     (187, 138))
        # Affichage du nombre de round
        surface.blit(self.dresseur_name_font.render(str(self.game.round.num), False, (80, 80, 80)), (138, 315))
        # Affichage du niveau du joueur
        surface.blit(self.dresseur_name_font.render(str(self.game.player.get_level()), False, (80, 80, 80)), (196, 348))

        # Affichage de la puissance du dresseur (power)
        surface.blit(self.dresseur_info_font.render(str(self.game.next_fighting_dresseur.power), False, (180, 0, 0)), (447, 200))
        # Affichage du niveau du dresseur (niveau du pokemon)
        surface.blit(self.dresseur_info_font.render(str(self.game.next_fighting_dresseur.pk.get_level()), False, (255, 255, 0)), (424, 226))

    def update_player_infos(self, surface, possouris):
        """
        Methode d'actualisation de l'affichage des infos du joueur.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """
        # PLAYER NAME
        self.display_player_name(surface, possouris)

        # PLAYER LEVEL
        self.update_player_lv(surface)

        # PLAYER MONEY
        surface.blit(self.money_font.render(str(self.game.player.money), False, (255, 255, 255)), (767, 71))

        # PLAYER ACTIONS_LEFT
        surface.blit(self.actions_font.render(str(self.game.player.actions), False, (0, 0, 0)), (385, 12))

    def update_player_name(self):
        """
        Methode d'actualisation de l'image du nom du joueur
        """
        self.player_name_text = self.font.render(self.game.player.name, False, (15, 0, 124))

    def display_player_name(self, surface, possouris):
        """
        Methode d'actualisation de l'affichage du nom du joueur.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """
        surface.blit(self.player_name_text, (662, 10))

        if self.game.player.name == "Nom":
            surface.blit(self.player_name_indication, (760, 30))

        if self.player_name_editing_mode:
            if self.player_name_cursor_compteur > 20:
                curseur = self.create_rect_alpha((2, self.player_name_text.get_height() - 16), (0, 0, 0), 200)
                surface.blit(curseur, (665 + self.player_name_text.get_width(), 16))

            self.player_name_cursor_compteur += 1
            if self.player_name_cursor_compteur > 40:
                self.player_name_cursor_compteur = 0
        else:
            if self.player_name_rect.collidepoint(possouris) and not self.ingame_window.is_hovering(possouris):
                surface.blit(self.player_name_hover, (0, 0))

    def update_player_lv(self, surface):
        """
        Methode d'actualisation de l'affichage du niveau du joueur.

        @in : surface, pygame.Surface → fenêtre du jeu
        """
        self.player_lv_image = self.font_size3.render(str(self.game.player.level), False, (124, 124, 124))
        if self.game.player.level >= 10:
            surface.blit(self.player_lv_image, (955, 73))
        else:
            surface.blit(self.player_lv_image, (965, 73))

    def update_hover_pokemon(self):
        """
        Methode d'actualisation du pokémon sur lequel pointe le curseur de souris.
        """
        is_a_pk_hover = False
        for pk_i in range(6):
            if self.current_hover_pokemon_register[pk_i]:
                self.current_hover_pokemon = pk_i
                is_a_pk_hover = True
        if not is_a_pk_hover:
            self.current_hover_pokemon = None

    def update_player_name_editing_mode(self, surface):
        """
        Methode d'actualisation de l'affichage du mode d'edition du nom du joueur.

        @in : surface, pygame.Surface → fenêtre du jeu
        """
        if self.player_name_editing_mode:
            surface.blit(self.mode_changement_pseudo_image, (0, 0))

    def update_team_pokemons(self, surface, possouris):
        """
        Methode d'actualisation de l'affichage de l'equipe du joueur.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """
        # Bouton delete pokemon
        if self.pk_move_mode:
            if self.delete_pk_button_rect.collidepoint(possouris):
                surface.blit(self.delete_pk_button,
                             (self.delete_pk_button_rect.x + 3, self.delete_pk_button_rect.y + 4),
                             (183, 0, 183, 183))
            else:
                surface.blit(self.delete_pk_button,
                             (self.delete_pk_button_rect.x + 3, self.delete_pk_button_rect.y + 4),
                             (0, 0, 183, 183))

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
        """
        Méthode d'actualisation de l'affichage du pokémon dans l'équipe.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        @in : i, int → indice du pokémon dans l'équipe
        """

        pk = self.game.player.team[i]

        if self.pk_move_mode and self.moving_pk[i]:
            pk_rect = pygame.Rect(possouris[0] - self.moving_pk_rel_possouris[0],
                                  possouris[1] - self.moving_pk_rel_possouris[1],
                                  369,
                                  69)

        else:
            pk_rect = self.pk_rects[i].copy()

        if pk is not None:
            if not self.ingame_window.sac_panel.emp_move_mode and \
                    not self.ingame_window.spawn_panel.spawning_pk_move_mode and not self.ingame_window.moving:
                self.update_pk_move(possouris, i)

            if i in (0, 2, 4):
                color = (255, 255, 255)
            else:
                color = (163, 171, 255)

            if self.pk_rects[i].collidepoint(possouris) and not self.ingame_window.is_hovering(possouris):
                surface.blit(self.create_rect_alpha((369, 69), color), (self.pk_rects[i].x, self.pk_rects[i].y))

            d = ((1272 - pk_rect.x) ** 2 + (637 - pk_rect.y) ** 2) ** 0.5

            alpha = 1582 + 255 - d*3
            if alpha < 0:
                alpha = 0

            # Variables
            icon = pk.icon_image.convert_alpha()
            name = self.pokemon_name_font.render(pk.name, False, (0, 0, 0)).convert_alpha()
            level = self.pokemon_level_font.render('Lv.' + str(pk.level), False, (0, 0, 0)).convert_alpha()

            type_color = game_infos.get_type_color(pk.get_type())
            type_name_to_print = game_infos.get_type_name_to_print(pk.get_type())
            type1_render = self.font_pokemon_type.render(type_name_to_print, False, type_color).convert_alpha()

            type2 = pk.get_type2()
            if not type2 == 'NoType':
                type2_color = game_infos.get_type_color(type2)
                type2_name_to_print = game_infos.get_type_name_to_print(type2)
                type2_render = self.font_pokemon_type.render(type2_name_to_print, False, type2_color).convert_alpha()

            pv = self.pokemon_hp_font.render(str(pk.health) + "/" + str(pk.pv), False, (0, 0, 0)).convert_alpha()

            # Alpha
            icon.set_alpha(alpha)
            name.set_alpha(alpha)
            level.set_alpha(alpha)
            type1_render.set_alpha(alpha)
            if type2 != 'NoType':
                type2_render.set_alpha(alpha)
            pv.set_alpha(alpha)

            surface.blit(icon, (pk_rect.x, pk_rect.y - 5), (0, 0, 64, 64))
            surface.blit(name, (pk_rect.x + 70, pk_rect.y + 13))
            surface.blit(level, (pk_rect.x + 60, pk_rect.y + 42))
            surface.blit(type1_render, (pk_rect.x + level.get_width() + 65, pk_rect.y + 42))
            if not pk.is_alive:
                ko = self.pokemon_hp_font.render('KO', False, (180, 0, 0)).convert_alpha()
                ko.set_alpha(alpha)
                surface.blit(ko, (pk_rect.x + 215 + pv.get_width(), pk_rect.y + 40))

            if not type2 == 'NoType':
                surface.blit(type2_render, (pk_rect.x + level.get_width() + type1_render.get_width() + 68, pk_rect.y + 42))

            back_bar = self.create_rect_alpha((150, 17), (35, 35, 35), alpha)
            front_bar = self.create_rect_alpha((pk.health / pk.pv * 150, 17), (42, 214, 0), alpha)

            surface.blit(back_bar, (pk_rect.x + 205, pk_rect.y + 26))
            surface.blit(front_bar, (pk_rect.x + 205, pk_rect.y + 26))

            surface.blit(pv, (pk_rect.x + 205, pk_rect.y + 40))

            if pk.objet_tenu is not None:
                item_tenu = self.font_pokemon_type.render('ITEM', False, (30, 30, 30)).convert_alpha()
                item_tenu.set_alpha(alpha)
                surface.blit(item_tenu,
                             (pk_rect.x + 327, pk_rect.y + 6))

            bg_rect = self.create_rect_alpha((86, 86), (255, 255, 255), 200 - alpha)

            bg_rect2 = pygame.Surface((98, 98), pygame.SRCALPHA).convert_alpha()
            bg_rect2.set_alpha(220 - alpha)
            pygame.draw.rect(bg_rect2, (0, 0, 0), bg_rect2.get_rect(), width=4)

            icon2 = pygame.transform.scale(pk.icon_image, (220, 110)).convert_alpha()
            level2 = self.pokemon_level_font.render('Lv.' + str(pk.level), False, (0, 0, 0)).convert_alpha()
            back_bar2 = self.create_rect_alpha((55, 6), (35, 35, 35), 255-alpha)
            front_bar2 = self.create_rect_alpha((pk.health / pk.pv * 55, 6), (42, 214, 0), 255-alpha)

            icon2.set_alpha(255-alpha)
            level2.set_alpha(255-alpha)

            if self.pk_move_mode:
                surface.blit(bg_rect, (possouris[0] - 43, possouris[1] - 43))
                surface.blit(bg_rect2, (possouris[0] - 49, possouris[1] - 49))
                surface.blit(icon2, (possouris[0] - 55, possouris[1] - 65), (0, 0, 100, 100))
                surface.blit(level2, (possouris[0] + 20, possouris[1] + 24))
                surface.blit(back_bar2, (possouris[0] - 40, possouris[1] + 35))
                surface.blit(front_bar2, (possouris[0] - 40, possouris[1] + 35))

        if self.pk_rects[i].collidepoint(possouris):

            if not self.ingame_window.is_hovering(possouris):
                self.current_hover_pokemon_register[i] = True

                if self.ingame_window.sac_panel.emp_move_mode:
                    if self.game.player.team[i] is not None:
                        if self.ingame_window.sac_panel.selected_item.target_pokemon == 'All' or \
                                self.game.player.team[
                                    i].name == self.ingame_window.sac_panel.selected_item.target_pokemon:

                            if 'Use' in self.ingame_window.sac_panel.selected_item.fonctionnement:
                                surface.blit(self.item_pk_hover_use,
                                             (self.PK_RECTS[i].x - 3, self.PK_RECTS[i].y - 2))
                            elif 'Give' in self.ingame_window.sac_panel.selected_item.fonctionnement:
                                if self.game.player.team[i].objet_tenu is None:
                                    surface.blit(self.item_pk_hover_give,
                                                 (self.PK_RECTS[i].x - 3, self.PK_RECTS[i].y - 2))
                                else:
                                    surface.blit(self.item_pk_hover_give_error,
                                                 (self.PK_RECTS[i].x - 3, self.PK_RECTS[i].y - 2))
                            else:
                                surface.blit(self.item_pk_hover_error,
                                             (self.PK_RECTS[i].x - 3, self.PK_RECTS[i].y - 2))
                        else:
                            surface.blit(self.item_pk_hover_error, (self.PK_RECTS[i].x - 3, self.PK_RECTS[i].y - 2))
        else:
            self.current_hover_pokemon_register[i] = False

    def update_pk_move(self, possouris, i):
        """
        Méthode d'actualisation du déplacement du pokémon par le joueur sur le panel de jeu.

        @in : possouris, list → coordonnées du pointeur de souris
        @in : i, int → indice du pokémon dans l'équipe
        """

        if not self.pk_move_mode:
            if not self.player_name_editing_mode and not self.ingame_window.is_hovering(possouris) and not self.ingame_window.train_panel.pk_move_mode:
                if self.game.mouse_pressed[1] and self.pk_rects[i].collidepoint(possouris):
                    self.pk_move_mode = True
                    self.moving_pk[i] = True
                    self.moving_pk_rel_possouris = (possouris[0] - self.pk_rects[i].x,
                                                    possouris[1] - self.pk_rects[i].y)
        else:
            if self.moving_pk[i]:
                if not self.game.mouse_pressed[1]:
                    if self.delete_pk_button_rect.collidepoint(possouris):
                        if self.game.player.get_nb_team_members() != 1:
                            self.game.player.team[i] = None
                    elif self.pk_rects[0].collidepoint(possouris):
                        self.change_pk_place(i, 0)
                    elif self.pk_rects[1].collidepoint(possouris):
                        self.change_pk_place(i, 1)
                    elif self.pk_rects[2].collidepoint(possouris):
                        self.change_pk_place(i, 2)
                    elif self.pk_rects[3].collidepoint(possouris):
                        self.change_pk_place(i, 3)
                    elif self.pk_rects[4].collidepoint(possouris):
                        self.change_pk_place(i, 4)
                    elif self.pk_rects[5].collidepoint(possouris):
                        self.change_pk_place(i, 5)
                    elif self.ingame_window.current_panel_name == 'Evolutions' and self.ingame_window.is_open and self.ingame_window.evol_panel.evolving_pk_rect.collidepoint(possouris):
                        self.ingame_window.evol_panel.update_evolving_pk()
                    elif self.ingame_window.current_panel_name == 'Train' and self.ingame_window.is_open and self.ingame_window.train_panel.training_pk_rect.collidepoint(possouris):
                        self.ingame_window.train_panel.update_training_pk()
                    elif self.boolFight_popup:
                        if self.fight_popup_drop_pk_rect.collidepoint(possouris):
                            if self.game.player.team[i].is_alive:
                                self.fighting_pk = self.game.player.team[i]
                                self.start_fight()
                                self.boolFight_popup = False

                    self.pk_move_mode = False
                    self.moving_pk[i] = False

    def update_pokemon_info(self, surface, possouris):
        """
        Méthode d'actualisation de l'affichage des infos du pokémon dans l'équipe.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """
        if self.pokemon_info_mode:
            if pygame.Rect(1210, 9, 59, 59).collidepoint(possouris):
                surface.blit(self.pokemon_info_popup_x_button_hover, (0, 0))
            else:
                surface.blit(self.pokemon_info_popup, (0, 0))

            if self.pokemon_info is not None:
                surface.blit(pygame.transform.scale(self.pokemon_info.icon_image, (280, 140)),
                             (900, 0), (0, 0, 140, 140))
                surface.blit(self.font_pokemon_info_name.render(self.pokemon_info.name, False,
                                                                (0, 0, 0)), (1038, 15))
                surface.blit(
                    self.font_pokemon_info_values.render(str(self.pokemon_info.pv), False,
                                                         (2, 137, 0)), (1070, 43))
                surface.blit(
                    self.font_pokemon_info_values.render(str(self.pokemon_info.attack), False,
                                                         (189, 0, 0)), (1070, 66))
                surface.blit(
                    self.font_pokemon_info_values.render(str(self.pokemon_info.defense), False,
                                                         (191, 200, 0)), (1070, 89))
                surface.blit(
                    self.font_pokemon_info_values.render(str(self.pokemon_info.speed), False,
                                                         (0, 139, 230)), (1070, 112))
                surface.blit(
                    self.font_pokemon_info_lv.render(str(self.pokemon_info.level), False,
                                                     (0, 0, 0)), (965, 139))

                if self.pokemon_info.objet_tenu is not None:

                    if self.pokemon_info_obj_rect.collidepoint(possouris):
                        surface.blit(self.create_rect_alpha((70, 70), (255, 255, 255)), self.pokemon_info_obj_rect)
                    surface.blit(
                        pygame.transform.scale(self.pokemon_info.objet_tenu.icon_image,
                                               (70, 70)),
                        (self.pokemon_info_obj_rect.x + 2, self.pokemon_info_obj_rect.y))
            else:
                surface.blit(self.pokemon_info_popup_unknown, (0, 0))

    def update_cursor(self, possouris):
        """
        Méthode d'actualisation du pointeur de la souris.

        @in : possouris, list → coordonnées du pointeur de souris
        """
        if self.get_interactions(possouris=possouris):
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def update_go_fight_button(self, surface, possouris):
        """
        Méthode d'actualisation de l'affichage du bouton "Go fight".

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """

        if not self.go_fight_button_rect.collidepoint(possouris) or self.ingame_window.is_hovering(possouris):
            if self.go_fight_button_compteur < 50:
                surface.blit(self.go_fight_button, self.go_fight_button_rect)
            else:
                surface.blit(self.go_fight_button_v2, self.go_fight_button_rect)
        else:
            surface.blit(self.go_fight_button_hover, self.go_fight_button_rect)

        self.go_fight_button_compteur += 1
        if self.go_fight_button_compteur > 100:
            self.go_fight_button_compteur = 0

    def start_fight(self):
        """
        Méthode démarrage de combat
        """
        self.game.start_fight(self.fighting_pk, fight_type='Boss')

    def next_turn(self):
        """
        Méthode de passage au tour suivant
        """
        self.ingame_window.reset_all_panels()

    # INTERACTIONS -----------------------------

    def left_clic_interactions(self, possouris):
        """
        Méthode gérant les intéractions de l'utilisateur avec le clic gauche de la souris.

        @in : possouris, list → coordonnées du pointeur de souris
        """
        if not self.pk_move_mode and not self.player_name_editing_mode:
            if self.player_name_rect.collidepoint(possouris):
                self.player_name_editing_mode = True
                self.game.player.reset_name()
                self.update_player_name()

                self.pokemon_info_mode = False

                if self.ingame_window.is_open:
                    self.ingame_window.close()

            if not self.boolFight_popup:
                if self.buttons.spawn_button_rect.collidepoint(possouris):
                    if self.buttons.unlocked_buttons['Spawn']:
                        self.ingame_window.update_panel('Spawn')
                        self.ingame_window.open()
                        self.ingame_window.maximize()
                elif self.buttons.train_button_rect.collidepoint(possouris):
                    if self.buttons.unlocked_buttons['Train']:
                        self.ingame_window.update_panel('Train')
                        self.ingame_window.open()
                        self.ingame_window.maximize()
                elif self.buttons.grind_button_rect.collidepoint(possouris):
                    if self.buttons.unlocked_buttons['Grind']:
                        self.ingame_window.update_panel('Grind')
                        self.ingame_window.open()
                        self.ingame_window.maximize()
                elif self.buttons.items_button_rect.collidepoint(possouris):
                    if self.buttons.unlocked_buttons['Items']:
                        self.ingame_window.update_panel('Items')
                        self.ingame_window.open()
                        self.ingame_window.maximize()
                elif self.buttons.evol_button_rect.collidepoint(possouris):
                    if self.buttons.unlocked_buttons['Evol']:
                        self.ingame_window.update_panel('Evolutions')
                        self.ingame_window.open()
                        self.ingame_window.maximize()

            if self.sac_button_rect.collidepoint(possouris):
                self.ingame_window.update_panel("Sac d'objets")
                self.ingame_window.open()
                self.ingame_window.maximize()

            if self.game.player.actions <= 0:
                if not self.boolFight_popup:
                    if self.go_fight_button_rect.collidepoint(possouris):
                        self.boolFight_popup = True
                else:
                    if self.fight_popup_x_button_rect.collidepoint(possouris):
                        self.boolFight_popup = False

            if self.pokemon_info_mode:
                if pygame.Rect(1210, 9, 59, 59).collidepoint(possouris):
                    self.pokemon_info_mode = False
                elif self.pokemon_info_obj_rect.collidepoint(possouris):
                    item = self.pokemon_info.objet_tenu
                    if item is not None:
                        self.pokemon_info.objet_tenu = None
                        self.game.player.add_sac_item(item)

        elif self.player_name_editing_mode:
            if not self.player_name_rect.collidepoint(possouris):
                if self.game.player.name == "":
                    self.game.player.name = 'Nom'
                    self.update_player_name()
                self.player_name_editing_mode = False

    def right_clic_interactions(self, possouris):
        """
        Méthode gérant les intéractions de l'utilisateur avec le clic droit de la souris.

        @in : possouris, list → coordonnées du pointeur de souris
        """
        if not self.player_name_editing_mode:

            i = 0
            for pk_rect in self.pk_rects:
                if pk_rect.collidepoint(possouris):
                    self.pokemon_info = self.game.player.team[i]
                    self.pokemon_info_mode = True
                i += 1

    def keydown(self, event_key):
        """
        Méthode gérant les intéractions de l'utilisateur avec le clavier.

        @in : event_key, int → valeur associée à la touche appuyée
        """
        if event_key == pygame.K_RETURN:
            if self.game.player.name == "":
                self.game.player.name = "Nom"
                self.update_player_name()
            self.player_name_editing_mode = False
        else:
            self.game.player.edit_name(event_key)

    def get_interactions(self, possouris):
        """
        Méthode qui retourne True si la souris est positionnée sur un bouton.

        @in : possouris, list → coordonnées du pointeur de souris
        @out : bool
        """
        if self.ingame_window.is_hovering(possouris):
            return self.ingame_window.is_hovering_buttons(possouris) or self.pk_move_mode
        elif self.player_name_editing_mode:
            return self.player_name_rect.collidepoint(possouris)
        else:
            if self.player_name_rect.collidepoint(possouris):
                if self.pokemon_info_mode:
                    if not self.pokemon_info_popup_rect.collidepoint(possouris):
                        return True
                    else:
                        return False
                else:
                    return True

            elif self.pk_move_mode:
                return True
            elif self.sac_button_rect.collidepoint(possouris):
                return True
            elif self.is_hovering_team_pokemon(possouris):
                return True
            elif self.boolFight_popup:
                if self.fight_sac_button_rect.collidepoint(possouris) or self.fight_equipe_button_rect.collidepoint(possouris):
                    return True
                elif self.fight_popup_x_button_rect.collidepoint(possouris):
                    return True
            elif self.game.player.actions <= 0 and self.go_fight_button_rect.collidepoint(possouris):
                return True
            elif self.buttons.is_hovering_button(possouris):
                return not self.boolFight_popup
            elif self.is_hovering_pokemon_info_popup_buttons(possouris):
                return True
            else:
                return False

    def create_rect_alpha(self, dimensions, color, alpha=90):
        rect = pygame.Surface(dimensions)
        rect.set_alpha(alpha)
        rect.fill(color)
        return rect

    def change_pk_place(self, i1, i2):
        """
        Méthode d'inversion de place de 2 pokémons dans l'équipe.

        @in : i1, int → indice du pokémon 2 dans l'équipe
        @in : i2, int → indice du pokémon 2 dans l'équipe
        """
        if not i1 == i2 and not (i2 is None):
            self.game.player.team[i1], self.game.player.team[i2] = self.game.player.team[i2], self.game.player.team[i1]

    def is_hovering_team_pokemon(self, possouris) -> bool:
        """
        Méthode qui retourne True si la souris est positionnée sur un pokémon de l'équipe.

        @in : possouris, list → coordonnées du pointeur de souris
        @out : bool
        """
        if not self.pk_rects[0].collidepoint(possouris) and not self.pk_rects[1].collidepoint(possouris):
            if not self.pk_rects[2].collidepoint(possouris) and not self.pk_rects[3].collidepoint(possouris):
                if not self.pk_rects[4].collidepoint(possouris) and not self.pk_rects[5].collidepoint(possouris):
                    return False
        return True

    def is_hovering_pokemon_info_popup_buttons(self, possouris) -> bool:
        """
        Méthode qui retourne True si la souris est positionnée sur un bouton du popup d'infos des pokémons.

        @in : possouris, list → coordonnées du pointeur de souris
        @out : bool
        """
        if pygame.Rect(1210, 9, 59, 59).collidepoint(possouris):
            return True
        elif pygame.Rect(1166, 141, 74, 74).collidepoint(possouris) and self.pokemon_info is not None and self.pokemon_info.objet_tenu is not None:
            return True

        return False


class GamePanelButtons:
    """
    Classe gérant les boutons d'action du panel principal du jeu.
    """

    def __init__(self):
        self.unlocked_buttons = {'Spawn': True,
                                 'Train': True,
                                 'Grind': False,
                                 'Items': True,
                                 'Evol': True
                                 }
        # SPAWN BUTTON
        self.spawn_button = pygame.image.load('assets/game/panels/classic_panel/spawn_button.png')
        self.spawn_button_rect = self.get_custom_rect(self.spawn_button, 37, 133, 250, 250)

        self.spawn_button_hover = pygame.image.load('assets/game/panels/classic_panel/spawn_button_hover.png')
        self.spawn_button_pos = (32, 136)

        # TRAIN BUTTON
        self.train_button = pygame.image.load('assets/game/panels/classic_panel/train_button.png')
        self.train_button_rect = self.get_custom_rect(self.train_button, 319, 133, 250, 250)

        self.train_button_hover = pygame.image.load('assets/game/panels/classic_panel/train_button_hover.png')

        self.train_button_pos = (317, 136)

        # GRIND BUTTON
        self.grind_button = pygame.image.load('assets/game/panels/classic_panel/grind_button.png')
        self.grind_button_rect = self.get_custom_rect(self.grind_button, 607, 133, 250, 250)

        self.grind_button_hover = pygame.image.load('assets/game/panels/classic_panel/grind_button_hover.png')

        self.grind_button_pos = (602, 136)

        # ITEMS BUTTON
        self.items_button = pygame.image.load('assets/game/panels/classic_panel/items_button.png')
        self.items_button_rect = self.get_custom_rect(self.items_button, 72, 417, 250, 250)

        self.items_button_hover = pygame.image.load('assets/game/panels/classic_panel/items_button_hover.png')

        self.items_button_pos = (68, 420)

        # EVOL BUTTON
        self.evol_button = pygame.image.load('assets/game/panels/classic_panel/evol_button.png')
        self.evol_button_rect = self.get_custom_rect(self.evol_button, 357, 417, 250, 250)

        self.evol_button_hover = pygame.image.load('assets/game/panels/classic_panel/evol_button_hover.png')

        self.evol_button_pos = (352, 420)

        # EDIT BUTTON
        self.edit_actions_button = pygame.image.load('assets/game/panels/classic_panel/edit_actions_button.png')
        self.edit_actions_button_rect = self.get_custom_rect(self.edit_actions_button, 515, 11)

        self.edit_actions_button_hover = pygame.image.load('assets/game/panels/classic_panel/edit_actions_button_hover.png')

    def update(self, surface, possouris, ingame_window):
        """
        Méthode d'actualisation de l'affichage des boutons d'action du panel principal du jeu.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        @in : ingame_window, ingame_window.IngameWindow → fenêtre ingame du jeu
        """

        if self.edit_actions_button_rect.collidepoint(possouris) and not ingame_window.is_hovering(possouris):
            surface.blit(self.edit_actions_button_hover, self.edit_actions_button_rect)
        else:
            surface.blit(self.edit_actions_button, self.edit_actions_button_rect)

        if self.unlocked_buttons['Spawn']:
            if self.spawn_button_rect.collidepoint(possouris) and not ingame_window.is_hovering(possouris):
                surface.blit(self.spawn_button, self.spawn_button_pos)
                surface.blit(self.spawn_button_hover, self.spawn_button_pos)
            else:
                surface.blit(self.spawn_button, self.spawn_button_pos)

        if self.unlocked_buttons['Train']:
            if self.train_button_rect.collidepoint(possouris) and not ingame_window.is_hovering(possouris):
                surface.blit(self.train_button, self.train_button_pos)
                surface.blit(self.train_button_hover, self.train_button_pos)
            else:
                surface.blit(self.train_button, self.train_button_pos)

        if self.unlocked_buttons['Grind']:
            if self.grind_button_rect.collidepoint(possouris) and not ingame_window.is_hovering(possouris):
                surface.blit(self.grind_button, self.grind_button_pos)
                surface.blit(self.grind_button_hover, self.grind_button_pos)
            else:
                surface.blit(self.grind_button, self.grind_button_pos)

        if self.unlocked_buttons['Items']:
            if self.items_button_rect.collidepoint(possouris) and not ingame_window.is_hovering(possouris):
                surface.blit(self.items_button, self.items_button_pos)
                surface.blit(self.items_button_hover, self.items_button_pos)
            else:
                surface.blit(self.items_button, self.items_button_pos)

        if self.unlocked_buttons['Evol']:
            if self.evol_button_rect.collidepoint(possouris) and not ingame_window.is_hovering(possouris):
                surface.blit(self.evol_button, self.evol_button_pos)
                surface.blit(self.evol_button_hover, self.evol_button_pos)
            else:
                surface.blit(self.evol_button, self.evol_button_pos)

    def get_custom_rect(self, image, rectx=None, recty=None, rectw=None, recth=None):
        image_rect = image.get_rect()
        if rectx is not None:
            image_rect.x = rectx
        if recty is not None:
            image_rect.y = recty
        if rectw is not None:
            image_rect.w = rectw
        if recth is not None:
            image_rect.h = recth

        return image_rect

    def is_hovering_button(self, possouris):
        if self.edit_actions_button_rect.collidepoint(possouris):
            return True
        elif self.spawn_button_rect.collidepoint(possouris):
            if self.unlocked_buttons['Spawn']:
                return True
        elif self.train_button_rect.collidepoint(possouris):
            if self.unlocked_buttons['Train']:
                return True
        elif self.grind_button_rect.collidepoint(possouris):
            if self.unlocked_buttons['Grind']:
                return True
        elif self.items_button_rect.collidepoint(possouris):
            if self.unlocked_buttons['Items']:
                return True
        elif self.evol_button_rect.collidepoint(possouris):
            if self.unlocked_buttons['Evol']:
                return True
        else:
            return False