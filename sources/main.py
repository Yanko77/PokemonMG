"""
Cleaning effectué
"""

# Modules
from sources.config import FPS, SCREEN_SIZE

import pygame
pygame.init()
pygame.font.init()

from game import Game

# Fonctions


def main():

    screen = pygame.display.set_mode(SCREEN_SIZE)
    icon = pygame.image.load('assets/icon.png')

    pygame.display.set_caption("PKMG || Pokémon Management Game")
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()

    game = Game(screen)

    running = True

    while running:
        possouris = pygame.mouse.get_pos()
        screen.fill((0, 0, 0))

        game.update(possouris=possouris)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    game.starter_picking.intro.skip_animation()

            elif event.type == pygame.MOUSEBUTTONUP:
                game.mouse_pressed[event.button] = False

                if event.button == 1:
                    game.left_clic_interactions(possouris)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.mouse_pressed[event.button] = True

        clock.tick(FPS)

    pygame.quit()

# Programme principal


if __name__ == '__main__':
    main()
