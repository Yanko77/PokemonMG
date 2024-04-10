"""
Fichier qui gère l'action "Train" du jeu.
"""

# Importation des modules

import pygame
import random

import game_infos
import pokemon
import dresseur

# Définition des classes


class TrainPanel:
    """
    Classe représentant le panel de l'action "Train".
    Dans ce panel, le joueur pourra affronter entrainer ses pokémon en lançant un combat dont il pourra choisir la
        difficulté.
    """

    def __init__(self, game):
        self.game = game

        # FONTS
        self.info_select_pk_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 22)
        self.ennemy_pk_name_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 22)
        self.ennemy_pk_type_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 17)
        self.ennemy_pk_stats_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 20)

        self.pokemon_level_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 15)
        # CONSTANTES
        self.PATH = 'assets/game/ingame_windows/Train/'

        self.LV_DIFFICULT_COEFS = {
            'easy': (0.6, 1.2),
            'normal': (0.7, 1.3),
            'hard': (0.8, 1.4)
        }

        self.DIFF_COLORS = {
            'easy': (0, 140, 0),
            'normal': (255, 180, 0),
            'hard': (150, 0, 0)
        }

        self.ENNEMY_PK_PREVIEW_DIFF_TEXT = {
            'easy': self.ennemy_pk_type_font.render('EASY', False, self.DIFF_COLORS['easy']),
            'normal': self.ennemy_pk_type_font.render('NORMAL', False, self.DIFF_COLORS['normal']),
            'hard': self.ennemy_pk_type_font.render('HARD', False, self.DIFF_COLORS['hard']),
        }
        self.ennemy_pk_preview_diff_text_pos = (700, 367)

        # Chargement des images
        self.background = self.img_load('background')  # Background
        self.background_pos = (-12, -21)

        self.training_pk_emp = self.img_load('emp_training_pk')  # Emplacement du pokemon à entrainer
        self.training_pk_emp_pos = (78, 96)
        self.locked = self.img_load('locked')
        self.locked_pos = (70, 80)

        self.diff_ind = {'easy': self.img_load('diff_ind_easy'),  # Indicateur de difficulté
                         'normal': self.img_load('diff_ind_normal'),
                         'hard': self.img_load('diff_ind_hard')}
        self.diff_ind_pos = (80, 177)

        self.ennemy_pk_popup = self.img_load('ennemy_pk_popup')
        self.ennemy_pk_popup_pos = (446, 39)

        self.fight_button = self.img_load('fight_button')  # Bouton FIGHT
        self.fight_button_h = self.img_load('fight_button_hover')
        self.fight_button_rect = pygame.Rect(613, 448, 266, 73)

        self.settings_button = self.img_load('settings_button')  # Bouton SETTINGS
        self.settings_button_h = self.img_load('settings_button_hover')
        self.settings_button_rect = pygame.Rect(22, 90, 90, 120)

        self.ennemy_pk_infos_stats_button = self.img_load('info_stats_button')  # Bouton INFOS STATS
        self.ennemy_pk_infos_stats_button_h = self.img_load('info_stats_button_hover')
        self.ennemy_pk_infos_stats_button_rect = pygame.Rect(715, 408, 105, 31)
        
        self.settings_popup = self.img_load('settings_popup')  # Popup SETTINGS
        self.settings_popup_pos = (59, 59)
        
        self.easy_button = self.img_load('easy_button')  # Bouton EASY
        self.easy_button_h = self.img_load('easy_button_hover')
        self.easy_button_rect = pygame.Rect(92, 68, 74, 44)
        
        self.normal_button = self.img_load('normal_button')  # Bouton NORMAL
        self.normal_button_h = self.img_load('normal_button_hover')
        self.normal_button_rect = pygame.Rect(171, 68, 74, 44)
        
        self.hard_button = self.img_load('hard_button')  # Bouton HARD
        self.hard_button_h = self.img_load('hard_button_hover')
        self.hard_button_rect = pygame.Rect(249, 68, 74, 44)
        
        # Pré-chargement des textes
        self.no_pk_selected_text = self.info_select_pk_font.render('NO POKEMON SELECTED', False, (255, 255, 255))
        self.no_pk_selected_text_pos = (90, 65)

        # Rects
        self.training_pk_rect = pygame.Rect(103, 115, 268, 268)

        # Variables relatives au pokémon à entrainer
        self.training_pk = None

        # Variables relatives au jeu
        self.difficult = 'easy'
        self.boolEnnemy_pk_stats = False

        # Variables relatives aux pokémons ennemis
        self.ennemy_pks = {
            'easy': self.spawn_ennemy_pk('easy'),
            'normal': self.spawn_ennemy_pk('normal'),
            'hard': self.spawn_ennemy_pk('hard')
        }
        self.ennemy_pk = self.ennemy_pks[self.difficult]

        self.ennemy_pks_backup = {}

        self.set_ennemy_pks()
        self.load_ennemy_pk()

        self.ennemy_pk_icon_pos = (455, 273)
        self.ennemy_pk_name_pos = (617, 317)
        self.ennemy_pk_type1_pos = (670, 346)
        self.ennemy_pk_type2_pos = (675, 346)
        self.ennemy_pk_pv_pos = (653, 348)
        self.ennemy_pk_atk_pos = (653, 373)
        self.ennemy_pk_def_pos = (749, 348)
        self.ennemy_pk_vit_pos = (749, 373)
        #
        self.pk_move_mode = False
        self.moving_pk_rel_possouris = (0, 0)

        # Variables relatives aux popups
        self.boolSettings_popup = False
        self.boolAdd_training_pk_popup = False

        self.stats_popup = self.img_load('ennemy_pk_stats')
        self.stats_popup_pos = (612, 352)

        # Variables de la fenetre ingame
        self.window_pos = [0, 0]

    # Méthodes d'affichage

    def update(self, surface, possouris, window):
        """
        Méthode d'actualisation de l'affichage du panel.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        @in : window_pos, list → coordonnées de la fenêtre ingame
        """

        window_pos = window.basic_window_pos

        # Actualiser les variables relatives à la position de la fenetre ingame
        if self.window_pos != window_pos:
            self.update_all_rects(window_pos)

        # Affichage du background
        surface.blit(self.background, self.background_pos)

        # Gestion des affichages relatifs au pokémon à entrainer
        if self.training_pk is not None:

            # Afficher la preview du pokemon ennemi
            self.update_ennemy_preview(surface, possouris)

            # Afficher le bouton FIGHT
            if self.fight_button_rect.collidepoint(possouris):
                surface.blit(self.fight_button_h, self.fight_button_rect)
            else:
                surface.blit(self.fight_button, self.fight_button_rect)

        # Affichage de l'emplacement du pokemon à entrainer
        self.update_training_pk_emp(surface, possouris)

        # Affichage du popup SETTINGS
        if self.boolSettings_popup:
            self.update_settings_popup(surface, possouris)

    def update_training_pk_emp(self, surface, possouris):
        """
        Methode d'actualisation de l'affichage de l'emplacement du pokémon à entrainer du joueur.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """

        # Affichage de l'emplacement
        surface.blit(self.training_pk_emp, self.training_pk_emp_pos)

        # Affichage de l'indicateur de difficulté
        surface.blit(self.diff_ind[self.difficult], self.diff_ind_pos)

        # Affichage du bouton SETTINGS
        if self.settings_button_rect.collidepoint(possouris):
            surface.blit(self.settings_button_h, (self.settings_button_rect.x + 13,
                                                  self.settings_button_rect.y + 10))
        else:
            surface.blit(self.settings_button, (self.settings_button_rect.x + 13,
                                                self.settings_button_rect.y + 10))

        # Affichage de l'effet d'hovering sur le pokémon de l'emplacement
        if self.training_pk_rect.collidepoint(possouris):
            surface.blit(self.create_rect_alpha((self.training_pk_rect.w, self.training_pk_rect.h),
                                                 (100, 100, 100)),
                         (self.training_pk_rect.x, self.training_pk_rect.y))

        # Affichages des boutons relatifs au pokémon à entrainer
        if self.training_pk is None:
            # Affichage du texte NO SELECTED PK
            surface.blit(self.no_pk_selected_text, self.no_pk_selected_text_pos)

            # Affichage de l'emplacement bloqué
            surface.blit(self.locked, self.locked_pos)

        else:
            if self.pk_move_mode:
                pk_rect = pygame.Rect(possouris[0] - self.moving_pk_rel_possouris[0],
                                      possouris[1] - self.moving_pk_rel_possouris[1],
                                      252,
                                      252)
            else:
                pk_rect = self.training_pk_rect.copy()

            # Affichages des boutons relatifs au popup ADD_TRAINING_PK
            if self.boolAdd_training_pk_popup:

                # Affichage du bouton +
                if self.add_button_rect.collidepoint(possouris):
                    surface.blit(self.add_button_h, self.add_button_rect)
                else:
                    surface.blit(self.add_button, self.add_button_rect)
            else:

                d = ((141 + self.window_pos[0] - pk_rect.x) ** 2 + (139 + self.window_pos[1] - pk_rect.y) ** 2) ** 0.5

                alpha = 208 + 255 - d * 3
                if alpha < 0:
                    alpha = 0

                # Variables
                icon = pygame.transform.scale(self.training_pk.icon_image, (520, 260)).convert_alpha()

                # Alpha
                icon.set_alpha(alpha)
                surface.blit(icon, (pk_rect.x, pk_rect.y - 25), (0, 0, 250, 250))

                # Quand on bouge
                bg_rect = self.create_rect_alpha((86, 86), (255, 255, 255), 200 - alpha)

                bg_rect2 = pygame.Surface((98, 98), pygame.SRCALPHA).convert_alpha()
                bg_rect2.set_alpha(220 - alpha)
                pygame.draw.rect(bg_rect2, (0, 0, 0), bg_rect2.get_rect(), width=4)

                icon2 = pygame.transform.scale(self.training_pk.icon_image, (220, 110)).convert_alpha()
                level2 = self.pokemon_level_font.render('Lv.' + str(self.training_pk.level), False,
                                                        (0, 0, 0)).convert_alpha()
                back_bar2 = self.create_rect_alpha((55, 6), (35, 35, 35), 255 - alpha)
                front_bar2 = self.create_rect_alpha((self.training_pk.health / self.training_pk.pv * 55, 6),
                                                    (42, 214, 0), 255 - alpha)

                icon2.set_alpha(255 - alpha)
                level2.set_alpha(255 - alpha)

                if self.pk_move_mode:
                    surface.blit(bg_rect, (possouris[0] - 43, possouris[1] - 43))
                    surface.blit(bg_rect2, (possouris[0] - 49, possouris[1] - 49))
                    surface.blit(icon2, (possouris[0] - 55, possouris[1] - 65), (0, 0, 100, 100))
                    surface.blit(level2, (possouris[0] + 20, possouris[1] + 24))
                    surface.blit(back_bar2, (possouris[0] - 40, possouris[1] + 35))
                    surface.blit(front_bar2, (possouris[0] - 40, possouris[1] + 35))

                if not self.pk_move_mode:
                    if self.game.mouse_pressed[1] and pk_rect.collidepoint(possouris):
                        if not self.game.classic_panel.pk_move_mode:
                            self.pk_move_mode = True
                            self.moving_pk_rel_possouris = (possouris[0] - self.training_pk_rect.x,
                                                            possouris[1] - self.training_pk_rect.y)
                else:
                    if not self.game.mouse_pressed[1]:
                        self.pk_move_mode = False

                        if self.game.classic_panel.PK_RECTS[0].collidepoint(possouris):
                            self.add_pk_to_team(0)
                        elif self.game.classic_panel.PK_RECTS[1].collidepoint(possouris):
                            self.add_pk_to_team(1)
                        elif self.game.classic_panel.PK_RECTS[2].collidepoint(possouris):
                            self.add_pk_to_team(2)
                        elif self.game.classic_panel.PK_RECTS[3].collidepoint(possouris):
                            self.add_pk_to_team(3)
                        elif self.game.classic_panel.PK_RECTS[4].collidepoint(possouris):
                            self.add_pk_to_team(4)
                        elif self.game.classic_panel.PK_RECTS[5].collidepoint(possouris):
                            self.add_pk_to_team(5)

    def update_ennemy_preview(self, surface, possouris):
        """
        Methode d'actualisation de l'affichage de la preview du pokemon ennemi.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """

        # Affichage du popup
        surface.blit(self.ennemy_pk_popup, self.ennemy_pk_popup_pos)

        # Affichage de l'icone du pokémon ennemi
        surface.blit(self.ennemy_pk_icon,
                     self.ennemy_pk_icon_pos,
                     (0, 0, 150, 150))

        # Affichage du nom du pokémon ennemi
        surface.blit(self.ennemy_pk_name,
                     self.ennemy_pk_name_pos)

        # Affichage du bouton STATS
        if self.ennemy_pk_infos_stats_button_rect.collidepoint(possouris):
            surface.blit(self.ennemy_pk_infos_stats_button_h, self.ennemy_pk_infos_stats_button_rect)
        else:
            surface.blit(self.ennemy_pk_infos_stats_button, self.ennemy_pk_infos_stats_button_rect)

        # Affichages relatifs aux stats
        if not self.boolEnnemy_pk_stats:

            # Affichage du type1 du pokémon ennemi
            surface.blit(self.ennemy_pk_type1, self.ennemy_pk_type1_pos)

            # Affichage du type 2 du pokémon ennemi, s'il en a un
            if self.ennemy_pk_type2 is not None:
                surface.blit(self.ennemy_pk_type2, (self.ennemy_pk_type2_pos[0] + self.ennemy_pk_type1.get_width(),
                                                    self.ennemy_pk_type2_pos[1]))

            # Affichage de la difficulté
            surface.blit(self.ENNEMY_PK_PREVIEW_DIFF_TEXT[self.difficult], self.ennemy_pk_preview_diff_text_pos)

        else:

            # Affichage du cache pour les stats
            surface.blit(self.stats_popup, self.stats_popup_pos)

            # Affichage des stats du pokémon
            surface.blit(self.ennemy_pk_pv, self.ennemy_pk_pv_pos)
            surface.blit(self.ennemy_pk_atk, self.ennemy_pk_atk_pos)
            surface.blit(self.ennemy_pk_def, self.ennemy_pk_def_pos)
            surface.blit(self.ennemy_pk_vit, self.ennemy_pk_vit_pos)

    def update_settings_popup(self, surface, possouris):
        """
        Méthode d'actualisation de l'affichage du popup "settings".

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """

        # Affichage du popup SETTINGS
        surface.blit(self.settings_popup, self.settings_popup_pos)

        # Affichage du bouton EASY
        if self.easy_button_rect.collidepoint(possouris):
            surface.blit(self.easy_button_h, self.easy_button_rect)
        else:
            surface.blit(self.easy_button, self.easy_button_rect)

        # Affichage du bouton NORMAL
        if self.normal_button_rect.collidepoint(possouris):
            surface.blit(self.normal_button_h, self.normal_button_rect)
        else:
            surface.blit(self.normal_button, self.normal_button_rect)

        # Affichage du bouton HARD
        if self.hard_button_rect.collidepoint(possouris):
            surface.blit(self.hard_button_h, self.hard_button_rect)
        else:
            surface.blit(self.hard_button, self.hard_button_rect)

    def update_training_pk(self):
        """
        Methode permettant de changer le pokémon à entrainer du joueur.
        """

        if self.training_pk is None:
            i = self.game.classic_panel.moving_pk.index(True)

            self.training_pk = self.game.player.team[i]
            self.set_ennemy_pks()
            self.load_ennemy_pk()
            self.game.player.team[i] = None

    def update_all_rects(self, window_pos):
        """
        Méthode d'actualisation des rects en fonction de la position de la fenêtre ingame.

        @in : window_pos, list → coordonnées de la fenêtre ingame
        """
        self.window_pos = window_pos.copy()

        self.background_pos = (-12 + self.window_pos[0], -21 + self.window_pos[1])
        self.training_pk_emp_pos = (78 + self.window_pos[0], 96 + self.window_pos[1])
        self.locked_pos = (70 + self.window_pos[0], 80 + self.window_pos[1])
        self.diff_ind_pos = (80 + self.window_pos[0], 177 + self.window_pos[1])
        self.ennemy_pk_popup_pos = (446 + self.window_pos[0], 39 + self.window_pos[1])
        self.fight_button_rect = pygame.Rect(613 + self.window_pos[0], 448 + self.window_pos[1], 266, 73)
        self.settings_button_rect = pygame.Rect(22 + self.window_pos[0], 90 + self.window_pos[1], 90, 120)
        self.add_button_rect = pygame.Rect(127 + self.window_pos[0], 144 + self.window_pos[1], 215, 215)
        self.ennemy_pk_infos_stats_button_rect = pygame.Rect(715 + self.window_pos[0], 408 + self.window_pos[1], 105,
                                                             31)
        self.settings_popup_pos = (59 + self.window_pos[0], 59 + self.window_pos[1])
        self.easy_button_rect = pygame.Rect(92 + self.window_pos[0], 68 + self.window_pos[1], 74,
                                            44 + self.window_pos[1])
        self.normal_button_rect = pygame.Rect(171 + self.window_pos[0], 68 + self.window_pos[1], 74, 44)
        self.hard_button_rect = pygame.Rect(249 + self.window_pos[0], 68 + self.window_pos[1], 74, 44)
        self.no_pk_selected_text_pos = (90 + self.window_pos[0], 65 + self.window_pos[1])
        self.training_pk_rect = pygame.Rect(103 + self.window_pos[0], 115 + self.window_pos[1], 268, 268)
        self.ennemy_pk_icon_pos = (455 + self.window_pos[0], 273 + self.window_pos[1])
        self.ennemy_pk_name_pos = (617 + self.window_pos[0], 317 + self.window_pos[1])
        self.ennemy_pk_type1_pos = (670 + self.window_pos[0], 346 + self.window_pos[1])
        self.ennemy_pk_type2_pos = (675 + self.window_pos[0], 346 + self.window_pos[1])
        self.ennemy_pk_pv_pos = (653 + self.window_pos[0], 348 + self.window_pos[1])
        self.ennemy_pk_atk_pos = (653 + self.window_pos[0], 373 + self.window_pos[1])
        self.ennemy_pk_def_pos = (749 + self.window_pos[0], 348 + self.window_pos[1])
        self.ennemy_pk_vit_pos = (749 + self.window_pos[0], 373 + self.window_pos[1])
        self.stats_popup_pos = (612 + self.window_pos[0], 352 + self.window_pos[1])
        self.ennemy_pk_preview_diff_text_pos = (700 + self.window_pos[0], 367 + self.window_pos[1])

    # Méthodes essentielles

    def start_fight(self):
        """
        Méthode de lancement de combat.
        """
        self.game.start_fight(self.training_pk, dresseur.Sauvage(self.game, self.ennemy_pks[self.difficult]), self.difficult)

    def open_settings_popup(self):
        """
        Méthode d'ouverture du popup "settings".
        """
        self.boolSettings_popup = True

    def close_settings_popup(self):
        """
        Méthode de fermeture du popup "settings".
        """
        self.boolSettings_popup = False

    # Méthodes annexes

    def spawn_ennemy_pk(self, diff) -> pokemon.Pokemon or None:
        """
        Methode qui génére et renvoie le pokémon ennemi en fonction de la difficulté.
        Si aucun pokémon ne peut apparaitre, la méthode renvoie None.

        @in : diff, str → difficulté du combat
        """

        if self.training_pk is None:
            return None
        else:
            ennemy_pk_lv = self.get_ennemy_pk_level(diff)
            ennemy_pk_name = self.get_ennemy_pk_name(diff, ennemy_pk_lv)

            return pokemon.Pokemon(ennemy_pk_name, ennemy_pk_lv, self.game)
    
    def set_difficult(self, diff='easy'):
        """
        Méthode de modification de la difficulté.

        @in : diff, str → la nouvelle difficulté sélectionnée
        """
        self.difficult = diff
        
        self.ennemy_pk = self.ennemy_pks[self.difficult]
        self.load_ennemy_pk()
        
    def set_ennemy_pks(self):
        """
        Methode d'actualisation des pokémons ennemis en fonction du pokémon à entrainer du joueur.
        """
        if self.training_pk is not None:
            if self.training_pk.get_id() in self.ennemy_pks_backup.keys():
                self.ennemy_pks = self.ennemy_pks_backup[self.training_pk.get_id()]
                self.ennemy_pk = self.ennemy_pks[self.difficult]
            else:
                self.ennemy_pks = {
                    'easy': self.spawn_ennemy_pk('easy'),
                    'normal': self.spawn_ennemy_pk('normal'),
                    'hard': self.spawn_ennemy_pk('hard')
                }
                self.ennemy_pk = self.ennemy_pks[self.difficult]
                self.ennemy_pks_backup[self.training_pk.get_id()] = self.ennemy_pks
        
    def load_ennemy_pk(self):
        """
        Methode qui charge les images liées au pokémon ennemi pour limiter les chargements répétés
        """
        
        if self.ennemy_pk is not None:
            self.ennemy_pk_icon = pygame.transform.scale(self.ennemy_pk.get_icon(), (300, 150))
            self.ennemy_pk_name = self.ennemy_pk_name_font.render(f"{self.ennemy_pk.get_name()}  Lv.{self.ennemy_pk.get_level()}", False, (0, 0, 0))
            self.ennemy_pk_type1 = self.ennemy_pk_type_font.render(
                game_infos.type_names_to_print[self.ennemy_pk.get_type()],
                False,
                game_infos.get_type_color(self.ennemy_pk.get_type()))
            
            if self.ennemy_pk.get_type2() != 'NoType':
                self.ennemy_pk_type2 = self.ennemy_pk_type_font.render(
                    game_infos.type_names_to_print[self.ennemy_pk.get_type2()],
                    False,
                    game_infos.get_type_color(self.ennemy_pk.get_type2()))
            else:
                self.ennemy_pk_type2 = None
                
            self.ennemy_pk_pv = self.ennemy_pk_stats_font.render(str(self.ennemy_pk.get_stats()[0]), False, (2, 137, 0))
            self.ennemy_pk_atk = self.ennemy_pk_stats_font.render(str(self.ennemy_pk.get_stats()[1]), False, (189, 0, 0))
            self.ennemy_pk_def = self.ennemy_pk_stats_font.render(str(self.ennemy_pk.get_stats()[2]), False, (191, 200, 0))
            self.ennemy_pk_vit = self.ennemy_pk_stats_font.render(str(self.ennemy_pk.get_stats()[3]), False, (0, 139, 230))
            
    def get_ennemy_pk_name(self, diff, ennemy_pk_lv: int) -> str or None:
        """
        Methode qui détermine le nom du pokémon ennemi en fonction de la difficulté
        """
        
        if self.training_pk is None:
            return None
        
        r = random.Random()
        r.seed(self.training_pk.random_seed + self.game.general_seed)
        
        spawnable_pks = game_infos.get_all_diff_pokemons(self.game, self.training_pk, ennemy_pk_lv, diff)
        ennemy_pk_name = r.choice(spawnable_pks)
        
        return ennemy_pk_name
    
    def get_ennemy_pk_level(self, diff) -> int:
        """
        Methode qui determine le level du pokémon ennemi à affronter selon la difficulté choisie.

        @in : diff, str → difficulté du combat.
        """

        #
        if diff == 'easy':
            n = 1
        elif diff == 'normal':
            n = 2
        else:
            n = 3

        r = random.Random()
        r.seed(self.training_pk.random_seed + n)

        # Calcul du niveau minimum
        min_lv = round(self.game.player.get_level() / 2
                       + self.LV_DIFFICULT_COEFS[diff][0] * self.training_pk.get_level())

        # Calcul du niveau maximum
        max_lv = round(self.game.player.get_level() / 2
                       + self.LV_DIFFICULT_COEFS[diff][1] * self.training_pk.get_level())

        if min_lv > 100:
            min_lv = 99
        if max_lv > 100:
            max_lv = 99

        ennemy_pk_lv = r.randint(min_lv, max_lv)
        return ennemy_pk_lv

    def add_pk_to_team(self, team_i):
        """
        Méthode permettant d'ajouter un pokémon à l'équipe du joueur.

        @in : team_i, int → indice du pokémon dans l'équipe
        """
        if self.game.player.team[team_i] is None:
            self.game.player.team[team_i] = self.training_pk
            self.training_pk = None

    def img_load(self, file_name):
        return pygame.image.load(f'{self.PATH}{file_name}.png')

    def create_rect_alpha(self, dimensions, color, opacite=90):
        rect = pygame.Surface(dimensions)
        rect.set_alpha(opacite)
        rect.fill(color)
        return rect

    # Méthodes basiques

    def reset(self):
        """
        Méthode de réinitialisation du panel.
        Utilisée lors de l'initialisation d'un nouveau tour de jeu.
        """
        self.training_pk = None
        self.ennemy_pks_backup = {}

        self.difficult = 'easy'
        self.boolEnnemy_pk_stats = False

        # Variables relatives aux pokémons ennemis
        self.ennemy_pks = {
            'easy': self.spawn_ennemy_pk('easy'),
            'normal': self.spawn_ennemy_pk('normal'),
            'hard': self.spawn_ennemy_pk('hard')
        }
        self.ennemy_pk = self.ennemy_pks[self.difficult]

        self.ennemy_pks_backup = {}

        self.load_ennemy_pk()

        self.boolSettings_popup = False
        self.boolAdd_training_pk_popup = False

    def close(self):
        """
        Méthode classique qui éxécute tout ce qu'il faut faire lorsque le panel est fermé.
        """
        if self.training_pk is not None:
            if self.game.player.get_nb_team_members() < 6:
                self.game.player.add_team_pk(self.training_pk)
                self.training_pk = None

    # Méthodes de gestion d'intérations
        
    def left_clic_interactions(self, possouris):
        """
        Méthode gérant les intéractions de l'utilisateur avec le clic gauche de la souris.

        @in : possouris, list → coordonnées du pointeur de souris
        """
        if self.boolSettings_popup:
            if self.easy_button_rect.collidepoint(possouris):
                self.set_difficult('easy')
                self.close_settings_popup()
            elif self.normal_button_rect.collidepoint(possouris):
                self.set_difficult('normal')
                self.close_settings_popup()
            elif self.hard_button_rect.collidepoint(possouris):
                self.set_difficult('hard')
                self.close_settings_popup()

        if self.settings_button_rect.collidepoint(possouris):
            if self.boolSettings_popup:
                self.close_settings_popup()
            else:
                self.open_settings_popup()

        if self.training_pk is not None:
            if self.ennemy_pk_infos_stats_button_rect.collidepoint(possouris):
                self.boolEnnemy_pk_stats = not self.boolEnnemy_pk_stats
            elif self.fight_button_rect.collidepoint(possouris):
                if self.ennemy_pk.is_alive:
                    if self.training_pk.is_alive:
                        if self.game.player.actions > 0:
                            self.start_fight()
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        else:
                            self.game.notif('Action nécessaire', (255, 0, 0))
                    else:
                        self.game.notif('Votre pokémon doit être vivant !', (255, 0, 0))
                else:
                    self.game.notif('Vous avez déjà battu ce pokémon !', (255, 0, 0))

    def right_clic_interactions(self, posssouris):
        """
        Méthode gérant les intéractions de l'utilisateur avec le clic droit de la souris.

        @in : possouris, list → coordonnées du pointeur de souris
        """
        if self.training_pk_rect.collidepoint(posssouris):
            self.game.classic_panel.pokemon_info_mode = True
            self.game.classic_panel.pokemon_info = self.training_pk

    def is_hovering_settings_popup_buttons(self, possouris):
        """
        Méthode qui retourne True si la souris est positionnée sur un bouton du popup "settings".

        @in : possouris, list → coordonnées du pointeur de souris
        @out : bool
        """
        if self.boolSettings_popup:
            return (self.easy_button_rect.collidepoint(possouris) or self.normal_button_rect.collidepoint(possouris) or
                    self.hard_button_rect.collidepoint(possouris))
        else:
            return False

    def is_hovering_buttons(self, possouris):
        """
        Méthode qui retourne True si la souris est positionnée sur un bouton du panel.

        @in : possouris, list → coordonnées du pointeur de souris
        @out : bool
        """
        return (self.settings_button_rect.collidepoint(possouris)
                or self.is_hovering_settings_popup_buttons(possouris)
                or (self.training_pk_rect.collidepoint(possouris) and self.training_pk is not None)
                or (self.ennemy_pk_infos_stats_button_rect.collidepoint(possouris) and self.training_pk is not None)
                or (self.fight_button_rect.collidepoint(possouris) and self.training_pk is not None)
                or self.pk_move_mode
                or self.training_pk_rect.collidepoint(possouris)
                )
