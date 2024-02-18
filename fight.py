import pygame
import random

import dresseur
import pokemon
from dresseur import Alizee, Olea, Ondine, Pierre, Blue, Red, Iris, Sauvage


DRESSEUR_LIST = [Alizee, Olea, Ondine, Pierre, Blue, Red, Iris]


class Fight:

    def __init__(self, game, player_pk, dresseur_class=None, dresseur_pk=None):
        self.game = game
        self.player_pk = player_pk
        # self.dresseur = self.init_dresseur(dresseur_class)(self.game)
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

        # Chargement des fonts
        self.player_pk_name_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 40)
        self.dresseur_pk_name_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 30)
        self.pk_pv_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 25)

        # Pré-chargement des noms des pokemons
        self.player_pk_name = self.player_pk_name_font.render(self.player_pk.name, False, (40, 40, 40))
        self.dresseur_pk_name = self.dresseur_pk_name_font.render(self.dresseur.pk.name,
                                                                  False, (40, 40, 40))

        # Variable relatives aux boutons
        self.current_action = None

    def update(self, surface: pygame.surface.Surface, possouris):
        surface.blit(self.background, (0, 0))

        self.update_buttons(surface, possouris)

        self.update_pokemons(surface)

        # GESTION CURSEUR INTERACTIONS
        if self.is_hovering(possouris):
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

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
            pass

        # Si l'action en cours est 'SAC'
        elif self.current_action == 'SAC':
            pass

    def is_hovering(self, possouris):
        return (self.sac_button_rect.collidepoint(possouris) or
                self.combat_button_rect.collidepoint(possouris) or
                self.fuite_button_rect.collidepoint(possouris)
                )

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
            pass

        # Si l'action en cours est 'SAC'
        elif self.current_action == 'SAC':
            pass

    def init_dresseur(self, dresseur_class, dresseur_pk=None):
        if dresseur_class is None:
            dresseur_class = random.choice(DRESSEUR_LIST)  # À modifier avec les niveaux de difficultés des dresseurs...

        return dresseur_class(self.game, pk=dresseur_pk)

    def img_load(self, file_name):
        return pygame.image.load(self.path + file_name + '.png')


if __name__ == '__main__':
    pass
