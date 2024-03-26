import pygame
import random

import pokemon
import special_pokemon
import objet


class Dresseur:
    """
    Classe représentant un dresseur (PNJ).
    Un dresseur est défini par:
    - Son nom, str
    - La game dans laquelle il intervient, game.Game
    - Sa classe, str
    - Sa puissance, int
    - La liste de pokémons qu'il peut posséder, list
    - Le pokémon qu'il possède s'il est déjà déterminé, pokemon.Pokemon
    """

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
        """
        Methode qui initialise et/ou détermine le pokémon du dresseur.
        """
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
        """
        Methode qui initialise l'inventaire du dresseur et détermine son contenu.
        """
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
            self.inventory.append(objet.Objet(item_name,self.game, quantite=temp_items[item_name]))
            # print(f'{item_name} added')

    def get_pk_level(self) -> int:
        """
        Methode qui calcul le niveau du pokémon du dresseur.

        Ce niveau est calculé de manière aléatoire dans un intervalle de 2 valeurs entières.

        @out: int => niveau du pokémon.
        """
        min_lv = round((self.game.player.level ** 1.9) * 0.30 + 5)
        max_lv = round((self.game.player.level ** 1.9) * 0.35 + 6)

        r = random.Random()
        r.seed(self.game.round.random_seed)

        return r.randint(min_lv, max_lv)

    def get_infos(self) -> tuple:
        """
        Methode qui retourne les infos du dresseur:
        - Son nom, str
        - Sa classe, str
        - Sa puissance, int
        - Son inventaire, list

        @out: tuple
        """
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
    """
    Classe représentant le dresseur du nom de Alizee.
    """
    def __init__(self, game, pk=None):
        super().__init__('Alizée', game, power=3,
                         pk_lists=[
                             ["Nirondelle"],  # Level 1
                             ['Heledelle'],  # Level 2
                             ['Heledelle', 'Bekipan'],  # Level 3
                             ['Bekipan', 'Airmure'],  # Level 4
                             ["Airmure", 'Corboss'],  # Level 5
                             ['Corboss', "Alizee's Altaria"],  # Level 6
                             ["Alizee's Altaria"]  # Level 7+
                         ],
                         pk=pk)
        self.init_pk()


class Red(Dresseur):
    """
    Classe représentant le dresseur du nom de Red.
    """
    def __init__(self, game, pk=None):
        super().__init__('Red', game, power=4,
                         # pk_lists=["Red's Pikachu", 'Mentali', 'Ronflex', 'Tortank', 'Florizarre', 'Lokhlass',
                         # 'Mackogneur'],
                         pk_lists=[["Pichu"],  # Level 1
                                   ["Red's Pikachu"],  # Level 2
                                   ["Red's Pikachu", "Mentali"],  # Level 3
                                   ["Red's Pikachu", "Lokhlass", "Mentali"],  # Level 4
                                   ["Red's Pikachu", "Lokhlass"],  # Level 5
                                   ["Tortank", "Florizarre", "Mackogneur"],  # Level 6
                                   ["Ronflex", "Tortank", "Florizarre", "Mackogneur"],  # Level 7
                                   ["Ronflex", "Mackogneur"]  # Level 8+
                                   ],
                         pk=pk)
        self.init_pk()


class Blue(Dresseur):
    """
    Classe représentant le dresseur du nom de Blue.
    """

    def __init__(self, game, pk=None):
        super().__init__('Blue', game, power=4,
                         pk_lists=[["Blue's Evoli"],  # Level 1
                                   ["Blue's Evoli", "Roucoups", "Melofee"],  # Level 2
                                   ["Blue's Evoli", "Leviator"],  # Level 3
                                   ["Roucarnage", "Melodelfe"],  # Level 4
                                   ["Roucarnage", "Arcanin"],  # Level 5
                                   ["Dracaufeu", "Alakazam", "Arcanin"],  # Level 6
                                   ["Dracaufeu", "Alakazam", "Arcanin"],  # Level 7
                                   ["Dracaufeu", "Arcanin"]  # Level 8+
                                   ],
                         pk=pk)
        self.init_pk()


class Pierre(Dresseur):
    """
    Classe représentant le dresseur du nom de Pierre.
    """

    def __init__(self, game, pk=None):
        super().__init__('Pierre', game, power=3,
                         # pk_lists=['Onix', 'Racaillou', 'Kabutops', 'Tyranocif', 'Osselait']
                         pk_lists=[["Osselait"],  # Level 1
                                   ["Osselait"],  # Level 2
                                   ["Pierre's Onix", "Osselait"],  # Level 3
                                   ["Pierre's Onix", "Kabutops"],  # Level 4
                                   ["Pierre's Onix", "Kabutops"],  # Level 5
                                   ["Pierre's Onix", "Kabutops"],  # Level 6
                                   ["Pierre's Onix", "Tyranocif"],  # Level 7
                                   ["Tyranocif"]  # Level 8+
                                   ],

                         pk=pk)
        self.init_pk()


class Ondine(Dresseur):
    """
    Classe représentant le dresseur du nom de Ondine.
    """

    def __init__(self, game, pk=None):
        super().__init__('Ondine', game, power=3,
                         # pk_lists=['Stari', 'Staross', 'Psykokwak', 'Leviator', 'Flingouste', 'Gamblast'],
                         pk_lists=[["Stari"],  # Level 1
                                   ["Stari", "Flingouste"],  # Level 2
                                   ["Flingouste", "Psykokwak"],  # Level 3
                                   ["Psykokwak", "Ondine's Staross"],  # Level 4
                                   ["Ondine's Staross", "Leviator"],  # Level 5
                                   ["Ondine's Staross", "Gamblast", "Leviator"],  # Level 6
                                   ["Ondine's Staross", "Gamblast", "Leviator"],  # Level 7
                                   ["Gamblast"]  # Level 8+
                                   ],

                         pk=pk)
        self.init_pk()


class Olea(Dresseur):
    """
    Classe représentant le dresseur du nom de Oléa.
    """

    def __init__(self, game, pk=None):
        super().__init__('Oléa', game, power=2,
                         # pk_lists=['Trousselin', 'Grodoudou', 'Lampignon', 'Mystibule', 'Spododo'],
                         pk_lists=[["Rondoudou"],  # Level 1
                                   ["Olea's Trousselin", "Rondoudou", "Spododo"],  # Level 2
                                   ["Olea's Trousselin", "Grodoudou"],  # Level 3
                                   ["Olea's Trousselin", "Lampignon"],  # Level 4
                                   ["Lampignon"],  # Level 5
                                   ["Lampignon", "Mysdibule"],  # Level 6
                                   ["Mysdibule"],  # Level 7+
                                   ],

                         pk=pk)
        self.init_pk()


class Iris(Dresseur):
    """
    Classe représentant le dresseur du nom de Iris.
    """

    def __init__(self, game, pk=None):
        super().__init__('Iris', game, power=2, pk_lists=['Emolga', 'Griknot', 'Dracolosse', 'Vipélierre'], pk=pk)
        self.init_pk()


def get_dresseur_by_name(name):
    """
    Fonction qui retourne la classe du dresseur à partir de son nom (prise en compte des accents !).

    @in: name, str
    @out: dresseur_class issu de la super-classe Dresseur.
    """
    if name == 'Iris':
        return Iris
    elif name == 'Oléa':
        return Olea
    elif name == 'Ondine':
        return Ondine
    elif name == 'Pierre':
        return Pierre
    elif name == 'Blue':
        return Blue
    elif name == 'Red':
        return Red
    elif name == 'Alizée':
        return Alizee


if __name__ == '__main__':
    pass
