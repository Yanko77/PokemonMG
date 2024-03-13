import pygame
import random

import pokemon
import special_pokemon
import objet


class Dresseur:

    def __init__(self, name: str, game, dresseur_type='Classic', power=1, pk_lists=None, pk=None):
        self.game = game
        self.name = name

        if not self.name == 'Sauvage':
            self.icon = pygame.image.load(f'assets/game/dresseur_icons/{self.name}.png')

        self.type = dresseur_type
        self.power = power
        self.fuyable = (self.type != 'Classic')

        self.pk_lists = pk_lists
        self.pk = pk

        # self.icon = pygame.image.load(f'assets/game/fight/dresseur/{self.name}.png')

        self.inventory = []
        self.init_inventory()

    def init_pk(self):
        # Eviter les erreurs de None != []
        if self.pk_lists is None:
            self.pk_lists = []

        # Ne pas faire de random sur la liste si le pokémon est deja renseigné
        if self.pk is None:
            # Affecter un pokémon aléatoire de la liste correspondant au niveau du joueur sinon
            if self.game.player.level < len(self.pk_lists):
                pk_name = random.choice(self.pk_lists[self.game.player.level])
            else:
                pk_name = random.choice(self.pk_lists[-1])

            if pk_name in special_pokemon.SPECIAL_PKS_LIST:
                self.pk = special_pokemon.Pokemon(pk_name, self.get_pk_level(), self.game)
            else:
                self.pk = pokemon.Pokemon(pk_name, self.get_pk_level(), self.game)

    def init_inventory(self):
        temp_items = {}
        if self.type == 'Classic':
            nb_items = random.randint(self.power - 1, self.power + 1)

            for i in range(nb_items):
                item = random.choice(self.game.items_list['Use'])
                if item.name in temp_items.keys():
                    temp_items[item.name] += 1
                else:
                    temp_items[item.name] = 1

        for item_name in temp_items.keys():
            self.inventory.append(objet.Objet(item_name, quantite=temp_items[item_name]))
            # print(f'{item_name} added')

    def get_pk_level(self):
        min_lv = round((self.game.player.level**1.9)*0.30 + 5)
        max_lv = round((self.game.player.level**1.9)*0.35 + 6)

        r = random.Random()
        r.seed(self.game.round.random_seed)

        return r.randint(min_lv, max_lv)

    def get_infos(self):
        return self.name, self.type, self.power, self.inventory


# LISTE DRESSEURS :
'''
Iris 2
Oléa 2
Ondine 3
Pierre 3
Blue 4
Red 4
Alizée 3
Chrys 2
Tili 2
Alyxia 3
Margie 2
Leon 4
Cynthia 4
Lance 2
Alain 4
Barbara 2
Guzma 3 
Kiawe 2

TEMPLATE :

class Name(Dresseur):

    def __init__(self, game):
        super().__init__('', game, power=2)
        self.pokemons_list = ['', '', '', '']

'''


class Sauvage(Dresseur):

    def __init__(self, game, pk):
        super().__init__('Sauvage', game, dresseur_type='Sauvage', pk=pk)
        self.init_pk()


class Alizee(Dresseur):

    def __init__(self, game, pk=None):
        super().__init__('Alizée', game, power=3,
                         pk_lists=[
                             ["Alizee's Altaria"],  # Level 1
                             ["Alizee's Altaria", 'Heledelle'],  # Level 2
                             ["Alizee's Altaria", 'Airmure'],  # Level 3
                             ["Alizee's Altaria", 'Bekipan'],  # Level 4
                             ["Alizee's Altaria", 'Corboss'],  # Level 5
                             ["Alizee's Altaria"]  # Level 6+
                         ],
                         pk=pk)
        self.init_pk()

class Red(Dresseur):

    def __init__(self, game, pk=None):
        super().__init__('Red', game, power=4,
                         pk_lists=['Pikachu', 'Mentali', 'Ronflex', 'Tortank', 'Florizarre', 'Lokhlass', 'Mackogneur'], pk=pk)


class Blue(Dresseur):

    def __init__(self, game, pk=None):
        super().__init__('Blue', game, power=4,
                         pk_lists=[["Blue's Evoli"],  # Level 1
                                   ["Blue's Evoli", "Roucarnage", "Melodelfe"],  # Level 2
                                   ["Blue's Evoli", "Roucarnage", "Leviator"],  # Level 3
                                   ["Blue's Evoli", "Roucarnage", "Arcanin"],  # Level 4
                                   ["Blue's Evoli", "Roucarnage", "Alakazam"],  # Level 5
                                   ["Blue's Evoli", "Dracaufeu"]  # Level 6+
                                   ],
                         pk=pk)
        self.init_pk()


class Pierre(Dresseur):

    def __init__(self, game, pk=None):
        super().__init__('Pierre', game, power=3, pk_lists=['Onix', 'Racaillou', 'Kabutops', 'Tyranocif', 'Osselait'], pk=pk)
        self.init_pk()


class Ondine(Dresseur):

    def __init__(self, game, pk=None):
        super().__init__('Ondine', game, power=3, pk_lists=['Stari', 'Staross', 'Psykokwak', 'Léviator', 'Flingouste'], pk=pk)
        self.init_pk()


class Olea(Dresseur):

    def __init__(self, game, pk=None):
        super().__init__('Oléa', game, power=2,
                         pk_lists=['Trousselin', 'Grodoudou', 'Granbull', 'Lampignon', 'Mystibule'],
                         pk=pk)
        self.init_pk()


class Iris(Dresseur):

    def __init__(self, game, pk=None):
        super().__init__('Iris', game, power=2, pk_lists=['Emolga', 'Griknot', 'Dracolosse', 'Vipélierre'], pk=pk)
        self.init_pk()


if __name__ == '__main__':
    pass
