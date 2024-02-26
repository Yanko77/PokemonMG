import pygame
import image


class Accueil:

    def __init__(self):
        self.intro = True
        self.basic_panel = True
        self.start_game = False
        self.credits = False
        self.settings = False

        self.debut_compteur = 0

        self.intro_accueil = image.IntroAccueil()
        self.background = image.Background()
        self.game_bar = image.GameBar()
        self.random_pokemon = image.RandomPokemon()

        self.buttons = image.AccueilButtons()

        self.start_game_panel = StartGamePanel()

    def update(self, surface):
        possouris = pygame.mouse.get_pos()

        if self.debut_compteur > 50:
            if self.intro:
                surface.blit(self.intro_accueil.image, (0, 0))
                self.intro_accueil.update_animation()
                if self.intro_accueil.is_animation_over:
                    self.intro = False
            else:
                surface.blit(self.background.image, (0, 0))
                if self.background.is_animation_over:
                    surface.blit(self.game_bar.image, (0, 0))

                    if self.random_pokemon.is_animation_over:
                        self.buttons.update(surface, possouris, self.basic_panel)
                        surface.blit(self.random_pokemon.image, (0, 0))

                        if self.start_game:
                            self.start_game_panel.update(surface, possouris, self.basic_panel)

                    if self.game_bar.is_animation_over and not self.random_pokemon.is_animation_over:
                        surface.blit(self.random_pokemon.image, (0, 0))
                        self.random_pokemon.update_animation()

                    else:
                        self.game_bar.update_animation()

                else:
                    self.background.update_animation()
        else:
            self.debut_compteur += 1


class StartGamePanel:

    def __init__(self):
        self.panel = image.load_image('assets/accueil/panels/start_game/panel.png')

        self.new_game_button = image.load_image('assets/accueil/panels/start_game/new_game_button.png')
        self.new_game_button_rect = image.get_custom_rect(self.new_game_button, 791, 508)
        self.new_game_button_h = image.load_image('assets/accueil/panels/start_game/new_game_button_hover.png')

        self.load_game_button = image.load_image('assets/accueil/panels/start_game/load_game_button.png')
        self.load_game_button_rect = image.get_custom_rect(self.load_game_button, 130, 508)
        self.load_game_button_h = image.load_image('assets/accueil/panels/start_game/load_game_button_hover.png')

        self.x_button = image.load_image('assets/accueil/panels/start_game/x_button.png')
        self.x_button_rect = image.get_custom_rect(self.x_button, 1144, 68)
        self.x_button_h = image.load_image('assets/accueil/panels/start_game/x_button_hover.png')

    def update(self, surface, possouris, basic_accueil):
        surface.blit(self.panel, (0, 0))

        # Bouton NEW GAME
        self.update_button(self.new_game_button, self.new_game_button_rect, self.new_game_button_h, surface, possouris, basic_accueil)

        # Bouton LOAD GAME
        self.update_button(self.load_game_button, self.load_game_button_rect, self.load_game_button_h, surface, possouris, basic_accueil)

        # Bouton NEW GAME
        self.update_button(self.x_button, self.x_button_rect, self.x_button_h, surface, possouris, basic_accueil)

        if not (self.x_button_rect.collidepoint(possouris) or self.new_game_button_rect.collidepoint(possouris)
                or self.load_game_button_rect.collidepoint(possouris)):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def update_button(self, button, button_rect, button_hover, surface, possouris, basic_accueil):
        if button_rect.collidepoint(possouris) and not basic_accueil:
            surface.blit(button_hover, button_rect)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            surface.blit(button, button_rect)
