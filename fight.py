# importation des modules
import pygame
import random

import dresseur
import game_infos
import pokemon
from dresseur import Alizee, Olea, Ondine, Pierre, Blue, Red, Iris, Sauvage
from bot_fight_algo import get_npc_action

# modif
import objet

# declaration des constante
DRESSEUR_LIST = [Alizee, Olea, Ondine, Pierre, Blue, Red, Iris]


# declaration de fighte
class Fight:

    def __init__(self, game, player_pk, dresseur_class=None, dresseur_pk=None, difficult='easy'):
        """
        La classe Fight est définie par:
        - Le pokemon envoyé par le joueur (player_pk)
        - Le dresseur à affronter (dresseur_class)
        """

        self.game = game
        self.player_pk = player_pk
        self.dresseur = self.init_dresseur(dresseur_class, dresseur_pk)

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
        self.attaque_font = pygame.font.Font('assets/fonts/Cheesecake.ttf', 55)
        self.sac_page_font = pygame.font.Font('assets/fonts/Cheesecake.ttf', 65)
        self.item_quantite_font = pygame.font.Font('assets/fonts/Impact.ttf', 30)
        self.fight_logs_font = pygame.font.Font('assets/fonts/Cheesecake.ttf', 40)

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

        self.reward_quantity = 2
        self.difficult = difficult
        
        self.fight_logs = []
        self.fight_result = None

        self.compteur = 0
        self.compteur_action_file = []

        self.boolEnding = False
        self.compteur_end_fight = 0

    def update(self, surface: pygame.surface.Surface, possouris):

        surface.blit(self.background, (0, 0))

        self.update_pokemons(surface)
        self.update_buttons(surface, possouris)
        self.update_current_action(possouris)

        if not self.boolEnding:
            if self.fight_result is None:
                if not self.current_turn_action == ('NoAction', None):
                    self.turn(self.current_turn_action, ('ATTAQUE', get_npc_action(self.dresseur.pk, self.player_pk, self.dresseur.pk.attaque_pool)))

            if self.compteur != 0:
                if self.compteur == 100 or self.compteur == 50:
                    if self.fight_result is None:
                        f = self.compteur_action_file[0][0]
                        param1 = self.compteur_action_file[0][1]
                        param2 = self.compteur_action_file[0][2]
                        param3 = self.compteur_action_file[0][3]

                        f(param1, param2, param3)
                    self.compteur_action_file.pop(0)
                    self.compteur -= 1
                elif self.compteur == 1:
                    if self.fight_result is None:
                        self.apply_status_effect(self.player_pk)
                    if self.fight_result is None:
                        self.apply_status_effect(self.dresseur.pk)

                    self.compteur -= 1
                else:
                    self.compteur -= 1

        self.update_fight_logs(surface)

        if self.boolEnding:
            self.update_fight_end(surface, possouris)

        # GESTION CURSEUR INTERACTIONS
        if self.is_hovering(possouris):
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def update_fight_end(self, surface, possouris):

        # Panel
        alpha_panel = self.compteur_end_fight**2/2
        if alpha_panel > 255:
            alpha_panel = 255
        self.end_fight_panel.set_alpha(alpha_panel)

        surface.blit(self.end_fight_panel, (0, 0))

        # Stats
        alpha_stats = -150 + self.compteur_end_fight*5
        if alpha_stats > 255:
            alpha_stats = 255

        self.lv.set_alpha(alpha_stats)
        self.pv.set_alpha(alpha_stats)
        self.atk.set_alpha(alpha_stats)
        self.defense.set_alpha(alpha_stats)
        self.vit.set_alpha(alpha_stats)

        x_stats = 80 - self.compteur_end_fight
        if x_stats < 0:
            x_stats = 0

        surface.blit(self.lv, (self.lv_rect.x + x_stats, self.lv_rect.y))
        surface.blit(self.pv, (self.pv_rect.x + x_stats, self.pv_rect.y))
        surface.blit(self.atk, (self.atk_rect.x + x_stats, self.atk_rect.y))
        surface.blit(self.defense, (self.defense_rect.x + x_stats, self.defense_rect.y))
        surface.blit(self.vit, (self.vit_rect.x + x_stats, self.vit_rect.y))

        # Icone
        self.pk_icon.set_alpha(alpha_stats)
        surface.blit(self.pk_icon, (42, 124), (0, 0, 480, 480))

        self.compteur_end_fight += 1

    def update_current_action(self, possouris):
        if self.current_action is not None:
            if not self.item_moving_mode:
                if not self.current_action_rect.collidepoint(possouris):
                    self.current_action = None

    def add_logs(self, info):
        if len(self.fight_logs) >= 6:
            self.fight_logs.pop(0)

        self.fight_logs.append(info)

    def update_fight_logs(self, surface):
        x = 13
        y = 248

        logs = self.fight_logs.copy()
        logs.reverse()

        for pk, attaque in logs:

            if pk == self.player_pk:
                pk_color = (0, 36, 255)
            else:
                pk_color = (255, 0, 0)

            if attaque == 'Defeat':
                nom = self.fight_logs_font.render(f'{pk.name} ', False, (180, 0, 0))
                liaison = self.fight_logs_font.render('a ', False, (180, 0, 0))
                attaque_render = self.fight_logs_font.render('perdu.', False, (180, 0, 0))
            elif attaque == 'Victory':
                nom = self.fight_logs_font.render(f'{pk.name} ', False, (0, 180, 30))
                liaison = self.fight_logs_font.render('a ', False, (0, 180, 30))
                attaque_render = self.fight_logs_font.render('gagné !', False, (0, 180, 30))
            else:

                nom = self.fight_logs_font.render(f'{pk.name} ', False, pk_color)
                liaison = self.fight_logs_font.render('utilise ', False, (51, 51, 51))
                attaque_render = self.fight_logs_font.render(f'{attaque.name_}', False, (0, 0, 0))

            surface.blit(nom, (x, y))
            surface.blit(liaison, (x + nom.get_width(), y))
            surface.blit(attaque_render, (x + nom.get_width() + liaison.get_width(), y))

            y -= 45

    def update_pokemons(self, surface):
        # Pokemon du joueur
        # Icone
        surface.blit(pygame.transform.scale(self.player_pk.icon_image, (700, 350)), (180, 270), (0, 0, 350, 350))
        # Barre d'info
        surface.blit(self.pk_info_bar, self.player_pk_info_bar_rect, (0, 0, 434, 144))
        # Barre de vie verte
        pygame.draw.rect(surface, (42, 214, 0),
                         pygame.Rect(31, 646, self.player_pk.health / self.player_pk.pv * 263, 24))
        # PV
        surface.blit(
            self.pk_pv_font.render(str(self.player_pk.health) + "/" + str(self.player_pk.pv),
                                        False, (40, 40, 40)), (39, 669))
        # Nom
        surface.blit(self.player_pk_name, (40, 584))

        # Pokemon du dresseur
        # Icone
        surface.blit(pygame.transform.scale(self.dresseur.pk.icon_image, (600, 300)), (770, 80), (0, 0, 300, 300))
        # Barre d'info
        surface.blit(self.pk_info_bar, self.dresseur_pk_info_bar_rect, (434, 0, 369, 123))
        # Barre de vie verte
        pygame.draw.rect(surface, (42, 214, 0),
                         pygame.Rect(899, 94, self.dresseur.pk.health / self.dresseur.pk.pv * 225, 21))
        # Nom
        surface.blit(self.dresseur_pk_name, (905, 51))

    def update_buttons(self, surface, possouris):

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
                    button_rect = self.attaque_buttons_rects[i]
                    pygame.draw.rect(surface, game_infos.type_colors[self.player_pk.attaque_pool[i].type],
                                     button_rect,
                                     border_radius=15)

                    if button_rect.collidepoint(possouris):
                        surface.blit(self.cover_attaque_button, button_rect)
                        surface.blit(self.cover_attaque_button_hover, button_rect)

                        attaque_name_shadow = self.attaque_font.render(self.player_pk.attaque_pool[i].name_, False,
                                                                       (30, 30, 30))
                        surface.blit(attaque_name_shadow, (button_rect.x + 1 + (356 - attaque_name_shadow.get_width()) / 2,
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
                surface.blit(self.sac_page_font.render(str(self.sac_action_curseur_pos+1), False, (255, 255, 255)),
                             (1218, 357))

                if self.sac_action_curseur_rect.collidepoint(possouris) or self.curseur_moving_mode:
                    img_rect = (23, 0, 23, 66)
                else:
                    img_rect = (0, 0, 23, 66)

                surface.blit(self.sac_action_curseur,
                             (self.sac_action_curseur_rect.x + 2, self.sac_action_curseur_rect.y + 5*(self.sac_action_curseur_pos+1)),  # Co du curseur
                             img_rect)

                if self.sac_action_curseur_pos == 0:
                    i = 0
                    for objet in self.game.player.sac_page1[0:8]:
                        self.sac_item_update(surface, possouris, objet, i)
                        i += 1
                elif self.sac_action_curseur_pos == 1:
                    i = 8
                    for objet in self.game.player.sac_page1[8:]:
                        self.sac_item_update(surface, possouris, objet, i)
                        i += 1
                    for objet in self.game.player.sac_page2[0:4]:
                        self.sac_item_update(surface, possouris, objet, i)
                        i += 1
                else:
                    i = 16
                    for objet in self.game.player.sac_page2[4:]:
                        self.sac_item_update(surface, possouris, objet, i)
                        i += 1

        else:
            if self.fin_du_combat_button_rect.collidepoint(possouris):
                surface.blit(self.fin_du_combat_button, self.fin_du_combat_button_rect, (425, 0, 425, 101))
            else:
                surface.blit(self.fin_du_combat_button, self.fin_du_combat_button_rect, (0, 0, 424, 101))

    def sac_item_update(self, surface, possouris, item, i):
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
            surface.blit(item_icon, (item_rect.x + (122 - item_icon.get_width()) / 2, item_rect.y + (122 - item_icon.get_height()) / 2))

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
                                    self.current_turn_action = ('ITEM', item, i)

    def sac_curseur_update(self, possouris):
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

    def is_hovering(self, possouris):
        if self.fight_result is None:
            if self.current_action is None:
                return (self.sac_button_rect.collidepoint(possouris) or
                        self.combat_button_rect.collidepoint(possouris) or
                        self.fuite_button_rect.collidepoint(possouris)
                        )
            elif self.current_action == 'COMBAT':
                return (self.attaque_buttons_rects[0].collidepoint(possouris) or
                        self.attaque_buttons_rects[1].collidepoint(possouris) or
                        self.attaque_buttons_rects[2].collidepoint(possouris) or
                        self.attaque_buttons_rects[3].collidepoint(possouris)
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

    def left_clic_interactions(self, possouris):  # Quand l'utilisateur utilise le clic gauche
        if self.fight_result is None:
            # Si aucune action n'est en cours
            if self.current_action is None:
                    if self.fuite_button_rect.collidepoint(possouris):
                        self.game.cancel_fight()
                    elif self.combat_button_rect.collidepoint(possouris):
                        self.current_action = 'COMBAT'
                    elif self.sac_button_rect.collidepoint(possouris):
                        self.current_action = 'SAC'

            # Si l'action en cours est 'COMBAT'
            elif self.current_action == 'COMBAT':
                if self.attaque_buttons_rects[0].collidepoint(possouris):
                    self.current_turn_action = ('ATTAQUE', self.player_pk.attaque_pool[0])

                elif self.attaque_buttons_rects[1].collidepoint(possouris):
                    self.current_turn_action = ('ATTAQUE', self.player_pk.attaque_pool[1])

                elif self.attaque_buttons_rects[2].collidepoint(possouris):
                    self.current_turn_action = ('ATTAQUE', self.player_pk.attaque_pool[2])

                elif self.attaque_buttons_rects[3].collidepoint(possouris):
                    self.current_turn_action = ('ATTAQUE', self.player_pk.attaque_pool[3])
        else:
            if self.boolEnding:
                pass
            else:
                if self.fin_du_combat_button_rect.collidepoint(possouris):
                    self.boolEnding = True

    def turn(self, player_pk_action, dresseur_pk_action):

        self.update_status_effect(self.player_pk)
        self.update_status_effect(self.dresseur.pk)

        pk1, pk2 = self.get_action_order(player_pk_action, dresseur_pk_action)
        if pk1[1][0] == 'ITEM' and pk1[0].is_alive:
            self.compteur_action_file.append((self.apply_item_action, pk1[0], pk1[1][1], pk1[1][2]))

        if pk2[1][0] == 'ITEM' and pk2[0].is_alive:
            self.compteur_action_file.append((self.apply_item_action, pk2[0], pk2[1][1], pk2[1][2]))

        if pk1[1][0] == 'ATTAQUE' and pk1[0].is_alive:
            self.compteur_action_file.append((self.apply_attaque_action, pk1[0], pk2[0], pk1[1][1]))

        if pk2[1][0] == 'ATTAQUE' and pk2[0].is_alive:
            self.compteur_action_file.append((self.apply_attaque_action, pk2[0], pk1[0], pk2[1][1]))

        self.current_turn_action = ('NoAction', None)

        self.compteur = 100

    def apply_item_action(self, pk, item, item_i):
        pk.use_item(item)

        if pk == self.player_pk:
            item.quantite -= 1

            if item.quantite <= 0:
                if item_i < 12:
                    self.game.player.sac_page1[item_i] = None
                else:
                    self.game.player.sac_page2[item_i - 12] = None

        self.add_logs((pk, item))

        if not self.player_pk.is_alive:
            self.fight_result = 'Defeat'
            self.add_logs((self.player_pk, 'Defeat'))
        elif not self.dresseur.pk.is_alive:
            self.fight_result = 'Victory'
            self.add_logs((self.player_pk, 'Victory'))

    def apply_attaque_action(self, pk, ennemy_pk, attaque):

        pk_can_atk = True

        if pk.status['Sommeil']:
            pk_can_atk = False
        if pk.status['Gel']:
            pk_can_atk = False
        if pk.status['Paralysie']:
            if random.randint(1, 4) == 1:
                pk_can_atk = False
        if pk.status['Confusion']:
            if random.randint(1, 3) == 1:
                pk_can_atk = False
                pk.attaque(pk, attaque.Attaque('Charge'))

        if pk_can_atk:
            pk.attaque(ennemy_pk, attaque)

        self.add_logs((pk, attaque))

        if not self.player_pk.is_alive:
            self.fight_result = 'Defeat'
            self.add_logs((self.player_pk, 'Defeat'))
        elif not self.dresseur.pk.is_alive:
            self.fight_result = 'Victory'
            self.add_logs((self.player_pk, 'Victory'))

    def get_action_order(self, player_pk_action, dresseur_pk_action):
        """Déterminer l'ordre d'agissement des 2 pokemons"""

        player_pk_action_type, dresseur_pk_action_type = player_pk_action[0], dresseur_pk_action[0]

        if 'ITEM' in (player_pk_action_type, dresseur_pk_action_type):
            if player_pk_action_type == 'ITEM':
                return (self.player_pk,player_pk_action), (self.dresseur.pk,dresseur_pk_action)
            elif dresseur_pk_action_type == 'ITEM':
                return (self.dresseur.pk,dresseur_pk_action), (self.player_pk,player_pk_action)

        else:
            if not player_pk_action[1].priorite == dresseur_pk_action[1].priorite:
                if player_pk_action[1].priorite > dresseur_pk_action[1].priorite:
                    return (self.player_pk,player_pk_action), (self.dresseur.pk,dresseur_pk_action)
                elif player_pk_action[1].priorite < dresseur_pk_action[1].priorite:
                    return (self.dresseur.pk,dresseur_pk_action), (self.player_pk,player_pk_action)
            else:
                if self.player_pk.speed >= self.dresseur.pk.speed:
                    return (self.player_pk,player_pk_action),(self.dresseur.pk,dresseur_pk_action)
                else:
                    return (self.dresseur.pk,dresseur_pk_action),(self.player_pk,player_pk_action)

    def init_dresseur(self, dresseur_class, dresseur_pk=None):
        if dresseur_class is None:
            dresseur_class = random.choice(DRESSEUR_LIST)  # À modifier avec les niveaux de difficultés des dresseurs...

        return dresseur_class(self.game, pk=dresseur_pk)

    def img_load(self, file_name):
        return pygame.image.load(self.path + file_name + '.png')

    def get_rewards(self, is_not_boss_fight=True):
        # utilisation d'une action pour reclamer recompense
        if is_not_boss_fight:
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
                    rewards.append(objet)
            acc += (100 - objet.rarity)
            
        # level up du pokemon
        if self.difficult == 'easy':
            self.player_pk.level_up()
        elif self.difficult == 'normal':
            self.player_pk.level_up(2)
        elif self.difficult == 'hard':
            self.player_pk.level_up(3)
        
        return rewards

    def apply_status_effect(self, pk):
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

        if not self.player_pk.is_alive:
            self.fight_result = 'Defeat'
            self.add_logs((self.player_pk, 'Defeat'))
        elif not self.dresseur.pk.is_alive:
            self.fight_result = 'Victory'
            self.add_logs((self.player_pk, 'Victory'))

    def update_status_effect(self, pk):
        print('Update des effets du pokemon :', pk.name)
        if pk.status["Brulure"]:
            if random.randint(1, 8) == 3:
                pk.status["Brulure"] = False
                print('Effet brulure retiré')

        if pk.status["Poison"]:
            if random.randint(1, 4) == 3:
                pk.status["Poison"] = False
                print('Effet poison retiré')

        if pk.status["Paralysie"]:
            if random.randint(1, 10) == 3:
                pk.status["Paralysie"] = False
                pk.speed = pk.base_speed
                print('Effet paralysie retiré')

        if pk.status["Gel"]:
            if random.randint(1, 5) == 3:
                pk.status["Gel"] = False
                print('Effet gel retiré')

        if pk.status["Sommeil"]:
            if self.sommeil_compteur_tour[pk] == -1:
                self.sommeil_compteur_tour[pk] = 3
            if random.randint(1, 1 + self.sommeil_compteur_tour[pk]) == 1:
                pk.status["Sommeil"] = False
                self.sommeil_compteur_tour[pk] = -1
                print('Effet sommeil retiré')
            else:
                self.sommeil_compteur_tour -= 1

        if pk.status["Confusion"]:
            if self.confusion_compteur_tour[pk] == -1:
                self.confusion_compteur_tour[pk] = 4
            if random.randint(1, 1 + self.confusion_compteur_tour[pk]) == 1:
                pk.status["Confusion"] = False
                self.confusion_compteur_tour[pk] = -1
                print('Effet confusion retiré')
            else:
                self.confusion_compteur_tour -= 1


if __name__ == '__main__':
    pass
