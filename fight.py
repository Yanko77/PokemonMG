import pygame
import random
from dresseur import Alizee, Olea, Ondine, Pierre, Blue, Red, Iris


DRESSEUR_LIST = [Alizee, Olea, Ondine, Pierre, Blue, Red, Iris]


class Fight:

    def __init__(self, game, player_pk, dresseur=None):
        self.game = game
        self.player_pk = player_pk
        self.dresseur = self.init_dresseur(dresseur)(self.game)

        # Chargement des images
        self.path = 'assets/game/panels/fight_panel/'

        self.background = self.img_load('background')

        self.combat_button = self.img_load('combat_button')
        self.combat_button_rect = pygame.Rect(873, 526, 387, 174)

        self.sac_button = self.img_load('sac_button')
        self.sac_button_rect = pygame.Rect(717, 527, 144, 144)

        self.fuite_button = self.img_load('fuite_button')
        self.fuite_button_rect = pygame.Rect(1188, 446, 72, 74)

    def update(self, surface: pygame.surface.Surface, possouris):
        surface.blit(self.background, (0, 0))

        self.update_buttons(surface, possouris)

        # GESTION CURSEUR INTERACTIONS
        if self.is_hovering(possouris):
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def update_buttons(self, surface, possouris):
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

    def is_hovering(self, possouris):
        return (self.sac_button_rect.collidepoint(possouris) or
                self.combat_button_rect.collidepoint(possouris) or
                self.fuite_button_rect.collidepoint(possouris)
                )

    def init_dresseur(self, dresseur):
        if dresseur is None:
            dresseur = random.choice(DRESSEUR_LIST)  # À modifier avec les niveaux de difficultés des dresseurs...

        return dresseur

    def img_load(self, file_name):
        return pygame.image.load(self.path + file_name + '.png')


if __name__ == '__main__':
    pass
