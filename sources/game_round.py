"""
Fichier gérant les tours de jeu.
"""

# Importation des modules
import random

# Définition des classes


class Round:
    """
    Classe représentant le tour de jeu.
    """

    def __init__(self, game):
        self.game = game
        self.num = 0

        self.random_seed = None
        self.set_new_random_seed()

        self.all_current_game_seeds = [self.random_seed]

    def next(self):
        """
        Méthode permettant de passer au tour de jeu suivant.
        """
        self.num += 1
        self.set_new_random_seed()
        self.all_current_game_seeds.append(self.random_seed)

    def set_new_random_seed(self, seed=None):
        """
        Méthode qui détermine la nouvelle seed aléatoire.
        """
        if seed is None:
            self.random_seed = self.generate_round_random_seed()
        else:
            self.random_seed = seed

    def get_random_seed(self) -> int:
        return self.random_seed

    def generate_round_random_seed(self) -> int:
        """
        Méthode de génération de seed aléatoire.
        @out: int
        """
        return int(str(random.randint(0, 255))
                               + str(random.randint(0, 255))
                               + str(random.randint(0, 255))
                               + str(random.randint(0, 255)))
