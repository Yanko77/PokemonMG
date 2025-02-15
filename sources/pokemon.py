import pygame

import sources.types as types


class Pokemon:

    def __init__(self,
                 name: str,
                 level: int,
                 game,
                 is_shiny=False,
                 items=None):

        self.name = name
        self.id = ...

        self.level = level

        self.types: tuple[types.Type, types.Type | None] = (types.NORMAL, types.SPECTR)  # TODO

        self.stats = PokemonStats({'max_health': 50})  # TODO

        if items is None:
            self.items = PokemonBag(self)

        self.icon = pygame.image.load(f'assets/icons/pokemons/{self.name}.png') \
            .convert_alpha() \
            .subsurface((0, 0, 64, 64))

    def get_icon(self, size=(64, 64)) -> pygame.Surface:
        return pygame.transform.scale(self.icon, size)

    def __repr__(self):
        return f'{self.name} Lv.{self.level}'


class PokemonBag:
    """
    Classe qui gère tout ce qui concerne les objets portés par le pokémon.
    """

    def __init__(self, items_list):
        self.items_list = items_list


class PokemonStats:
    """
    Classe qui gère les statistiques du pokémon
    """

    def __init__(self, stats_dict: dict[str, int]):
        self.max_health = stats_dict['max_health']
        self.health = self.max_health
