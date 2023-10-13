import pygame
import image
import random
import pokemon


class TrainPanel:

    def __init__(self, game):
        self.game = game
        # LOADING IMAGES --------------------------
        self.background = image.load_image('assets/game/ingame_windows/Train/background.png')

        # DEFAULT VARIABLES --------------------------
        self.difficult = None
        self.training_pk = None

    def update(self, surface, possouris, window_pos):
        surface.blit(self.background, (window_pos[0], window_pos[1]))

    def set_difficult(self, diff_value='easy'):
        self.difficult = diff_value

    def get_spawn_train_pk(self):
        pokemon_name = None
        if self.difficult == 'easy':
            all_possible = pokemon.get_all_diff_pokemons(2)
            if all_possible is None:
                all_possible = pokemon.get_all_diff_pokemons(1)
            pokemon_name = all_possible[random.randint(0, len(all_possible))]

        elif self.difficult == 'normal':
            all_possible = pokemon.get_all_diff_pokemons(1)
            pokemon_name = all_possible[random.randint(0, len(all_possible))]

        elif self.difficult == 'hard':
            all_possible = pokemon.get_all_diff_pokemons(0.5)
            pokemon_name = all_possible[random.randint(0, len(all_possible))]

        return pokemon_name

    def spawn_train_pk(self):
        if self.difficult == 'easy':
            self.train_pk = pokemon.Pokemon(self.get_spawn_train_pk(), self.training_pk.level - 1)
        elif self.difficult == 'normal':
            self.train_pk = pokemon.Pokemon(self.get_spawn_train_pk(), self.training_pk.level)
        elif self.difficult == 'hard':
            self.train_pk = pokemon.Pokemon(self.get_spawn_train_pk(), self.training_pk.level + 1)

    def algo_temporaire_combat_simulation(self): # a suprimer aprés mais comme t'es pas la c'est ma propose d'algo de combat
        self.spawn_train_pk()
        while self.training_pk.is_alive and self.train_pk.is_alive:
            if self.training_pk.speed > self.train_pk.speed:
                self.train_pk.damage(self.training_pk.attack / 10)
                self.training_pk.domage(self.training_pk.attack / 10)
            else:
                self.training_pk.domage(self.training_pk.attack / 10)
                self.train_pk.damage(self.training_pk.attack / 10)

        self.training_pk.health, self.training_pk.is_alive = self.train_pk.pv, True
        if self.train_pk.is_alive:
            return False # ou se que tu veut pour dire qu'il a perdu
        else:
            return True # ou se que tu veut pour dire qu'il a gagné





if __name__ == "__main__":
    t = TrainPanel
    # j'ai voulue faire des teste mais il manqué certaine partie du programme dont je ne sais pas utilier
    # ps si ta lue suprime les commentaire
