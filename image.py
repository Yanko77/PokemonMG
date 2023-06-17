import pygame
import animation

class Image(animation.AnimateImage):

    def __init__(self, nb_images, image_name):
        super().__init__(nb_images, image_name)

    def update_animation(self):
        self.animate(loop=False, final_image_num=23)


class Background(Image):

    def __init__(self):
        super().__init__(24, "Background")
        self.start_animation()