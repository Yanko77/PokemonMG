import pygame
import random

import pokemon
import objet


class Dresseur:

    def __init__(self, name: str, game, dresseur_type='Classic', power=1, pk_list=None, pk=None):
        self.game = game
        self.name = name

        self.type = dresseur_type
        self.power = power
        self.fuyable = (self.type != 'Classic')

        self.pk = self.init_pk(pk, pk_list)

        # self.icon = pygame.image.load(f'assets/game/fight/dresseur/{self.name}.png')

        self.inventory = []
        self.init_inventory()

    def init_pk(self, pk, pk_list):
        # Eviter les erreurs de None != []
        if pk_list is None:
            pk_list = []

        # Renvoyer le pokemon si renseigné, un random de la liste sinon
        if pk is not None:
            return pk
        else:
            return random.choice(pk_list)

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


class Alizee(Dresseur):

    def __init__(self, game):
        super().__init__('Alizée', game, power=3, pk_list=['Hélédelle', 'Altaria', 'Airmure', 'Bekipan', 'Corboss'])


class Red(Dresseur):

    def __init__(self, game):
        super().__init__('Red', game, power=4, pk_list=['Pikachu', 'Mentali', 'Ronflex', 'Tortank', 'Florizarre', 'Lokhlass', 'Mackogneur'])


class Blue(Dresseur):

    def __init__(self, game):
        super().__init__('Blue', game, power=4, pk_list=['Evoli (stat hyper hautes)', 'Roucarnage', 'Leviator', 'Arcanin', 'Alakazam', 'Dracaufeu', 'Melodelfe'])


class Pierre(Dresseur):

    def __init__(self, game):
        super().__init__('Pierre', game, power=3, pk_list=['Onix', 'Racaillou', 'Kabutops', 'Tyranocif', 'Osselait'])


class Ondine(Dresseur):

    def __init__(self, game):
        super().__init__('Ondine', game, power=3, pk_list=['Stari', 'Staross', 'Psykokwak', 'Léviator', 'Flingouste'])


class Olea(Dresseur):

    def __init__(self, game):
        super().__init__('Oléa', game, power=2, pk_list=['Trousselin', 'Grodoudou', 'Granbull', 'Lampignon', 'Mystibule'])


class Iris(Dresseur):

    def __init__(self, game):
        super().__init__('Iris', game, power=2, pk_list=['Emolga', 'Griknot', 'Dracolosse', 'Vipélierre'])


if __name__ == '__main__':
    pass
