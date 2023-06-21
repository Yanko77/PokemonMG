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

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if game.is_accueil:
                    if game.accueil.basic_panel:
                        if game.accueil.buttons.quit_rect.collidepoint(posSouris):
                            running = False

                        if game.accueil.buttons.start_game_rect.collidepoint(posSouris):
                            game.accueil.start_game = True
                            game.accueil.basic_panel = False
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                    if game.accueil.start_game:
                        if game.accueil.start_game_panel.x_button_rect.collidepoint(posSouris):
                            game.accueil.start_game = False
                            game.accueil.basic_panel = True

    clock.tick(FPS)


pygame.quit()
