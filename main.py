import pygame
from game import Game

FPS = 60

screen = pygame.display.set_mode((1280, 720))
icon = pygame.image.load("assets/icon.png")
pygame.display.set_caption("PMG || Pokemon Management Game")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

game = Game()

running = True

# Boucle du jeu
while running:
    posSouris = pygame.mouse.get_pos()

    game.update(screen)

    pygame.display.flip()  # Update de la fenetre

    for event in pygame.event.get():  # Detection actions du joueur
        if event.type == pygame.QUIT:
            running = False

        if game.is_accueil:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if game.accueil.buttons.quit_rect.collidepoint(posSouris):
                        running = False

                    if game.accueil.buttons.start_game_rect.collidepoint(posSouris):
                        game.is_accueil = True

    clock.tick(FPS)


pygame.quit()
