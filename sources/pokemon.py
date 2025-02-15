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
            self.bag = PokemonBag(self, [])

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

    def __init__(self, owner: Pokemon, items_list: list):
        self.owner = owner
        self.items_list = items_list
        
        self.max_capacity = 2
        
    @property
    def is_empty(self):
        return self.count_items() == 0

    def count_items(self) -> int:
        return len(self.items_list)
    
    def add(self, item) -> bool:
        """
        Essaye d'ajouter un objet au sac du pokémon.
        Renvoie True si c'est possible, False sinon
        """
        
        if self.count_items() == self.max_capacity:
            return False
        else:
            self.items_list.append(item)
            return True


class PokemonStats:
    """
    Classe qui gère les statistiques du pokémon
    """

    def __init__(self, stats_dict: dict[str, int]):
        self.max_health = stats_dict['max_health']
        self.health = self.max_health
