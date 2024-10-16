import pygame
pygame.font.init()


FONT_NAMES = (
    'Oswald-Regular',
    'Impact',
    'Bdeogale',
    'Cheesecake',
    '007 GoldenEye'
)

FONT_IDs = {
    'Oswald-Regular': 1,
    'Impact': 2,
    'Bdeogale': 3,
    'Cheesecake': 4,
    '007 GoldenEye': 5
}


class Font:

    def __init__(self,
                 font_name: str,
                 font_size: int):

        assert font_size < 10000, "Font size must be less than 10000"

        self.name = font_name
        self.size = font_size

        self._font_render = pygame.font.Font(f"assets/fonts/{self.name}.ttf", self.size)

    @property
    def id(self):
        return FONT_IDs[self.name] * 10000 + self.size

    def render(self, text: str, color: tuple = (255, 255, 255)):
        return self._font_render.render(text, True, color)

