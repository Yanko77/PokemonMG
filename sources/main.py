# Modules
from sources.config import FPS, SCREEN_SIZE

import pygame
pygame.init()
pygame.font.init()

from game import Game

# Fonctions


def main(fps, screen_size):

    screen = pygame.display.set_mode(screen_size)
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
                    game.notif('Ca marche !')

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    game.left_clic_interactions(possouris)

        clock.tick(fps)

    pygame.quit()

# Programme principal


if __name__ == '__main__':
    main(FPS, SCREEN_SIZE)
