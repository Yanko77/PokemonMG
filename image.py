import pygame
import animation


class Image(animation.AnimateImage):

    def __init__(self, nb_images, image_name):
        super().__init__(nb_images, image_name)
        self.final_image_num = nb_images - 1
        self.loop = False
        self.pas = 1


    def update_animation(self):
        self.animate(loop=self.loop, final_image_num=self.final_image_num, pas=self.pas)


class Background(Image):

    def __init__(self):
        super().__init__(24, "Background")
        self.pas = 2
        self.start_animation()


class GameBar(Image):

    def __init__(self):
        super().__init__(10, 'game_bar')
        self.start_animation()


class Carchakrok:

    def __init__(self):
        self.image = pygame.image.load('assets/accueil/carchakrok.png')
        self.rect = self.image.get_rect()
        self.rect.x = 1000
        self.rect.y = 0

    def update_animation(self):
        if self.rect.x > 0:
            self.rect.x -= 50