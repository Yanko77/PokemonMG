import pygame
import random

import dresseur
import game_infos
import pokemon
from dresseur import Alizee, Olea, Ondine, Pierre, Blue, Red, Iris, Sauvage
from bot_fight_algo import get_npc_action


DRESSEUR_LIST = [Alizee, Olea, Ondine, Pierre, Blue, Red, Iris]


class Fight:

    def __init__(self, game, player_pk, dresseur_class=None, dresseur_pk=None):
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

        # Chargement des fonts
        self.player_pk_name_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 40)
        self.dresseur_pk_name_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 30)
        self.pk_pv_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 25)
        self.attaque_font = pygame.font.Font('assets/fonts/Cheesecake.ttf', 55)
        self.sac_page_font = pygame.font.Font('assets/fonts/Cheesecake.ttf', 65)
        self.item_quantite_font = pygame.font.Font('assets/fonts/Impact.ttf', 30)

        # Pré-chargement des noms des pokemons
        self.player_pk_name = self.player_pk_name_font.render(self.player_pk.name, False, (40, 40, 40))
        self.dresseur_pk_name = self.dresseur_pk_name_font.render(self.dresseur.pk.name,
                                                                  False, (40, 40, 40))

        # Variable relatives aux boutons
        self.current_action = None
        self.attaque_buttons_rects = [
            pygame.Rect(907, 432, 356, 109),
            pygame.Rect(535, 471, 356, 109),
            pygame.Rect(907, 560, 356, 109),
            pygame.Rect(535, 596, 356, 109)
        ]
        self.current_action_rect = pygame.Rect(477, 356, 803, 365)

        # Variables relatives aux actions du tour
        self.current_turn_action = ('NoAction', None)  # ('ITEM', item) ou ('ATTAQUE', attaque)

    def update(self, surface: pygame.surface.Surface, possouris):
        surface.blit(self.background, (0, 0))

        self.update_buttons(surface, possouris)
        self.update_current_action(possouris)
        self.update_pokemons(surface)

        if not self.current_turn_action == ('NoAction', None):
            self.turn(self.current_turn_action, ('ATTAQUE', get_npc_action(self.dresseur.pk, self.player_pk, self.dresseur.pk.attaque_pool)))


        # GESTION CURSEUR INTERACTIONS
        if self.is_hovering(possouris):
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def update_current_action(self, possouris):
        if self.current_action is not None:
            if not self.current_action_rect.collidepoint(possouris):
                self.current_action = None

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

    def sac_item_update(self, surface, possouris, item, i):
        item_icon = pygame.transform.scale(item.icon_image, (90, 90))
        item_rect = self.objet_icon_rects[i]

        # Affichage icone
        surface.blit(item_icon, (item_rect.x + (122 - item_icon.get_width()) / 2, item_rect.y + (122 - item_icon.get_height()) / 2))

        # Affichage quantite
        surface.blit(self.item_quantite_font.render(str(item.quantite), False, (255, 255, 255)),
                     (item_rect.x + 90,
                      item_rect.y + 75))

        # Hovering


    def sac_curseur_update(self, possouris):
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
            return self.sac_action_curseur_rect.collidepoint(possouris) or self.curseur_moving_mode
        else:
            return False

    def left_clic_interactions(self, possouris):  # Quand l'utilisateur utilise le clic gauche
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



        # Si l'action en cours est 'SAC'
        elif self.current_action == 'SAC':
            pass

    def turn(self, player_pk_action, dresseur_pk_action):
        pk1, pk2 = self.get_action_order(player_pk_action, dresseur_pk_action)
        if pk1[1][0] == 'ITEM' and pk1[0].is_alive:
            pk1[0].use_item(pk1[1][1])

        if pk2[1][0] == 'ITEM' and pk2[0].is_alive:
            pk2[0].use_item(pk2[1][1])

        if pk1[1][0] == 'ATTAQUE' and pk1[0].is_alive:
            pk1[0].attaque(pk2[0], pk1[1][1])

        if pk2[1][0] == 'ATTAQUE' and pk2[0].is_alive:
            pk2[0].attaque(pk1[0], pk2[1][1])

        self.current_turn_action = ('NoAction', None)

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


if __name__ == '__main__':
    pass
