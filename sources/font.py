import pygame
pygame.font.init()


class Font:

    MAX_LOADED_FONT = 50

    def __init__(self,
                 font_name: str,
                 font_size: int):

        assert font_size < 10000, "Font size must be less than 10000"

        self.name = font_name
        self.size = font_size

        self._font_renderer = pygame.font.Font(f"assets/fonts/{self.name}.ttf", self.size)

        self.loaded_renders = {}

    def render(self, text: str, color: tuple = (255, 255, 255), load_mode=True):
        """
        Passer le 'load_mode' à False si le texte à afficher est temporaire (ne sera pas ré-affiché plus tard)
        """

        if (text, color) in self.loaded_renders:
            return self.loaded_renders[(text, color)]
        else:
            render = self._font_renderer.render(text, True, color).convert_alpha()

            if load_mode:
                self.loaded_renders[(text, color)] = render

            return render


# Game's fonts list

OSWALD30 = Font('Oswald-Regular', 30)
OSWALD25 = Font('Oswald-Regular', 25)
OSWALD18 = Font('Oswald-Regular', 18)
OSWALD15 = Font('Oswald-Regular', 15)
IMPACT50 = Font('Impact', 50)
