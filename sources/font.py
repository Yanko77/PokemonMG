import pygame
pygame.font.init()


FONT_NAMES = (
    'Oswald-Regular',
    'Impact',
    'Bdeogale',
    'Cheesecake',
    '007 GoldenEye'
)


class Font:

    def __init__(self,
                 font_name: str,
                 font_size: int):
        self.name = font_name
        self.size = font_size

        self._font_render = pygame.font.Font(f"assets/fonts/{self.name}", self.size)

    def render(self, text: str, color: tuple = (255, 255, 255)):
        return self._font_render.render(text, True, color)

