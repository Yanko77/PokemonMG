import pygame

import objet
from game import Game
import player_name

import pokemon
import dresseur


def main():
    pygame.init()
    pygame.font.init()

    FPS = 144
    screen = pygame.display.set_mode((1280, 720))
    icon = pygame.image.load("assets/icon.png")
    pygame.display.set_caption("PMG || Pokemon Management Game")
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()

    game = Game()

    running = True
    posSouris = (0, 0)

    # Boucle du jeu
    while running:
        posSouris = list(pygame.mouse.get_pos())

        game.update(screen, posSouris)

        if game.bool_game_over:
            running = False

        pygame.display.flip()  # Update de la fenetre

        for event in pygame.event.get():  # Detection actions du joueur
            if event.type == pygame.QUIT:
                running = False
                game.save()

            if event.type == pygame.KEYDOWN:
                game.pressed[event.key] = True

                if event.key == pygame.K_UP:
                    print(posSouris)

                elif event.key == pygame.K_DOWN:
                    for item in game.classic_panel.ingame_window.items_panel.research_item(input()):
                        print(item.name)

                if game.is_playing:
                    if game.classic_panel.player_name_editing_mode:
                        game.classic_panel.keydown(event.key)
                    elif game.classic_panel.ingame_window.current_panel_name == 'Items':
                        game.classic_panel.ingame_window.items_panel.keydown(event.key)

            if event.type == pygame.KEYUP:
                game.pressed[event.key] = False

            if event.type == pygame.MOUSEBUTTONUP:
                game.mouse_pressed[event.button] = False
                if event.button == 1:
                    if game.is_accueil:
                        game.accueil.left_clic_interactions(posSouris)

                    elif not game.is_starter_selected:
                        game.starter_panel.left_clic_interactions(posSouris)

                    elif game.is_playing:
                        if game.is_fighting:
                            game.current_fight.left_clic_interactions(posSouris)  # Interactions clic gauche dans fight.py
                        else:
                            if game.classic_panel.ingame_window.is_hovering(posSouris):
                                if not game.classic_panel.pk_move_mode:
                                    game.classic_panel.ingame_window.left_clic_interactions(posSouris)
                            else:
                                game.classic_panel.left_clic_interactions(posSouris)

                if event.button == 3:
                    if game.is_playing:
                        if game.classic_panel.ingame_window.is_hovering(posSouris):
                            game.classic_panel.ingame_window.right_clic_interactions(posSouris)
                        else:
                            game.classic_panel.right_clic_interactions(posSouris)

            if event.type == pygame.MOUSEBUTTONDOWN:
                game.mouse_pressed[event.button] = True

        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()