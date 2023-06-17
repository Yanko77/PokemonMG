import pygame
import image



class Game:
    def __init__(self):
        self.is_playing = False

        self.background = image.Background()
        self.a = pygame.image.load('assets/accueil/animation/Background/1.png')

    def update(self, screen):

        if self.is_playing:
            ...
        else:
            screen.blit(self.background.image, (0, 0))
            self.background.update_animation()
