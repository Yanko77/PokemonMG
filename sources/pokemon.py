import pygame


class Pokemon:

    def __init__(self,
                 name: str,
                 level: int,
                 game,
                 is_shiny=False,
                 items=None):

        self.name = name
        self.id = ...

        if items is None:
            self.items = PokemonBag(self)

        self.icon = pygame.image.load(f'assets/icons/pokemons/{self.name}.png') \
            .convert_alpha() \
            .subsurface((0, 0, 64, 64))

    def get_icon(self, size=(64, 64)) -> pygame.Surface:
        return pygame.transform.scale(self.icon, size)


class PokemonBag:
    """
    Classe qui gère tout ce qui concerne les objets portés par le pokémon.
    """

    def __init__(self, items_list):
        self.items_list = items_list
