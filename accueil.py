import pygame
import image


class Accueil:

    def __init__(self):
        self.intro = True
        self.debut_compteur = 0

        self.intro_accueil = image.IntroAccueil()
        self.background = image.Background()
        self.game_bar = image.GameBar()
        self.random_pokemon = image.RandomPokemon()

        self.buttons = image.AccueilButtons()

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
                        self.buttons.update(surface, possouris)
                        surface.blit(self.random_pokemon.image, (0, 0))

                    if self.game_bar.is_animation_over and not self.random_pokemon.is_animation_over:
                        surface.blit(self.random_pokemon.image, (0, 0))
                        self.random_pokemon.update_animation()

                    else:
                        self.game_bar.update_animation()

                else:
                    self.background.update_animation()
        else:
            self.debut_compteur += 1
