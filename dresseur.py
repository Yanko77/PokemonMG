import pygame
import random


class Dresseur:

    def __init__(self, name: str, pokemon, dresseur_type='Classic', power=1):
        self.name = name
        self.pokemon = pokemon

        self.type = dresseur_type
        self.power = power

        self.icon = pygame.image.load('assets/game/fight/dresseur/{self.name}.png')
        self.inventory = []

    def init_inventory(self):
        if self.type == 'Classic':
            nb_items = random.randint(self.power - 1, self.power + 1)
