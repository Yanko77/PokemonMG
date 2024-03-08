import random

import fight
from fight import DRESSEUR_LIST


class Round:

    def __init__(self, game):
        self.game = game
        self.num = 0

        self.random_seed = None
        self.set_new_random_seed()

        self.all_current_game_seeds = [self.random_seed]

    def next(self):
        self.num += 1
        self.set_new_random_seed()
        self.all_current_game_seeds.append(self.random_seed)

    def set_new_random_seed(self, seed=None):
        if seed is None:
            self.random_seed = self.generate_round_random_seed()
        else:
            self.random_seed = seed

    def get_random_seed(self):
        return self.random_seed

    def generate_round_random_seed(self):
        return int(str(random.randint(0, 255))
                               + str(random.randint(0, 255))
                               + str(random.randint(0, 255))
                               + str(random.randint(0, 255)))
