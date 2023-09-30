import pygame
import image
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
        if self.difficult == 'easy':
            ...



        return pokemon_name
