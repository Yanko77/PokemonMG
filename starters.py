import pygame
import pokemon


class StartersPanel:

    def __init__(self, game):
        self.game = game

        self.background = pygame.image.load('assets/game/ingame_windows/Starters/background.png')
        self.button_aide = pygame.image.load('assets/game/ingame_windows/Starters/button_aide.png')
        self.button_aide_rect = pygame.Rect(800, 444, 42, 42)
        self.button_aide_hover = pygame.image.load('assets/game/ingame_windows/Starters/button_aide_hover.png')

        self.pokeball1 = pygame.image.load('assets/game/ingame_windows/Starters/pokeball1.png')
        self.pk1_rect = pygame.Rect(80, 84, 190, 190)
        self.pokeball2 = pygame.image.load('assets/game/ingame_windows/Starters/pokeball2.png')
        self.pk2_rect = pygame.Rect(362, 84, 190, 190)
        self.pokeball3 = pygame.image.load('assets/game/ingame_windows/Starters/pokeball3.png')
        self.pk3_rect = pygame.Rect(642, 84, 190, 190)

        self.pk_hover = pygame.image.load('assets/game/ingame_windows/Starters/pokeball_hover.png')
        self.pk_hover = pygame.transform.scale(self.pk_hover, (190, 190))

        self.starter1 = pokemon.Pokemon(self.game.starters[0], 5)
        self.starter2 = pokemon.Pokemon(self.game.starters[1], 5)
        self.starter3 = pokemon.Pokemon(self.game.starters[2], 5)

        self.pk_decouverts = [False, False, False]

    def update(self, surface, possouris, window_pos):
        self.update_rect_pos(window_pos)

        surface.blit(self.background, window_pos)

        if self.button_aide_rect.collidepoint(possouris):
            surface.blit(self.button_aide_hover, window_pos)
        else:
            surface.blit(self.button_aide, window_pos)

        if self.pk1_rect.collidepoint(possouris):
            surface.blit(self.pk_hover, (80+window_pos[0], 84+window_pos[1]))
        elif self.pk2_rect.collidepoint(possouris):
            surface.blit(self.pk_hover, (362+window_pos[0], 84+window_pos[1]))
        elif self.pk3_rect.collidepoint(possouris):
            surface.blit(self.pk_hover, (642+window_pos[0], 84+window_pos[1]))

        if not self.pk_decouverts[0]:
            surface.blit(self.pokeball1, window_pos)
        else:
            if self.starter1.name == 'Bulbizarre':
                surface.blit(pygame.transform.scale(self.starter1.icon_image, (512, 256)), (window_pos[0]+40, window_pos[1]+30), (0, 0, 256, 256))
            else:
                surface.blit(pygame.transform.scale(self.starter1.icon_image, (512, 256)),
                             (window_pos[0] + 50, window_pos[1] + 30), (0, 0, 256, 256))
        if not self.pk_decouverts[1]:
            surface.blit(self.pokeball2, window_pos)
        else:
            surface.blit(pygame.transform.scale(self.starter2.icon_image, (512, 256)),
                         (window_pos[0] + 332, window_pos[1] + 30), (0, 0, 256, 256))
        if not self.pk_decouverts[2]:
            surface.blit(self.pokeball3, window_pos)
        else:
            surface.blit(pygame.transform.scale(self.starter3.icon_image, (512, 256)),
                         (window_pos[0] + 614, window_pos[1] + 30), (0, 0, 256, 256))

    def update_rect_pos(self, window_pos):
        self.button_aide_rect = pygame.Rect(800 + window_pos[0], 444 + window_pos[1], 42, 42)
        self.pk1_rect = pygame.Rect(80 + window_pos[0], 84 + window_pos[1], 190, 190)
        self.pk2_rect = pygame.Rect(362 + window_pos[0], 84 + window_pos[1], 190, 190)
        self.pk3_rect = pygame.Rect(642 + window_pos[0], 84 + window_pos[1], 190, 190)

    def decouvrir_pk(self, i):
        self.pk_decouverts[i] = True

    def is_hovering_buttons(self, possouris, window_pos):
        if self.pk1_rect.collidepoint(possouris) or self.pk2_rect.collidepoint(possouris) \
                or self.pk3_rect.collidepoint(possouris) or self.button_aide_rect.collidepoint(possouris):
            return True
