import pygame
import random
from dresseur import Alizee, Olea, Ondine, Pierre, Blue, Red, Iris


DRESSEUR_LIST = [Alizee, Olea, Ondine, Pierre, Blue, Red, Iris]


class Fight:

    def __init__(self, game, player_pk, dresseur=None):
        self.game = game
        self.player_pk = player_pk
        self.dresseur = self.init_dresseur(dresseur)(self.game)

    def update(self, surface:pygame.surface.Surface, possouris):
        surface.fill((0, 0, 0))

    def init_dresseur(self, dresseur):
        if dresseur is None:
            dresseur = random.choice(DRESSEUR_LIST)

        return dresseur


if __name__ == '__main__':
    pass
