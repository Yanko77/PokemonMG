import random

import pygame

import game_infos
import pokemon


class TrainPanel:

    def __init__(self, game):
        self.game = game

        # FONTS
        self.info_select_pk_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 22)
        self.ennemy_pk_name_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 22)
        self.ennemy_pk_type_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 17)
        self.ennemy_pk_stats_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 20)

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
        self.background_pos = (-13, -21)

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

        self.add_button = self.img_load('add_button')  # Bouton ADD (+)
        self.add_button_h = self.img_load('add_button_hover')
        self.add_button_rect = pygame.Rect(127, 144, 215, 215)

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
        self.training_pk_rect = pygame.Rect(111, 123, 252, 252)

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

        # Variables relatives aux popups
        self.boolSettings_popup = False
        self.boolAdd_training_pk_popup = False

        self.stats_popup = self.img_load('ennemy_pk_stats')
        self.stats_popup_pos = (612, 352)

        # Variables de la fenetre ingame
        self.window_pos = [0, 0]

    def update(self, surface, possouris, window_pos):
        # Actualiser les variables relatives à la position de la fenetre ingame
        if self.window_pos != window_pos:
            self.update_all_rects(window_pos)

        # Affichage du background
        surface.blit(self.background, self.background_pos)

        # Affichage de l'emplacement du pokemon à entrainer
        self.update_training_pk_emp(surface, possouris)

        # Gestion des affichages relatifs au pokémon à entrainer
        if self.training_pk is not None:

            # Afficher la preview du pokemon ennemi
            self.update_ennemy_preview(surface, possouris)

            # Afficher le bouton FIGHT
            if self.fight_button_rect.collidepoint(possouris):
                surface.blit(self.fight_button, self.fight_button_rect)
            else:
                surface.blit(self.fight_button_h, self.fight_button_rect)

        # Affichage du popup SETTINGS
        if self.boolSettings_popup:
            self.update_settings_popup(surface, possouris)

    def update_training_pk_emp(self, surface, possouris):
        """
        Methode qui gère l'affichage de l'emplacement du pokémon à entrainer du joueur
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
                                                 (255, 255, 255)),
                         self.training_pk_rect)

        # Affichages des boutons relatifs au pokémon à entrainer
        if self.training_pk is None:

            # Affichage de l'emplacement bloqué
            surface.blit(self.locked, self.locked_pos)

        else:

            # Affichage du texte NO SELECTED PK
            surface.blit(self.no_pk_selected_text, self.no_pk_selected_text_pos)

            # Affichages des boutons relatifs au popup ADD_TRAINING_PK
            if self.boolAdd_training_pk_popup:

                # Affichage du bouton +
                if self.add_button_rect.collidepoint(possouris):
                    surface.blit(self.add_button_h, self.add_button_rect)
                else:
                    surface.blit(self.add_button, self.add_button_rect)
            else:

                # Affichage du pokémon à entrainer
                surface.blit(pygame.transform.scale(self.training_pk.icon_image, (504, 252)),
                             (self.training_pk_rect.x, self.training_pk_rect.y - 25),
                             (0, 0, 252, 252))

    def update_ennemy_preview(self, surface, possouris):
        """
        Methode qui gère l'affichage de la preview du pokemon ennemi
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
        if self.boolEnnemy_pk_stats:

            # Affichage du type1 du pokémon ennemi
            surface.blit(self.ennemy_pk_type1, self.ennemy_pk_type1_pos)

            # Affichage du type 2 du pokémon ennemi, s'il en a un
            if ennemy_pk_type2 is not None:
                surface.blit(self.ennemy_pk_type2, self.ennemy_pk_type2_pos)

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
        Methode qui gère l'affichage du popup SETTINGS
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

    def update_all_rects(self, window_pos):
        self.window_pos = window_pos.copy()

        self.background_pos = (-13 + self.window_pos[0], -21 + self.window_pos[1])
        self.training_pk_emp_pos = (78 + self.window_pos[0], 96 + self.window_pos[1])
        self.locked_pos = (70 + self.window_pos[0], 80 + self.window_pos[1])
        self.diff_ind_pos = (80 + self.window_pos[0], 177 + self.window_pos[1])
        self.ennemy_pk_popup_pos = (446 + self.window_pos[0], 39 + self.window_pos[1])
        self.fight_button_rect = pygame.Rect(613 + self.window_pos[0], 448 + self.window_pos[1], 266, 73)
        self.settings_button_rect = pygame.Rect(22 + self.window_pos[0], 90 + self.window_pos[1], 90, 120)
        self.add_button_rect = pygame.Rect(127 + self.window_pos[0], 144 + self.window_pos[1], 215, 215)
        self.ennemy_pk_infos_stats_button_rect = pygame.Rect(715 + self.window_pos[0], 408 + self.window_pos[1], 105, 31)
        self.settings_popup_pos = (59 + self.window_pos[0], 59 + self.window_pos[1])
        self.easy_button_rect = pygame.Rect(92 + self.window_pos[0], 68 + self.window_pos[1], 74, 44 + self.window_pos[1])
        self.normal_button_rect = pygame.Rect(171 + self.window_pos[0], 68 + self.window_pos[1], 74, 44)
        self.hard_button_rect = pygame.Rect(249 + self.window_pos[0], 68 + self.window_pos[1], 74, 44)
        self.no_pk_selected_text_pos = (90 + self.window_pos[0], 65 + self.window_pos[1])
        self.training_pk_rect = pygame.Rect(111 + self.window_pos[0], 123 + self.window_pos[1], 252, 252)
        self.ennemy_pk_icon_pos = (455 + self.window_pos[0], 273 + self.window_pos[1])
        self.ennemy_pk_name_pos = (617 + self.window_pos[0], 317 + self.window_pos[1])
        self.ennemy_pk_type1_pos = (670 + self.window_pos[0], 346 + self.window_pos[1])
        self.ennemy_pk_type2_pos = (675 + self.window_pos[0], 346 + self.window_pos[1])
        self.ennemy_pk_pv_pos = (653 + self.window_pos[0], 348 + self.window_pos[1])
        self.ennemy_pk_atk_pos = (653 + self.window_pos[0], 373 + self.window_pos[1])
        self.ennemy_pk_def_pos = (749 + self.window_pos[0], 348 + self.window_pos[1])
        self.ennemy_pk_vit_pos = (749 + self.window_pos[0], 373 + self.window_pos[1])
        self.stats_popup_pos = (612 + self.window_pos[0], 352 + self.window_pos[1])

    def start_fight(self):
        self.game.start_fight(self.training_pk, dresseur.Sauvage, self.ennemy_pks[self.difficult],
                              self.difficult)
    
    def set_difficult(self, diff='easy'):
        self.difficult = diff
        
        self.ennemy_pk = self.ennemy_pks[self.difficult]
        self.load_ennemy_pk()
        
    def set_ennemy_pks(self):
        """
        Methode d'actualisation des pokémons ennemis en fonction du pokémon à entrainer du joueur
        """
        self.ennemy_pks = {
            'easy': self.spawn_ennemy_pk('easy'),
            'normal': self.spawn_ennemy_pk('normal'),
            'hard': self.spawn_ennemy_pk('hard')
        }
        self.ennemy_pk = self.ennemy_pks[self.difficult]
        
    def load_ennemy_pk(self):
        """
        Methode qui charge les images liées au pokémon ennemi pour limiter les chargements répétés
        """
        
        if self.ennemy_pk is not None:
            self.ennemy_pk_icon = pygame.transform.scale(self.ennemy_pk.get_icon(), (300, 150))
            self.ennemy_pk_name = self.ennemy_pk_name_font.render(f"{self.ennemy_pk.get_name()}  Lv.{pk.get_level()}", False, (0, 0, 0))
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
                
            self.ennemy_pk_pv = self.ennemy_pk_stats_font.render(str(self.ennemy_pk.get_stats[0]), False, (2, 137, 0))
            self.ennemy_pk_atk = self.ennemy_pk_stats_font.render(str(self.ennemy_pk.get_stats[1]), False, (189, 0, 0))
            self.ennemy_pk_def = self.ennemy_pk_stats_font.render(str(self.ennemy_pk.get_stats[2]), False, (191, 200, 0))
            self.ennemy_pk_vit = self.ennemy_pk_stats_font.render(str(self.ennemy_pk.get_stats[3]), False, (0, 139, 230))
            
    def get_ennemy_pk_name(self, diff) -> str or None:
        """
        Methode qui détermine le nom du pokémon ennemi en fonction de la difficulté
        """
        
        if self.training_pk is None:
            return None
        
        r = random.Random()
        r.seed(self.training_pk.random_seed + self.game.general_seed)
        
        spawnable_pks = game_infos.get_all_diff_pokemons(self.training_pk.get_type(), diff)
        ennemy_pk_name = r.choice(spawnable_pks)
        
        return ennemy_pk_name
    
    def get_ennemy_pk_level(self, diff) -> int:
        """
        Methode qui determine le level du pokémon ennemi à affronter selon la difficulté choisie
        """

        # Calcul du niveau minimum
        min_lv = round(self.game.player.get_level() / 2
                       + self.LV_DIFFICULT_COEFS[diff][0] * self.game.player.get_moyenne_team())

        # Calcul du niveau maximum
        max_lv = round(self.game.player.get_level() / 2
                       + self.LV_DIFFICULT_COEFS[diff][1] * self.game.player.get_moyenne_team())

        ennemy_pk_lv = random.randint(min_lv, max_lv)
        return ennemy_pk_lv
    
    def spawn_ennemy_pk(self, diff) -> pokemon.Pokemon or None:
        """
        Methode qui génére et renvoie le pokémon ennemi en fonction de la difficulté
        """
        ennemy_pk_name = self.get_ennemy_pk_name(diff)
        if ennemy_pk_name is None:
            return None
        else:
            return pokemon.Pokemon(ennemy_pk_name, self.get_ennemy_pk_level(diff), self.game.player)
        
    def open_settings_popup(self):
        self.boolSettings_popup = True
        
    def close_settings_popup(self):
        self.boolSettings_popup = False
        
    def left_clic_interactions(self, possouris):
        if self.settings_button_rect.collidepoint(possouris):
            if self.boolSettings_popup:
                self.close_settings_popup()
            else:
                self.open_settings_popup()

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

        if self.training_pk is not None:
            if self.training_pk_rect.collidepoint(possouris):
                self.training_pk = None
            elif self.ennemy_pk_infos_stats_button_rect.collidepoint(possouris):
                self.boolEnnemy_pk_stats = not boolEnnemy_pk_stats
            elif self.fight_button_rect.collidepoint(possouris):
                self.start_training_fight()
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def is_hovering_settings_popup_buttons(self, possouris):
        if self.boolSettings_popup:
            return (self.easy_button_rect.collidepoint(possouris) or self.normal_button_rect.collidepoint(possouris) or
                    self.hard_button_rect.collidepoint(possouris))
        else:
            return False

    def is_hovering_buttons(self, possouris):
        return (self.settings_button_rect.collidepoint(possouris)
                or self.is_hovering_settings_popup_buttons(possouris)
                or (self.add_button_rect.collidepoint(
                    possouris) and self.training_pk is None and not self.boolAdd_training_pk_popup)
                or (self.training_pk_rect.collidepoint(possouris) and self.training_pk is not None)
                or (self.ennemy_pk_infos_stats_button_rect.collidepoint(possouris) and self.training_pk is not None)
                or (self.fight_button_rect.collidepoint(possouris) and self.training_pk is not None)
                )
        
    def img_load(self, file_name):
        return pygame.image.load(f'{self.PATH}{file_name}.png')

    def create_rect_alpha(self, dimensions, color, opacite=90):
        rect = pygame.Surface(dimensions)
        rect.set_alpha(opacite)
        rect.fill(color)
        return rect
