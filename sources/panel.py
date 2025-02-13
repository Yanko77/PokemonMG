"""
Cleaning effectué
"""

import pygame

import game as g


class Panel:

    def __init__(self, game, path: str, prio: int = 0):
        self.game: g.Game = game

        self.prio = prio  # Priorité d'affichage
        self._components = []  # Composants du panel

        self.PATH = path

    @property
    def components(self):
        return self._components

    def set_components(self, comp_list):
        """
        All components in 'comp_list' must have an attribute 'prio'
        """
        self._components = comp_list
        self.sort_components_by_prio()

    def set_component_prio(self, comp, value):
        comp.prio = value
        self.sort_components_by_prio()

    def sort_components_by_prio(self):
        """
        Trie la liste self._components en fonction de la priorité des composants.
        """
        self._components.sort(key=lambda comp: comp.prio)

    def update(self, possouris):
        pass

    def left_clic_interactions(self, possouris):
        """
        Transmet l'information du clic au composant sur lequel on clique.

        :return: True si un composant a réagi, False sinon.
        """
        for comp in self.components[::-1]:
            print(repr(comp))
            if hasattr(comp, 'is_hovering') and comp.is_hovering(possouris):
                if hasattr(comp, 'left_clic_interactions'):
                    comp.left_clic_interactions(possouris)
                return True

        return False

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

        :path: chemin d'accès du fichier depuis self.PATH
        """
        return pygame.image.load(f'{self.PATH}{path}.png').convert_alpha()
