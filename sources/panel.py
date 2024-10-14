"""
Cleaning effectué
"""

import pygame


class Panel:

    def __init__(self, game, path):
        self.game = game

        self.PATH = path

    def update(self, possouris):
        pass

    def left_clic_interactions(self, possouris):
        pass

    def is_hovering_buttons(self, possouris):
        return False

    def create_rect_alpha(self, dimensions, color, alpha=90):
        rect = pygame.Surface(dimensions)
        rect.set_alpha(alpha)
        rect.fill(color)
        return rect

    def img_load(self, path: str) -> pygame.Surface:
        """
        Methode de chargement d'image dépendant du chemin d'accès (self.PATH, une constante).
        Retourne une surface pygame.
        @in : path, str → chemin d'accès du fichier depuis self.PATH
        """
        return pygame.image.load(f'{self.PATH}{path}.png').convert_alpha()
