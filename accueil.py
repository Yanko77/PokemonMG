import pygame
import image


class Accueil:

    def __init__(self):
        self.background = image.Background()
        self.game_bar = image.GameBar()
        self.carchakrok = image.Carchakrok()

    def update(self, surface):
        surface.blit(self.background.image, (0, 0))
        self.background.update_animation()
        if self.background.is_animation_over:
            surface.blit(self.game_bar.image, (0, 0))
            self.game_bar.update_animation()
            if self.game_bar.is_animation_over:
                surface.blit(self.carchakrok.image, (self.carchakrok.rect.x, self.carchakrok.rect.y))
                self.carchakrok.update_animation()