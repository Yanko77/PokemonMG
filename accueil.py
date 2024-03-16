import pygame


class Accueil:

    def __init__(self, game):
        self.game = game
        self.PATH = 'assets/accueil/'

        # INTRO
        self.intro = True
        self.intro_compteur = -150

        self.logo = self.img_load('intro/logo').convert_alpha()

        # HOME SCREEN
        self.jouer = False
        self.parametres = False
        self.credits = False
        self.home_screen_fade = True
        self.home_screen_compteur = -255

        self.background = self.img_load('home_screen/background')

        self.jouer_button = self.img_load('home_screen/buttons/jouer')
        self.jouer_button_h = self.img_load('home_screen/buttons/jouer_')

        self.parametres_button = self.img_load('home_screen/buttons/parametres')
        self.parametres_button_h = self.img_load('home_screen/buttons/parametres_')

        self.credits_button = self.img_load('home_screen/buttons/credits')
        self.credits_button_h = self.img_load('home_screen/buttons/credits_')

        self.quitter_button = self.img_load('home_screen/buttons/quitter')
        self.quitter_button_h = self.img_load('home_screen/buttons/quitter_')

        self.new_game_button = self.img_load('home_screen/buttons/new_game')
        self.new_game_button_h = self.img_load('home_screen/buttons/new_game_')

        self.load_game_button = self.img_load('home_screen/buttons/load_game')
        self.load_game_button_h = self.img_load('home_screen/buttons/load_game_')

        self.buttons_rect = [
            pygame.Rect(472, 293, 340, 56),
            pygame.Rect(472, 379, 340, 56),
            pygame.Rect(472, 465, 340, 56),
            pygame.Rect(472, 551, 340, 56)
        ]
        self.buttons = []

    def update(self, surface, possouris):
        if self.intro:
            self.update_intro(surface)
        else:
            self.update_home_screen(surface, possouris)

        if self.is_hovering_buttons(possouris):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def update_intro(self, surface):
        """
        Methode qui gère l'affichage de l'intro du lancement du jeu
        """
        if self.intro_compteur > 0:
            surface.fill((0, 0, 0))

            if self.intro_compteur < 254:
                self.logo.set_alpha(self.intro_compteur)
            elif 700 > self.intro_compteur > 300:
                self.logo.set_alpha(555 - self.intro_compteur)
            elif self.intro_compteur >= 699:
                self.intro = False

            y = 200 - self.intro_compteur
            if y < 0:
                y = 0

            surface.blit(self.logo, (0, y))

        self.intro_compteur += 1

    def update_home_screen(self, surface, possouris):
        surface.fill((0, 0, 0))

        if self.home_screen_fade:
            if 255 + self.home_screen_compteur < 255:
                self.background.set_alpha(255 + self.home_screen_compteur)
            else:
                self.home_screen_fade = False

        surface.blit(self.background, (0, 0))

        if self.jouer:
            self.buttons = [
                (self.new_game_button, self.new_game_button_h, 'new_game'),
                (self.load_game_button, self.load_game_button_h, 'load_game'),
            ]
        elif self.parametres:
            self.buttons = [
            ]
        elif self.credits:
            self.buttons = [
            ]
        else:
            self.buttons = [
                (self.jouer_button, self.jouer_button_h, 'jouer'),
                (self.parametres_button, self.parametres_button_h, 'parametres'),
                (self.credits_button, self.credits_button_h, 'credits'),
                (self.quitter_button, self.quitter_button_h, 'quitter'),
            ]

        # Affichage des boutons
        i = 0
        for button in self.buttons:
            y = self.buttons_rect[i].y

            if self.home_screen_compteur < 40:
                y += 40 - self.home_screen_compteur

            if self.home_screen_compteur < 55:
                button[0].set_alpha(self.home_screen_compteur*5)

            if self.buttons_rect[i].collidepoint(possouris) and self.home_screen_compteur > 55:
                surface.blit(button[1], (self.buttons_rect[i].x, y))
            else:
                surface.blit(button[0], (self.buttons_rect[i].x, y))

            i += 1

        if self.home_screen_compteur < 55:
            self.home_screen_compteur += 1.5

    def clic(self, button_name: str):
        if button_name == 'jouer':
            self.jouer = True
        elif button_name == 'parametres':
            self.parametres = True
        elif button_name == 'credits':
            self.credits = True
        elif button_name == 'quitter':
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif button_name == 'new_game':
            self.game.start_new_game()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        elif button_name == 'load_game':
            pass
        else:
            self.jouer = False
            self.parametres = False
            self.credits = False

    def left_clic_interactions(self, possouris):
        if self.home_screen_compteur > 55:
            i = 0
            for button in self.buttons:
                if self.buttons_rect[i].collidepoint(possouris):
                    self.clic(button[2])
                i += 1

    def is_hovering_buttons(self, possouris):
        if self.home_screen_compteur > 55:
            i = 0
            for rect in self.buttons_rect:
                if i < len(self.buttons):
                    if rect.collidepoint(possouris):
                        return True
                i += 1

            return False
        return False

    def img_load(self, path):
        return pygame.image.load(f'{self.PATH}{path}.png')


if __name__ == '__main__':
    FPS = 144
    screen = pygame.display.set_mode((1280, 720))
    icon = pygame.image.load("assets/icon.png")
    pygame.display.set_caption("PMG || Pokemon Management Game")
    pygame.display.set_icon(icon)

    accueil = Accueil(None)
    clock = pygame.time.Clock()

    running = True

    while running:
        posSouris = list(pygame.mouse.get_pos())

        accueil.update(screen, posSouris)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONUP:
                accueil.left_clic_interactions(posSouris)

        clock.tick(FPS)

pygame.quit()