import pygame
import animation
import random


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
        super().__init__(24, 'game_bar')
        self.start_animation()


class RandomPokemon:

    def __init__(self):
        self.is_animation_over = False
        self.after_animation_over_compteur = 0

        self.num = random.randint(0, 8)
        self.image = pygame.image.load(f'assets/accueil/pokemons/{self.num}.png')
        self.image.set_alpha(0)

        self.image_opacity = 0

    def update_animation(self):
        self.image.set_alpha(self.image_opacity)
        if self.image_opacity < 255:
            self.image_opacity += 10
        else:
            if not self.is_animation_over:
                self.after_animation_over_compteur += 1
            if self.after_animation_over_compteur > 20:
                self.is_animation_over = True


class IntroAccueil(Image):

    def __init__(self):
        super().__init__(147, 'intro')
        self.start_animation()
        self.pas = 2


class AccueilButtons:

    def __init__(self):
        self.start_game = pygame.image.load('assets/accueil/Buttons/Start_game/start_game.png')
        self.start_game_rect = self.start_game.get_rect()
        self.start_game_rect.x = 30
        self.start_game_rect.y = 155
        self.start_game_h = pygame.image.load('assets/accueil/Buttons/Start_game/start_game_hover.png')

        self.settings = pygame.image.load('assets/accueil/Buttons/Settings/settings.png')
        self.settings = pygame.transform.scale(self.settings, (422, 83))
        self.settings_rect = self.settings.get_rect()
        self.settings_rect.x = 30
        self.settings_rect.y = 280
        self.settings_h = pygame.image.load('assets/accueil/Buttons/Settings/settings_hover.png')
        self.settings_h = pygame.transform.scale(self.settings_h, (422, 83))

        self.credits = pygame.image.load('assets/accueil/Buttons/Credits/credits.png')
        self.credits = pygame.transform.scale(self.credits, (359, 83))
        self.credits_rect = self.settings.get_rect()
        self.credits_rect.x = 30
        self.credits_rect.y = 390
        self.credits_h = pygame.image.load('assets/accueil/Buttons/Credits/credits_hover.png')
        self.credits_h = pygame.transform.scale(self.credits_h, (359, 83))

        self.quit = pygame.image.load('assets/accueil/Buttons/Quit/quit.png')
        self.quit = pygame.transform.scale(self.quit, (213, 91))
        self.quit_rect = self.quit.get_rect()
        self.quit_rect.x = 30
        self.quit_rect.y = 500

        self.quit_h = pygame.image.load('assets/accueil/Buttons/Quit/quit_hover.png')
        self.quit_h = pygame.transform.scale(self.quit_h, (213, 91))

    def update(self, surface, possouris, basic_accueil:bool):
        if self.start_game_rect.collidepoint(possouris) and basic_accueil:
            surface.blit(self.start_game_h, self.start_game_rect)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            surface.blit(self.start_game, self.start_game_rect)

        if self.settings_rect.collidepoint(possouris) and basic_accueil:
            surface.blit(self.settings_h, self.settings_rect)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            surface.blit(self.settings, self.settings_rect)

        if self.credits_rect.collidepoint(possouris) and basic_accueil:
            surface.blit(self.credits_h, self.credits_rect)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            surface.blit(self.credits, self.credits_rect)

        if self.quit_rect.collidepoint(possouris) and basic_accueil:
            surface.blit(self.quit_h, self.quit_rect)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            surface.blit(self.quit, self.quit_rect)

        if basic_accueil:
            if not (self.quit_rect.collidepoint(possouris) or self.start_game_rect.collidepoint(possouris) or
                    self.credits_rect.collidepoint(possouris) or self.settings_rect.collidepoint(possouris)):

                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


class StartGamePanel:

    def __init__(self):
        self.panel = pygame.image.load('assets/accueil/panels/start_game/panel.png')

        self.new_game_button = pygame.image.load('assets/accueil/panels/start_game/new_game_button.png')
        self.new_game_button_rect = self.new_game_button.get_rect()
        self.new_game_button_rect.x = 791
        self.new_game_button_rect.y = 508
        self.new_game_button_h = pygame.image.load('assets/accueil/panels/start_game/new_game_button_hover.png')

        self.load_game_button = pygame.image.load('assets/accueil/panels/start_game/load_game_button.png')
        self.load_game_button_rect = self.load_game_button.get_rect()
        self.load_game_button_rect.x = 130
        self.load_game_button_rect.y = 508
        self.load_game_button_h = pygame.image.load('assets/accueil/panels/start_game/load_game_button_hover.png')

        self.x_button = pygame.image.load('assets/accueil/panels/start_game/x_button.png')
        self.x_button_rect = self.x_button.get_rect()
        self.x_button_rect.x = 1144
        self.x_button_rect.y = 68
        self.x_button_h = pygame.image.load('assets/accueil/panels/start_game/x_button_hover.png')

    def update(self, surface, possouris, basic_accueil):
        surface.blit(self.panel, (0, 0))

        if self.new_game_button_rect.collidepoint(possouris) and not basic_accueil:
            surface.blit(self.new_game_button_h, self.new_game_button_rect)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            surface.blit(self.new_game_button, self.new_game_button_rect)

        if self.load_game_button_rect.collidepoint(possouris) and not basic_accueil:
            surface.blit(self.load_game_button_h, self.load_game_button_rect)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            surface.blit(self.load_game_button, self.load_game_button_rect)

        if self.x_button_rect.collidepoint(possouris) and not basic_accueil:
            surface.blit(self.x_button_h, self.x_button_rect)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            surface.blit(self.x_button, self.x_button_rect)

        if not (self.x_button_rect.collidepoint(possouris) or self.new_game_button_rect.collidepoint(possouris)
                or self.load_game_button_rect.collidepoint(possouris)):

            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


