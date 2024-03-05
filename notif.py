import pygame


class Notif:

    def __init__(self):
        self.font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 40)

        self.color = (0, 0, 0)
        self.text = self.font.render("", False, self.color).convert_alpha()

        self.rect = pygame.Surface(self.text.get_size(), pygame.SRCALPHA).convert_alpha()
        self.rect_pos = (0, 0)

        self.is_animating = False
        self.compteur = 0

    def update(self, surface):
        if self.is_animating:
            if self.compteur > 0:
                alpha = ((self.compteur - 20) * (self.compteur - 80) * -1.02)/2
                if alpha < 0:
                    alpha = 0
                elif alpha > 255:
                    alpha = 255

                self.rect.set_alpha(round(alpha) - 60)
                pygame.draw.rect(self.rect, (255, 255, 255), self.rect.get_rect())

                self.text.set_alpha(round(alpha))

                surface.blit(self.rect, self.rect_pos)
                surface.blit(self.text, self.rect_pos)

                self.compteur -= 0.8
            else:
                self.is_animating = False

    def new_notif(self, text, color):
        self.color = color
        self.text = self.font.render(f" {text} ", False, self.color)

        self.rect = pygame.Surface(self.text.get_size(), pygame.SRCALPHA).convert_alpha()
        self.rect_pos = (1280 - self.rect.get_width() - 5, 5)

        self.start_animation()

    def start_animation(self):
        self.compteur = 82
        self.is_animating = True

    def create_rect_alpha(self, dimensions, color, alpha=90):
        rect = pygame.Surface(dimensions)
        rect.set_alpha(alpha)
        rect.fill(color)
        return rect