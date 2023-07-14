import pygame


class Objet:

    def __init__(self, name):
        self.name = name[0].upper() + name[1:].lower()
        self.icon_image = pygame.image.load(f'assets/items/{self.name}.png')

        # self.classes = classes_list