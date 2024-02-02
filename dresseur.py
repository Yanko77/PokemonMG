import pygame
import random

import pokemon
import objet


class Dresseur:

    def __init__(self, name: str, pokemon, game, dresseur_type='Classic', power=1):
        self.game = game
        self.name = name
        self.pokemon = pokemon

        self.type = dresseur_type
        self.power = power

        # self.icon = pygame.image.load(f'assets/game/fight/dresseur/{self.name}.png')
        self.inventory = []
        self.init_inventory()

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
            print(f'{item_name} added')


if __name__ == '__main__':
    import game
    g = game.Game()
    d = Dresseur('Yanko', pokemon.Pokemon('Dracaufeu', 10, g.player), g)
    print([(item.name, item.quantite) for item in d.inventory])
