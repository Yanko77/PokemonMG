"""
Fichier gérant le système de combat.
"""

# Importation des modules

import pygame
import random

import dresseur
import game_infos
import objet
import pokemon
from dresseur import Alizee, Olea, Ondine, Pierre, Blue, Red, Iris, Sauvage
import attaques

# Déclaration des constantes

DRESSEUR_LIST = [Alizee, Olea, Ondine, Pierre, Blue, Red]

# Définition des classes


class Fight:
    """
    Classe représentant un combat entre le pokémon du joueur, et un dresseur (PNJ)
    
    Classe définie par:
    - La game, game.Game
    - Le pokémon du joueur, pokemon.Pokemon
    - Le dresseur
    - La difficulté du combat, str
    - Le type de combat, str ('Classic' ou 'Boss')
    """

    def __init__(self, game, player_pk, dresseur=None, difficult='easy', fight_type='Classic'):
        self.game = game
        self.player_pk = player_pk
        self.dresseur = self.init_dresseur(dresseur)
        self.fight_type = fight_type

        # Chargement des images
        self.path = 'assets/game/panels/fight_panel/'

        self.background = self.img_load('background')

        self.combat_button = self.img_load('combat_button')
        self.combat_button_rect = pygame.Rect(873, 526, 387, 174)

        self.sac_button = self.img_load('sac_button')
        self.sac_button_rect = pygame.Rect(717, 527, 144, 144)

        self.fuite_button = self.img_load('fuite_button')
        self.fuite_button_rect = pygame.Rect(1188, 446, 72, 74)

        self.pk_info_bar = self.img_load('pk_info_bar')
        self.player_pk_info_bar_rect = (22, 561, 434, 144)
        self.dresseur_pk_info_bar_rect = (891, 22, 369, 122)

        self.cover_attaque_button = self.img_load('attaque_button')
        self.cover_attaque_button_hover = self.img_load('attaque_button_hover')

        self.sac_action_background = self.img_load('sac_action_bg')
        self.sac_action_background_rect = pygame.Rect(673, 360, 587, 335)

        self.sac_action_curseur = self.img_load('sac_action_curseur')
        self.sac_action_curseur_rect = pygame.Rect(673, 432, 27, 72)
        self.sac_action_curseur_rects = [pygame.Rect(673, 432, 27, 88),
                                         pygame.Rect(673, 520, 27, 88),
                                         pygame.Rect(673, 608, 27, 88)]
        self.sac_action_curseur_pos = 0
        self.curseur_moving_mode = False
        self.objet_icon_rects = [
            pygame.Rect(718, 432, 122, 122),
            pygame.Rect(858, 432, 122, 122),
            pygame.Rect(998, 432, 122, 122),
            pygame.Rect(1138, 432, 122, 122),
            pygame.Rect(718, 572, 122, 122),
            pygame.Rect(858, 572, 122, 122),
            pygame.Rect(998, 572, 122, 122),
            pygame.Rect(1138, 572, 122, 122),
            pygame.Rect(718, 432, 122, 122),
            pygame.Rect(858, 432, 122, 122),
            pygame.Rect(998, 432, 122, 122),
            pygame.Rect(1138, 432, 122, 122),
            pygame.Rect(718, 572, 122, 122),
            pygame.Rect(858, 572, 122, 122),
            pygame.Rect(998, 572, 122, 122),
            pygame.Rect(1138, 572, 122, 122),
            pygame.Rect(718, 432, 122, 122),
            pygame.Rect(858, 432, 122, 122),
            pygame.Rect(998, 432, 122, 122),
            pygame.Rect(1138, 432, 122, 122),
            pygame.Rect(718, 572, 122, 122),
            pygame.Rect(858, 572, 122, 122),
            pygame.Rect(998, 572, 122, 122),
            pygame.Rect(1138, 572, 122, 122),
        ]
        self.item_moving_mode = False
        self.item_moving_i = None
        self.current_moving_item_rel_possouris = (0, 0)

        self.sac_item_hover = self.img_load('sac_item_hover')
        self.use_item_rect = pygame.Rect(12, 560, 454, 155)

        # End fight images
        self.end_fight_panel = self.img_load('end_fight_panel/panel').convert_alpha()

        self.fin_du_combat_button = self.img_load('end_fight_panel/fin_du_combat_button')
        self.fin_du_combat_button_rect = pygame.Rect(825, 588, 424, 101)

        self.stats_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 60)

        self.lv = self.img_load('end_fight_panel/lv').convert_alpha()
        self.lv_rect = pygame.Rect(576, 228, 0, 0)

        self.pv = self.img_load('end_fight_panel/pv').convert_alpha()
        self.pv_rect = pygame.Rect(576, 339, 0, 0)

        self.atk = self.img_load('end_fight_panel/atk').convert_alpha()
        self.atk_rect = pygame.Rect(576, 406, 0, 0)

        self.defense = self.img_load('end_fight_panel/def').convert_alpha()
        self.defense_rect = pygame.Rect(576, 476, 0, 0)

        self.vit = self.img_load('end_fight_panel/vit').convert_alpha()
        self.vit_rect = pygame.Rect(576, 546, 0, 0)

        self.pk_icon = pygame.transform.scale(self.player_pk.icon_image, (960, 480)).convert_alpha()

        # Chargement des fonts
        self.player_pk_name_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 40)
        self.dresseur_pk_name_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 30)
        self.pk_pv_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 25)
        self.dresseur_pk_pv_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 20)
        self.attaque_font = pygame.font.Font('assets/fonts/Cheesecake.ttf', 55)
        self.sac_page_font = pygame.font.Font('assets/fonts/Cheesecake.ttf', 65)
        self.item_quantite_font = pygame.font.Font('assets/fonts/Impact.ttf', 30)
        self.fight_logs_font = pygame.font.Font('assets/fonts/Cheesecake.ttf', 40)
        self.turn_exec_info_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 25)

        # Pré-chargement des noms des pokemons
        self.player_pk_name = self.player_pk_name_font.render(self.player_pk.name, False, (40, 40, 40))
        self.dresseur_pk_name = self.dresseur_pk_name_font.render(self.dresseur.pk.name,
                                                                  False, (40, 40, 40))

        # Variables relatives aux boutons
        self.current_action = None
        self.attaque_buttons_rects = [
            pygame.Rect(907, 432, 356, 109),
            pygame.Rect(535, 471, 356, 109),
            pygame.Rect(907, 560, 356, 109),
            pygame.Rect(535, 596, 356, 109)
        ]
        self.current_action_rect = pygame.Rect(477, 356, 803, 365)

        # Variables relatives aux status
        self.sommeil_compteur_tour = {self.player_pk: -1,
                                      self.dresseur.pk: -1}
        self.confusion_compteur_tour = {self.player_pk: -1,
                                        self.dresseur.pk: -1}

        # Variables relatives aux actions du tour
        self.current_turn_action = ('NoAction', None)  # ('ITEM', item) ou ('ATTAQUE', attaque)
        self.dresseur_pk_action = None
        self.executing_turn = False
        self.current_turn_order = None
        self.turn_exec_info = ''

        self.reward_quantity = 2
        self.difficult = difficult

        self.fight_logs = []
        self.fight_result = None

        self.compteur = 0
        self.compteur_action_file = []

        self.boolEnding = False
        self.is_animating_end_panel = False
        self.compteur_end = 0

        # Sauvegardes des hp des pokémons utilisés pour l'animation de dégats
        self.saved_player_pk_pv = self.player_pk.health
        self.saved_dresseur_pk_pv = self.dresseur.pk.health

    def update(self, surface, possouris):
        """
        Methode d'actualisation de l'affichage du combat.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """

        if not self.boolEnding:

            # Background du combat
            surface.blit(self.background, (0, 0))

            # Pokemons
            self.update_pokemons(surface)

            # Boutons du combat
            self.update_fight_buttons(surface, possouris)

            # Action en cours
            self.update_current_action(possouris)

            # Logs
            self.update_fight_logs(surface)

            # Execution du tour
            if self.executing_turn:
                self.update_turn_exec_info(surface)
                self.turn(self.current_turn_action)
        else:
            # Ecran de fin de combat
            self.update_end_panel(surface)

        # GESTION CURSEUR INTERACTIONS
        if self.is_hovering(possouris):
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def init_dresseur(self, dresseur=None):
        """
        Methode d'initialisation du dresseur.
        Retourne la classe d'objet du dresseur.
        """

        if dresseur is None:
            r = random.Random()
            r.seed(self.game.round.random_seed)
            dresseur = r.choice(DRESSEUR_LIST)

        return dresseur

    def update_end_panel(self, surface):
        """
        Methode d'actualisation de l'affichage du panel de fin de combat.

        @in : surface, pygame.Surface → fenêtre du jeu
        """

        if self.compteur_end < 200:
            self.is_animating_end_panel = True
        else:
            self.is_animating_end_panel = False

        if self.is_animating_end_panel:
            # Background
            pos_compteur = 720 - self.compteur_end*4
            if pos_compteur < 0:
                pos_compteur = 0
            bg_pos = (0, pos_compteur)

            surface.blit(self.end_fight_panel, bg_pos)

            self.compteur_end += 1
        else:
            pass
            # surface.blit(self.end_fight_panel, (0, 0))

    def update_current_action(self, possouris):
        """
        Methode permettant de modifier l'action en cours du joueur.

        @in : possouris, list → coordonnées du pointeur de souris
        """
        if self.current_action is not None:
            if not self.item_moving_mode:
                if not self.current_action_rect.collidepoint(possouris):
                    self.current_action = None

    def update_turn_exec_info(self, surface):
        """
        Methode d'actualisation de l'affichage des infos d'execution du tour du combat.

        @in : surface, pygame.Surface → fenêtre du jeu
        """
        surface.blit(self.turn_exec_info_font.render(self.turn_exec_info, False, (255, 255, 255)), (502, 9))

    def update_fight_buttons(self, surface, possouris):
        """
        Methode d'actualisation de l'affichage des boutons du combat.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """
        if self.fight_result is None:

            # Si aucun bouton n'a été cliqué
            if self.current_action is None:
                if self.combat_button_rect.collidepoint(possouris):
                    surface.blit(self.combat_button, self.combat_button_rect, (388, 0, 387, 174))
                else:
                    surface.blit(self.combat_button, self.combat_button_rect, (0, 0, 387, 174))

                if self.sac_button_rect.collidepoint(possouris):
                    surface.blit(self.sac_button, self.sac_button_rect, (145, 0, 144, 144))
                else:
                    surface.blit(self.sac_button, self.sac_button_rect, (0, 0, 144, 144))

                if self.fuite_button_rect.collidepoint(possouris):
                    surface.blit(self.fuite_button, self.fuite_button_rect, (73, 0, 72, 74))
                else:
                    surface.blit(self.fuite_button, self.fuite_button_rect, (0, 0, 72, 74))

            # Si l'action en cours est 'COMBAT'
            elif self.current_action == 'COMBAT':
                for i in range(4):  # Chaque bouton d'attaque
                    if self.player_pk.attaque_pool[i] is not None:
                        button_rect = self.attaque_buttons_rects[i]
                        pygame.draw.rect(surface, game_infos.type_colors[self.player_pk.attaque_pool[i].type],
                                         button_rect,
                                         border_radius=15)

                        if button_rect.collidepoint(possouris):
                            surface.blit(self.cover_attaque_button, button_rect)
                            surface.blit(self.cover_attaque_button_hover, button_rect)

                            attaque_name_shadow = self.attaque_font.render(self.player_pk.attaque_pool[i].name_, False,
                                                                           (30, 30, 30))
                            surface.blit(attaque_name_shadow,
                                         (button_rect.x + 1 + (356 - attaque_name_shadow.get_width()) / 2,
                                          button_rect.y + 3 + (
                                                  109 - attaque_name_shadow.get_height()) / 2))

                            attaque_name = self.attaque_font.render(self.player_pk.attaque_pool[i].name_, False,
                                                                    (255, 255, 255))
                            surface.blit(attaque_name, (button_rect.x + (356 - attaque_name.get_width()) / 2,
                                                        button_rect.y + (109 - attaque_name.get_height()) / 2))

                        else:
                            surface.blit(self.cover_attaque_button, button_rect)

                            attaque_name = self.attaque_font.render(self.player_pk.attaque_pool[i].name_, False,
                                                                    (240, 240, 240))
                            surface.blit(attaque_name, (button_rect.x + (356 - attaque_name.get_width()) / 2,
                                                        button_rect.y + (109 - attaque_name.get_height()) / 2))

            # Si l'action en cours est 'SAC'
            elif self.current_action == 'SAC':
                surface.blit(self.sac_action_background, self.sac_action_background_rect)

                self.sac_curseur_update(possouris)

                surface.blit(self.sac_page_font.render(str(self.sac_action_curseur_pos + 1), False, (150, 150, 150)),
                             (1218, 359))
                surface.blit(self.sac_page_font.render(str(self.sac_action_curseur_pos + 1), False, (255, 255, 255)),
                             (1218, 357))

                if self.sac_action_curseur_rect.collidepoint(possouris) or self.curseur_moving_mode:
                    img_rect = (23, 0, 23, 66)
                else:
                    img_rect = (0, 0, 23, 66)

                surface.blit(self.sac_action_curseur,
                             (self.sac_action_curseur_rect.x + 2,
                              self.sac_action_curseur_rect.y + 5 * (self.sac_action_curseur_pos + 1)),  # Co du curseur
                             img_rect)

                user_usable_items = []

                for item in self.game.player.sac:
                    if item is not None:
                        if item.fonctionnement.split(":")[0] == 'Use':
                            user_usable_items.append(item)

                for i in range(24 - len(user_usable_items)):
                    user_usable_items.append(None)

                if self.sac_action_curseur_pos == 0:
                    i = 0
                    for objet in user_usable_items[0:8]:
                        self.sac_item_update(surface, possouris, objet, i)
                        i += 1
                elif self.sac_action_curseur_pos == 1:
                    i = 8
                    for objet in user_usable_items[8:16]:
                        self.sac_item_update(surface, possouris, objet, i)
                        i += 1
                else:
                    i = 16
                    for objet in user_usable_items[16:]:
                        self.sac_item_update(surface, possouris, objet, i)
                        i += 1

        else:
            if self.fin_du_combat_button_rect.collidepoint(possouris):
                surface.blit(self.fin_du_combat_button, self.fin_du_combat_button_rect, (425, 0, 425, 101))
            else:
                surface.blit(self.fin_du_combat_button, self.fin_du_combat_button_rect, (0, 0, 424, 101))

    def update_pokemons(self, surface):
        """
        Methode d'actualisation de l'affichage des pokémons (Celui du joueur et celui du dresseur).

        @in : surface, pygame.Surface → fenêtre du jeu
        """
        # Pokemon du joueur
        # Icone
        surface.blit(pygame.transform.scale(self.player_pk.icon_image, (700, 350)), (180, 270), (0, 0, 350, 350))
        # Barre d'info
        surface.blit(self.pk_info_bar, self.player_pk_info_bar_rect, (0, 0, 434, 144))
        # Affichage de l'animation des dégats subis
        self.animate_player_pk_damage(surface)
        # Barre de vie verte
        pygame.draw.rect(surface, (42, 214, 0),
                         pygame.Rect(31, 646, self.player_pk.health / self.player_pk.pv * 263, 24))
        # PV
        pv_text = self.pk_pv_font.render(str(self.player_pk.health) + "/" + str(self.player_pk.pv),
                                   False, (40, 40, 40))
        surface.blit(pv_text, (39, 669))
        # Status
        all_status_on = []
        for status in self.player_pk.status.keys():
            if self.player_pk.status[status]:
                all_status_on.append(status.upper())

        # "POISON BRULÉ SOMMEIL GEL PARALYSÉ CONFUS"
        status_text_list = []
        for status in all_status_on:
            color = game_infos.status_color[status]
            status_text_list.append(self.pk_pv_font.render(status, False, color))

        x = 0
        for status_text in status_text_list:
            surface.blit(status_text, (39 + pv_text.get_width() + 7 + x, 669))
            x += status_text.get_width() + 7

        # Nom
        surface.blit(self.player_pk_name, (40, 584))
        # Level
        surface.blit(self.player_pk_name_font.render(f" Lv.{self.player_pk.level}", False, (0, 0, 0)),
                     (40 + self.player_pk_name.get_width(), 584))

        # Pokemon du dresseur
        # Icone
        surface.blit(pygame.transform.scale(self.dresseur.pk.icon_image, (600, 300)), (770, 80), (0, 0, 300, 300))
        # Barre d'info
        surface.blit(self.pk_info_bar, self.dresseur_pk_info_bar_rect, (434, 0, 369, 123))
        # Affichage de l'animation des dégats subis
        self.animate_dresseur_pk_damage(surface)
        # Barre de vie verte
        pygame.draw.rect(surface, (42, 214, 0),
                         pygame.Rect(899, 94, self.dresseur.pk.health / self.dresseur.pk.pv * 225, 21))
        # Nom
        surface.blit(self.dresseur_pk_name, (905, 51))
        # Level
        surface.blit(self.dresseur_pk_name_font.render(f"  Lv.{self.dresseur.pk.level}", False, (0, 0, 0)),
                     (905 + self.dresseur_pk_name.get_width(), 51))

        # Status
        all_status_on = []
        for status in self.dresseur.pk.status.keys():
            if self.dresseur.pk.status[status]:
                all_status_on.append(status.upper())

        # "POISON BRULÉ SOMMEIL GEL PARALYSÉ CONFUS"
        status_text_list = []
        for status in all_status_on:
            color = game_infos.status_color[status]
            status_text_list.append(self.dresseur_pk_pv_font.render(status, False, color))

        x = 0
        for status_text in status_text_list:
            surface.blit(status_text, (906 + x, 115))
            x += status_text.get_width() + 7

    def animate_player_pk_damage(self, surface):
        """
        Methode d'actualisation de l'affichage de l'animation de la barre rouge de dégats subis par le pokémon du joueur.

        @in : surface, pygame.Surface → fenêtre du jeu
        """
        if self.player_pk.health < self.saved_player_pk_pv:

            # Barre de vie rouge
            pygame.draw.rect(surface, (255, 0, 0),
                            pygame.Rect(31, 646, self.saved_player_pk_pv / self.player_pk.pv * 263, 24))

            self.saved_player_pk_pv -= self.player_pk.pv / 75

        else:
            self.saved_player_pk_pv = self.player_pk.health

    def animate_dresseur_pk_damage(self, surface):
        """
        Methode d'actualisation de l'affichage de l'animation de la barre rouge de dégats subis par le pokémon du dresseur.

        @in : surface, pygame.Surface → fenêtre du jeu
        """
        if self.dresseur.pk.health < self.saved_dresseur_pk_pv:

            # Barre de vie rouge
            pygame.draw.rect(surface, (255, 0, 0),
                             pygame.Rect(899, 94, self.saved_dresseur_pk_pv / self.dresseur.pk.pv * 225, 21))

            self.saved_dresseur_pk_pv -= self.dresseur.pk.pv / 75

        else:
            self.saved_dresseur_pk_pv = self.dresseur.pk.health

    def sac_item_update(self, surface, possouris, item, i):
        """
        Methode d'actualisation de l'affichage de l'emplacement d'objet dans l'action 'SAC'.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        @in : item, objet.Objet
        @in : i, int → indice de l'item dans le sac
        """
        if self.item_moving_mode and self.item_moving_i == i:
            item_rect = pygame.Rect(possouris[0] - self.current_moving_item_rel_possouris[0],
                                    possouris[1] - self.current_moving_item_rel_possouris[1],
                                    122,
                                    122)
        else:
            item_rect = self.objet_icon_rects[i].copy()

        # Hovering use_item_rect
        if self.use_item_rect.collidepoint(possouris) and self.item_moving_mode and self.item_moving_i == i:
            pygame.draw.rect(surface, (42, 214, 0), self.use_item_rect, width=10, border_radius=25)

        # Hovering
        if item_rect.collidepoint(possouris):
            surface.blit(self.sac_item_hover, item_rect)

        if item is not None:
            item_icon = pygame.transform.scale(item.icon_image, (90, 90))

            # Affichage icone
            surface.blit(item_icon, (
            item_rect.x + (122 - item_icon.get_width()) / 2, item_rect.y + (122 - item_icon.get_height()) / 2))

            # Affichage quantite
            surface.blit(self.item_quantite_font.render(str(item.quantite), False, (255, 255, 255)),
                         (item_rect.x + 90,
                          item_rect.y + 75))

            if not self.curseur_moving_mode:
                if not self.item_moving_mode:
                    if self.game.mouse_pressed[1] and item_rect.collidepoint(possouris):
                        self.item_moving_mode = True
                        self.item_moving_i = i
                        self.current_moving_item_rel_possouris = (possouris[0] - self.objet_icon_rects[i].x,
                                                                  possouris[1] - self.objet_icon_rects[i].y)
                else:
                    if self.item_moving_i == i:
                        if not self.game.mouse_pressed[1]:
                            self.item_moving_mode = False
                            self.item_moving_i = None
                            if self.use_item_rect.collidepoint(possouris):
                                if 'Use' in item.fonctionnement:
                                    sac_i = self.game.player.find_sac_item(item)

                                    self.current_turn_action = ('ITEM', item, sac_i)
                                    self.executing_turn = True

    def sac_curseur_update(self, possouris):
        """
        Methode d'actualisation de la position du curseur et de la possibilité de le déplacer à la souris.

        @in : possouris, list → coordonnées du pointeur de souris
        """
        if not self.item_moving_mode:
            if not self.curseur_moving_mode:
                if self.sac_action_curseur_rect.collidepoint(possouris) and self.game.mouse_pressed[1]:
                    self.curseur_moving_mode = True

            else:
                if not self.game.mouse_pressed[1]:
                    self.curseur_moving_mode = False
                else:
                    if possouris[1] < 520:
                        self.sac_action_curseur_pos = 0
                        self.sac_action_curseur_rect = self.sac_action_curseur_rects[0]
                    elif possouris[1] < 608:
                        self.sac_action_curseur_pos = 1
                        self.sac_action_curseur_rect = self.sac_action_curseur_rects[1]
                    else:
                        self.sac_action_curseur_pos = 2
                        self.sac_action_curseur_rect = self.sac_action_curseur_rects[2]

    def get_action_order(self, player_pk_action, dresseur_pk_action) -> str:
        """
        Déterminer l'ordre d'agissement des 2 pokemons.
        Renvoie le premier pokémon à attaquer.

        @in : player_pk_action & dresseur_pk_action, tuple → ('ITEM', objet.Objet(), i) ou ('ATTAQUE', attaques.Attaque())
        @out : str --> "player_pk" ou "dresseur_pk"
        """

        if self.player_pk.objet_tenu is not None and self.player_pk.objet_tenu.name == "Vive_Griffe":
            if random.randint(0, 1):
                return 'player_pk'

        elif self.dresseur.pk.objet_tenu is not None and self.dresseur.pk.objet_tenu.name == "Vive_Griffe":
            if random.randint(0, 1):
                return 'dresseur_pk'

        player_pk_action_type = player_pk_action[0]
        dresseur_pk_action_type = dresseur_pk_action[0]

        if player_pk_action_type == 'ITEM':  # Si le joueur utlise un objet, il est 1er
            return 'player_pk'
        elif dresseur_pk_action_type == 'ITEM':  # Si le dresseur utilise un objet mais pas le joueur, il est 1er
            return 'dresseur_pk'
        else:  # Si aucun des deux n'utilise d'objet
            player_pk_attaque = player_pk_action[1]
            dresseur_pk_attaque = dresseur_pk_action[1]

            if player_pk_attaque.priorite > dresseur_pk_attaque.priorite:
                return 'player_pk'
            elif player_pk_attaque.priorite < dresseur_pk_attaque.priorite:
                return 'dresseur_pk'
            else:
                # Si les deux attaques ont la meme priorité
                if self.player_pk.speed > self.dresseur.pk.speed:
                    # Si le pk du joueur est plus rapide
                    return 'player_pk'
                elif self.player_pk.speed < self.dresseur.pk.speed:
                    # Si le pk du dresseur est plus rapide
                    return 'dresseur_pk'
                else:
                    # Si les 2 pokemons ont la meme vitesse -> aléatoire
                    r_value = random.randint(0, 1)
                    if r_value:
                        return 'player_pk'
                    else:
                        return 'dresseur_pk'

    def turn(self, player_pk_action):
        """
        Methode qui réalise le tour de combat.
        Ordre :
            - Actualisation des effets de status des 2 pokémons
            - Attaque du 1er pokemon
            - Attaque du 2e pokemon (si encore vivant)
            - Application des effets de status sur le 1er pokémon (si encore vivant)
            - Application des effets de status sur le 2e pokémon (si encore vivant)

        @in: tuple → action du joueur
        """

        if self.compteur == 0:
            self.current_action = None
            self.compteur = 310
            self.dresseur_pk_action = ('ATTAQUE', get_npc_action(self.dresseur.pk, self.player_pk, self.dresseur.pk.attaque_pool))
            self.current_turn_order = self.get_action_order(player_pk_action, self.dresseur_pk_action)

        dresseur_pk_action = self.dresseur_pk_action

        # # # Actualisation des effets de status des 2 pokémons
        if self.compteur == 310:
            self.turn_exec_info = 'Actualisation des effets de status...'
            self.update_status_effects(self.player_pk)
            self.update_status_effects(self.dresseur.pk)

        # Si le premier pokémon à attaquer est le pokemon du joueur
        if self.current_turn_order == 'player_pk':

            # # # Actions des pokémons

            if player_pk_action[0] == 'ITEM':
                if self.compteur == 300:

                    item = player_pk_action[1]
                    i = player_pk_action[2]

                    self.exec_item_action(self.player_pk, item, i)
                    self.turn_exec_info = "Utilisation d'un objet..."

            if dresseur_pk_action[0] == 'ITEM':
                if self.compteur == 270:
                    item = dresseur_pk_action[1]

                    self.exec_item_action(self.dresseur.pk, item, None)
                    self.turn_exec_info = "Utilisation d'un objet..."

            if player_pk_action[0] == 'ATTAQUE':
                if self.compteur == 300:
                    if self.player_pk.is_alive:
                        attaque = player_pk_action[1]
                        self.exec_attaque_action(self.player_pk, self.dresseur.pk, attaque)
                        self.turn_exec_info = "Attaque des pokémons..."

            if dresseur_pk_action[0] == 'ATTAQUE':
                if self.compteur == 270:
                    if self.dresseur.pk.is_alive:
                        attaque = dresseur_pk_action[1]
                        self.exec_attaque_action(self.dresseur.pk, self.player_pk, attaque)
                        self.turn_exec_info = "Attaque des pokémons..."

            # # # Application des effets de status
            if self.compteur == 250:
                if self.dresseur.pk.is_alive:
                    self.apply_status_effects(self.player_pk)
                    self.turn_exec_info = "Application des effets de status..."
            if self.compteur == 230:
                if self.player_pk.is_alive:
                    self.apply_status_effects(self.dresseur.pk)
                    self.turn_exec_info = "Application des effets de status..."

        # Si le premier pokémon à attaquer est le pokémon du dresseur
        else:
            if dresseur_pk_action[0] == 'ITEM':
                if self.compteur == 300:
                    item = dresseur_pk_action[1]
                    self.exec_item_action(self.dresseur.pk, item, None)
                    self.turn_exec_info = "Utilisation d'un objet..."

            if player_pk_action[0] == 'ITEM':
                if self.compteur == 270:
                    item = player_pk_action[1]
                    i = player_pk_action[2]
                    self.exec_item_action(self.player_pk, item, i)
                    self.turn_exec_info = "Utilisation d'un objet..."

            if dresseur_pk_action[0] == 'ATTAQUE':
                if self.compteur == 300:
                    if self.dresseur.pk.is_alive:
                        attaque = dresseur_pk_action[1]
                        self.exec_attaque_action(self.dresseur.pk, self.player_pk, attaque)
                        self.turn_exec_info = "Attaque des pokémons..."

            if player_pk_action[0] == 'ATTAQUE':
                if self.compteur == 270:
                    if self.player_pk.is_alive:
                        attaque = player_pk_action[1]
                        self.exec_attaque_action(self.player_pk, self.dresseur.pk, attaque)
                        self.turn_exec_info = "Attaque des pokémons..."

                # # # Application des effets de status
                if self.compteur == 250:
                    self.apply_status_effects(self.dresseur.pk)
                    self.turn_exec_info = "Application des effets de status..."
                if self.compteur == 230:
                    self.apply_status_effects(self.player_pk)
                    self.turn_exec_info = "Application des effets de status..."

        if self.compteur == 200:
            self.turn_exec_info = "Vérification de victoire/défaite..."
            if not self.player_pk.is_alive:
                self.fight_result = 'Defeat'
                self.add_logs(('Result', "Defeat"))
                self.dresseur.pk.reset_stats()
                self.player_pk.reset_stats()
            elif not self.dresseur.pk.is_alive:
                self.fight_result = 'Victory'
                self.add_logs(('Result', "Victory"))
                self.dresseur.pk.reset_stats()
                self.player_pk.reset_stats()

            self.update_pk_attaques(player_pk_action, dresseur_pk_action)
            self.player_pk.reset_turn_effects()
            self.dresseur.pk.reset_turn_effects()
            self.player_pk.apply_turn_effects()
            self.dresseur.pk.apply_turn_effects()
            self.update_pk_item()
            self.executing_turn = False
            self.compteur = 1
            self.turn_exec_info = ""

        self.compteur -= 1

    def exec_item_action(self, pk, item, i):
        """
        Methode qui execute l'action d'un pokémon d'utiliser un item lors du tour.

        @in : pk, pokemon.Pokemon
        @in : item, objet.Objet
        @in : i, int → indice de l'item dans le sac
        """
        pk.use_item(item)

        item.quantite -= 1
        if i is not None:
            if item.quantite <= 0:
                self.game.player.sac[i] = None

        self.add_logs(('ITEM', pk, item))

    def exec_attaque_action(self, pk, ennemy_pk, attaque):
        """
        Methode qui execute l'action du pokémon d'attaquer

        @in : pk, pokemon.Pokemon → Pokémon attaquant
        @in : ennemy_pk, pokemon.Pokemon → Pokémon défenseur
        @in : attaque, attaques.Attaque → attaque éxécutée
        """

        # Verifications de status
        pk_can_atk = True
        if pk.status['Sommeil']:
            pk_can_atk = False
            self.add_logs(('Status effect', pk, 'Sommeil'))
        if pk.status['Gel']:
            pk_can_atk = False
            self.add_logs(('Status effect', pk, 'Gel'))
        if pk.status['Paralysie']:
            if random.randint(1, 4) == 1:
                pk_can_atk = False
                self.add_logs(('Status effect', pk, 'Paralysie'))
        if pk.status['Confusion']:
            if random.randint(1, 3) == 1:
                pk_can_atk = False
                self.add_logs(('Status effect', pk, 'Confusion'))
                pk.attaque(pk, attaques.Attaque('Charge'))

        if pk_can_atk:
            # Attaque le pokemon ennemi et affecte le resultat de l'attaque dans reussite_attaque (bool)
            info_attaque = pk.attaque(ennemy_pk, attaque)

            if info_attaque[0]:  # Si l'attaque a abouti
                self.add_logs(('ATTAQUE', pk, attaque))

            if info_attaque[1] is not None:  # Si un effet a été appliqué
                self.add_logs(('Status effect', info_attaque[1][1], info_attaque[1][0]))

    def add_logs(self, info):
        """
        Methode qui ajoute aux logs du combat une information.

        @in : info, tuple → ex: ('Result', 'Victoire') ou ('ATTAQUE', pokemon.Pokemon, attaques.Attaque) ...
        """
        if len(self.fight_logs) >= 6:
            self.fight_logs.pop(0)

        self.fight_logs.append(info)

    def update_fight_logs(self, surface):
        """
        Methode d'actualisation de l'affichage des logs du combat.

        @in : surface, pygame.Surface → fenêtre du jeu
        """
        x = 13
        y = 248

        logs = self.fight_logs.copy()
        logs.reverse()

        for info in logs:

            if info[1] == self.player_pk:
                pk_color = (0, 36, 255)
            else:
                pk_color = (255, 0, 0)

            if info[0] == 'ITEM' or info[0] == 'ATTAQUE':
                nom = self.fight_logs_font.render(f'{info[1].name} ', False, pk_color)
                utilise = self.fight_logs_font.render('utilise ', False, (51, 51, 51))
                action = self.fight_logs_font.render(f'{info[2].name_}', False, (0, 0, 0))

                surface.blit(nom, (x, y))
                surface.blit(utilise, (x + nom.get_width(), y))
                surface.blit(action, (x + nom.get_width() + utilise.get_width(), y))

            elif info[0] == 'Result':
                if info[1] == 'Victory':
                    color = (0, 180, 30)
                    resultat = self.fight_logs_font.render('gagné !', False, color)
                else:
                    resultat = self.fight_logs_font.render('perdu.', False, (180, 0, 0))
                    color = (180, 0, 0)

                nom = self.fight_logs_font.render(f'{self.player_pk.name} ', False, color)
                a = self.fight_logs_font.render('a ', False, color)

                surface.blit(nom, (x, y))
                surface.blit(a, (x + nom.get_width(), y))
                surface.blit(resultat, (x + nom.get_width() + a.get_width(), y))

            elif info[0] == 'End of Status':
                if info[2] == 'Brulure':
                    status = self.fight_logs_font.render(f'brûlé ', False, (255, 143, 0))
                elif info[2] == 'Poison':
                    status = self.fight_logs_font.render(f'empoisonné ', False, (220, 0, 255))
                elif info[2] == 'Gel':
                    status = self.fight_logs_font.render(f'gelé ', False, (0, 236, 255))
                elif info[2] == 'Sommeil':
                    status = self.fight_logs_font.render(f'endormi ', False, (0, 36, 108))
                elif info[2] == 'Confusion':
                    status = self.fight_logs_font.render(f'confus ', False, (159, 157, 0))
                elif info[2] == 'Paralysie':
                    status = self.fight_logs_font.render(f'paralysé ', False, (254, 239, 0))

                nom = self.fight_logs_font.render(f'{info[1].name} ', False, pk_color)
                phrase = self.fight_logs_font.render("n'est plus ", False, (51, 51, 51))

                surface.blit(nom, (x, y))
                surface.blit(phrase, (x + nom.get_width(), y))
                surface.blit(status, (x + nom.get_width() + phrase.get_width(), y))

            elif info[0] == 'Status effect':
                if info[2] == 'Brulure':
                    status = self.fight_logs_font.render(f'brûlé ', False, (255, 143, 0))
                elif info[2] == 'Poison':
                    status = self.fight_logs_font.render(f'empoisonné ', False, (220, 0, 255))
                elif info[2] == 'Gel':
                    status = self.fight_logs_font.render(f'gelé ', False, (0, 236, 255))
                elif info[2] == 'Sommeil':
                    status = self.fight_logs_font.render(f'endormi ', False, (0, 36, 108))
                elif info[2] == 'Confusion':
                    status = self.fight_logs_font.render(f'confus ', False, (159, 157, 0))
                elif info[2] == 'Paralysie':
                    status = self.fight_logs_font.render(f'paralysé ', False, (254, 239, 0))

                nom = self.fight_logs_font.render(f'{info[1].name} ', False, pk_color)
                phrase = self.fight_logs_font.render("est ", False, (51, 51, 51))

                surface.blit(nom, (x, y))
                surface.blit(phrase, (x + nom.get_width(), y))
                surface.blit(status, (x + nom.get_width() + phrase.get_width(), y))

            y -= 45

    def img_load(self, file_name):
        return pygame.image.load(self.path + file_name + '.png')

    def get_rewards(self):
        """
        Methode permettant de donner au joueur les recompenses du combat.
        """
        # utilisation d'une action pour reclamer recompense
        if self.fight_type != 'Boss':
            self.game.player.use_action()

        # Obtention des objets de récompense
        r_values_list = []
        rewards = []
        for n in range(self.reward_quantity):
            r_values_list.append(random.randint(0, self.game.get_total_items_rarity()))

        acc = 0
        for objet in self.game.get_items_list()['Spawnable']:
            for r_value in r_values_list:
                if r_value in range(acc, acc + (100 - objet.rarity)):
                    objet.quantite = random.randint(objet.quantite_at_spawn[0], objet.quantite_at_spawn[1])
                    rewards.append(objet)
            acc += (100 - objet.rarity)

        # level up du pokemon
        if self.difficult == 'easy':
            self.player_pk.level_up()
            self.game.player.add_money(random.randint(150, 350))

            self.game.notif(f'{self.player_pk.name} a gagné 1 level !', (0, 0, 255))
        elif self.difficult == 'normal':
            self.player_pk.level_up(2)
            self.game.player.add_money(random.randint(350, 650))

            self.game.notif(f'{self.player_pk.name} a gagné 2 levels !', (0, 0, 255))
        elif self.difficult == 'hard':
            self.player_pk.level_up(3)
            self.game.player.add_money(random.randint(650, 1050))

            self.game.notif(f'{self.player_pk.name} a gagné 3 levels !', (0, 0, 255))

        return rewards

    def end_fight(self):
        """
        Methode permettant de terminer le combat.
        """
        self.dresseur.pk.full_heal()  # Remettre full vie le pokémon du dresseur
        self.dresseur.pk.reset_status()

        if self.fight_result == 'Victory':
            rewards = self.get_rewards()

            for reward in rewards:
                self.game.player.add_sac_item(reward)

            self.player_pk.heal(self.player_pk.passive_heal)  # Heal le pokémon du joueur selon son heal passif
            self.player_pk.reset_status()

            self.game.end_fight()

        elif self.fight_type == 'Boss':   # Si c'est une défaite contre un boss
            self.game.game_over()

        else:  # Si c'est une défaite contre un pokémon sauvage
            self.game.end_fight()

    def apply_status_effects(self, pk):
        """
        Methode qui applique les effets de status du pokémon pris en parametre d'entrée.

        @in : pk, pokemon.Pokemon
        """
        print('Application des effets du pokemon :', pk.name)
        if pk.status["Brulure"]:
            pk.damage(round(pk.pv / 16))
            print('Degats brulure')

        if pk.status["Poison"]:
            pk.damage(round(pk.pv / 8))
            print('Degats poison')

        if pk.status["Paralysie"]:
            pk.speed = round(pk.base_speed / 2)
            print('Baisse de la speed de la paralysie. Nouvelle speed:', pk.speed)

        if pk.status["Gel"]:
            print('Effet Gel ')

        if pk.status["Sommeil"]:
            print('Effet Sommeil')

        if pk.status["Confusion"]:
            print('Effet confusion')

    def update_status_effects(self, pk):
        """
        Methode d'actualisation des effets de status du pokémon pris en parametre d'entrée.

        @in : pk, pokemon.Pokemon
        """
        print('Update des effets du pokemon :', pk.name)
        if pk.status["Brulure"]:
            if random.randint(1, 8) == 3:
                pk.status["Brulure"] = False
                self.add_logs(('End of Status', pk, 'Brulure'))

        if pk.status["Poison"]:
            if random.randint(1, 4) == 3:
                pk.status["Poison"] = False
                self.add_logs(('End of Status', pk, 'Poison'))

        if pk.status["Paralysie"]:
            if random.randint(1, 10) == 3:
                pk.status["Paralysie"] = False
                pk.speed = pk.base_speed
                self.add_logs(('End of Status', pk, 'Paralysie'))

        if pk.status["Gel"]:
            if random.randint(1, 5) == 3:
                pk.status["Gel"] = False
                self.add_logs(('End of Status', pk, 'Gel'))

        if pk.status["Sommeil"]:
            if self.sommeil_compteur_tour[pk] == -1:
                self.sommeil_compteur_tour[pk] = 3
            if random.randint(1, 1 + self.sommeil_compteur_tour[pk]) == 1:
                pk.status["Sommeil"] = False
                self.sommeil_compteur_tour[pk] = -1
                self.add_logs(('End of Status', pk, 'Sommeil'))
            else:
                self.sommeil_compteur_tour[pk] -= 1

        if pk.status["Confusion"]:
            if self.confusion_compteur_tour[pk] == -1:
                self.confusion_compteur_tour[pk] = 4
            if random.randint(1, 1 + self.confusion_compteur_tour[pk]) == 1:
                pk.status["Confusion"] = False
                self.confusion_compteur_tour[pk] = -1
                self.add_logs(('End of Status', pk, 'Confusion'))
            else:
                self.confusion_compteur_tour[pk] -= 1

    def update_pk_attaques(self, player_pk_action, dresseur_pk_action):
        """
        Methode d'actualisation de certain effets des attaques des pokémons d'un tour à l'autre.

        @in : player_pk_action, tuple → ('ITEM', objet.Objet) ou ('ATTAQUE', attaques.Attaque)
        @in : dresseur_pk_action, tuple → ('ITEM', objet.Objet) ou ('ATTAQUE', attaques.Attaque)
        """
        # Pokémon du joueur
        for attaque in self.player_pk.attaque_pool:
            if attaque is not None:
                if attaque.bool_special_precision:
                    if attaque.special_precision[0] == 'd':
                        if player_pk_action[1] == attaque:
                            attaque.precision -= int(attaque.special_precision[1].split('-')[1])
                        else:
                            attaque.precision = int(attaque.special_precision[1].split('-')[0])

        # Pokemon du dresseur
        for attaque in self.dresseur.pk.attaque_pool:
            if attaque is not None:
                if attaque.bool_special_precision:
                    if attaque.special_precision[0] == 'd':
                        if dresseur_pk_action[1] == attaque:
                            attaque.precision -= int(attaque.special_precision[1].split('-')[1])
                        else:
                            attaque.precision = int(attaque.special_precision[1].split('-')[0])

    def update_pk_item(self):
        """
        Methode qui actualise les effets des objets tenus par les pokemons
        """

        # Pokémon du joueur
        if self.player_pk.objet_tenu is not None:
            self.player_pk.update_item_turn_effects()

        # Pokemon du dresseur
        if self.dresseur.pk.objet_tenu is not None:
            self.dresseur.pk.update_item_turn_effects()

    def left_clic_interactions(self, possouris):
        """
        Méthode gérant les intéractions de l'utilisateur avec le clic gauche de la souris.

        @in : possouris, list → coordonnées du pointeur de souris
        """
        if not self.executing_turn:
            if self.fight_result is None:
                # Si aucune action n'est en cours
                if self.current_action is None:
                    if self.fuite_button_rect.collidepoint(possouris):
                        self.dresseur.pk.full_heal()
                        self.dresseur.pk.reset_status()
                        self.player_pk.reset_status()
                        # reset les altérations de stats des attaques
                        self.player_pk.reset_attaque_fight()
                        self.dresseur.pk.reset_attaque_fight()
                        self.game.cancel_fight()
                    elif self.combat_button_rect.collidepoint(possouris):
                        self.current_action = 'COMBAT'
                    elif self.sac_button_rect.collidepoint(possouris):
                        self.current_action = 'SAC'

                # Si l'action en cours est 'COMBAT'
                elif self.current_action == 'COMBAT':
                    if self.attaque_buttons_rects[0].collidepoint(possouris) and self.player_pk.attaque_pool[0] is not None:
                        self.current_turn_action = ('ATTAQUE', self.player_pk.attaque_pool[0])
                        self.executing_turn = True

                    elif self.attaque_buttons_rects[1].collidepoint(possouris) and self.player_pk.attaque_pool[1] is not None:
                        self.current_turn_action = ('ATTAQUE', self.player_pk.attaque_pool[1])
                        self.executing_turn = True

                    elif self.attaque_buttons_rects[2].collidepoint(possouris) and self.player_pk.attaque_pool[2] is not None:
                        self.current_turn_action = ('ATTAQUE', self.player_pk.attaque_pool[2])
                        self.executing_turn = True

                    elif self.attaque_buttons_rects[3].collidepoint(possouris) and self.player_pk.attaque_pool[3] is not None:
                        self.current_turn_action = ('ATTAQUE', self.player_pk.attaque_pool[3])
                        self.executing_turn = True
            else:
                if self.boolEnding:
                    pass
                else:
                    if self.fin_du_combat_button_rect.collidepoint(possouris):
                        # self.boolEnding = True
                        self.end_fight()

    def is_hovering(self, possouris):
        """
        Méthode qui retourne True si la souris est positionnée sur un bouton du panel.

        @in : possouris, list → coordonnées du pointeur de souris
        @out : bool
        """
        if self.fight_result is None:
            if self.current_action is None:
                return (self.sac_button_rect.collidepoint(possouris) or
                        self.combat_button_rect.collidepoint(possouris) or
                        self.fuite_button_rect.collidepoint(possouris)
                        )
            elif self.current_action == 'COMBAT':
                return ((self.attaque_buttons_rects[0].collidepoint(possouris) and self.player_pk.attaque_pool[0] is not None) or
                        (self.attaque_buttons_rects[1].collidepoint(possouris) and self.player_pk.attaque_pool[1] is not None) or
                        (self.attaque_buttons_rects[2].collidepoint(possouris) and self.player_pk.attaque_pool[2] is not None) or
                        (self.attaque_buttons_rects[3].collidepoint(possouris) and self.player_pk.attaque_pool[3] is not None)
                        )
            elif self.current_action == 'SAC':
                return (self.sac_action_curseur_rect.collidepoint(possouris) or self.curseur_moving_mode
                        or self.objet_icon_rects[0].collidepoint(possouris)
                        or self.objet_icon_rects[1].collidepoint(possouris)
                        or self.objet_icon_rects[2].collidepoint(possouris)
                        or self.objet_icon_rects[3].collidepoint(possouris)
                        or self.objet_icon_rects[4].collidepoint(possouris)
                        or self.objet_icon_rects[5].collidepoint(possouris)
                        or self.objet_icon_rects[6].collidepoint(possouris)
                        or self.objet_icon_rects[7].collidepoint(possouris)
                        or self.item_moving_mode
                        )
            else:
                return False
        else:
            if self.boolEnding:
                pass
            else:
                return self.fin_du_combat_button_rect.collidepoint(possouris)


"""
Fonctions de calcul du selection de l'action à réaliser par les PNJ (Personnage Non-Joueur) durant un combat.
"""

# CONSTANTES
SPEED_HEAL = 333  # valeur entre 0 et 1000


# FONCTIONS
def calcul_degats(pk, ennemy_pk, attaque, crit=False) -> int:
    """
    Methode de calcul des dégats simulés d'une attaque du pokémon du PNJ sur le pokémon du joueur.
    Retourne le montant de dégats de la simulation sur le pokémon du joueur.

    @in: pk, pokemon.Pokemon => Pokémon du PNJ
    @in: ennemy_pk, pokemon.Pokemon => Pokémon du joueur
    @in: attaque, attaque.Attaque => Attaque simulée
    @in: crit, bool => True si l'attaque critique, False sinon
    @out: degats, int
    """
    if attaque.puissance != 0 and ennemy_pk.is_vulnerable:
        cm = 1
        # Calcul avec stab ( attaque de type maternel )
        if attaque.type in [pk.type, pk.type2]:
            cm *= 1.5

        # Calcul avec affinités des types
        cm *= game_infos.get_mutiliplicateur(attaque.type, ennemy_pk.type)

        if not ennemy_pk.type2 == 'NoType':
            cm *= game_infos.get_mutiliplicateur(attaque.type, ennemy_pk.type2)

        if crit:
            cm *= (2 * pk.level + 5) / (pk.level + 5)

        if attaque.puissance == "level":
            puissance = pk.level
        elif attaque.puissance == "ennemy_pv":
            puissance = 1000000
        elif attaque.puissance == "pv*0.5":
            puissance = ennemy_pk.health // 2
        elif attaque.special_puissance == 'v':
            if pk.speed <= ennemy_pk.speed:
                puissance = int(attaque.puissance.split("-")[0])
            else:
                puissance = int(attaque.puissance.split("-")[1])
        else:
            puissance = attaque.puissance

        if attaque.special_puissance == 'c':
            degats = attaque.puissance
        elif attaque.puissance == "effort":
            degats = ennemy_pk.pv - pk.health
        else:
            degats = round((((((pk.level * 0.4 + 2) * pk.attack * puissance) / pk.defense) / 50) + 2) * cm)


    else:
        degats = 0

    return degats


def get_npc_action(pk, ennemy_pk, att: list) -> attaques.Attaque:
    """
    Methode de selection de la meilleure action à réaliser pour le pokémon du PNJ.
    Retourne l'attaque à réaliser.

    @in: pk, pokemon.Pokemon => Pokémon du PNJ
    @in: ennemy_pk, pokemon.Pokemon => Pokémon du joueur
    @in: att, list => liste d'attaque du pokémon du PNJ
    @out: attaque.Attaque => Meilleure attaque à réaliser pour le pokémon du PNJ
    """
    score = []
    is_killing = []
    for attaque in att:
        if attaque is not None:
            degat = calcul_degats(pk, ennemy_pk, attaque, False)
            if degat > ennemy_pk.health:
                is_killing.append(attaque)

    if is_killing == []:
        for attaque in att:
            if attaque is not None:
                degat = calcul_degats(pk, ennemy_pk, attaque, False)
                degat_crit = calcul_degats(pk, ennemy_pk, attaque, True)
                delta_degat = degat_crit - degat
                t = round(int(pk.infos[6]) / 2) * attaque.taux_crit
                scoretemp = degat + delta_degat * t
                taux = attaque.precision / 100

                # Calcul des bonus spéciaux des attaques ( altération de status, double attaque, invnlnérabilités,
                if attaque.special_effect[0][0] == 'status' and ennemy_pk.status[
                    str(attaque.special_effect[0][1])] is not True:
                    scoretemp *= (1 + int(attaque.special_effect[0][2]) / 100)

                scoretemp *= taux
                if attaque.special_effect[0][0] == 'heal_on_maxpv' or attaque.special_effect[
                    0] == 'long_time_heal_par_tour_of_maxpv':
                    scoretemp += (pk.pv / pk.health - 1) * round((pk.level * 0.4 * pk.attack) / pk.defense) * 150
                if attaque.special_effect[0][0] == 'heal_on_atk':
                    taux_heal_on_atk, _ = attaque.special_effect[0][1].split("*")
                    # scoretemp = scoretemp * (1 + (SPEED_HEAL/400) * float(taux_heal_on_atk))
                    scoretemp = scoretemp * (
                                1 + (SPEED_HEAL / 400) * float(taux_heal_on_atk) * (-2 * (pk.health / pk.pv) + 2))

                # print(attaque.name, scoretemp)

                score.append(scoretemp)

        max = score[0]
        j = 0
        for i in range(len(score)):
            if score[i] > max:
                max = score[i]
                j = i

        return att[j]

    else:
        for attaque in is_killing:
            score.append(attaque.precision)

        max = score[0]
        j = 0
        for i in range(len(score)):
            if score[i] > max:
                max = score[i]
                j = i
        return is_killing[j]
