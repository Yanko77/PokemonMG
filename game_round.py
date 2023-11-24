import random


class Round:

    def __init__(self):
        self.num = 0
        self.random_seed = random.random()
        self.all_current_game_seeds = [self.random_seed]

    def next(self):
        self.num += 1
        self.random_seed = random.random()
        self.all_current_game_seeds.append(self.random_seed)