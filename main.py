import pygame

import objet
from game import Game
import player_name

import pokemon
import dresseur

FPS = 144
screen = pygame.display.set_mode((1280, 720))
icon = pygame.image.load("assets/icon.png")
pygame.display.set_caption("PMG || Pokemon Management Game")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

game = Game()

running = True
posSouris = (0, 0)
old_posSouris = (0, 0)

# Boucle du jeu
while running:
    posSouris = list(pygame.mouse.get_pos())

    game.update(screen, posSouris)

    pygame.display.flip()  # Update de la fenetre

    for event in pygame.event.get():  # Detection actions du joueur
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            # Touche de test admin
            if event.key == pygame.K_a:
                game.current_fight.player_pk.level_up(200)
            elif event.key == pygame.K_z:
                game.player.sac_page1[0] = objet.Objet(input())
            elif event.key == pygame.K_o:
                game.start_fight(pokemon.Pokemon('Poussifeu', 5, game), dresseur.Sauvage(game, pokemon.Pokemon('Rafflesia', 4, game)))
            elif event.key == pygame.K_p:
                print(posSouris)

            if game.player.name_editing_mode:
                if event.key == pygame.K_RETURN:
                    if game.player.name == '':
                        game.player.reset_name()
                    game.player.name_editing_mode = False

                else:
                    if event.key == pygame.K_BACKSPACE:
                        game.player.edit_name('suppr')
                    elif event.key in player_name.pygame_alphabet:
                        if game.pressed[pygame.K_LSHIFT]:
                            game.player.edit_name('add', player_name.pygame_alphabet[event.key].upper())
                        else:
                            game.player.edit_name('add', player_name.pygame_alphabet[event.key].lower())

        if event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        if event.type == pygame.MOUSEBUTTONUP:
            game.mouse_pressed[event.button] = False
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

                        if game.accueil.start_game_panel.new_game_button_rect.collidepoint(posSouris):
                            game.accueil.start_game = False
                            game.is_accueil = False
                            game.create_new_game()
                            game.reset_save_file()
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                if game.is_playing:
                    if game.is_fighting:
                        game.current_fight.left_clic_interactions(posSouris)  # Interactions clic gauche dans fight.py
                    else:
                        if game.player.name_editing_mode:
                            if not game.classic_panel.ingame_window.is_hovering(posSouris):
                                if not game.classic_panel.player_name_rect.collidepoint(posSouris):
                                    if game.player.name == '':
                                        game.player.reset_name()
                                    game.player.name_editing_mode = False

                            else:
                                if not game.classic_panel.pk_move_mode:
                                    if game.classic_panel.ingame_window.buttons.x_button_rect.collidepoint(posSouris):
                                        if not game.classic_panel.ingame_window.current_panel_name == 'Starters':
                                            game.classic_panel.ingame_window.close()
                                        elif game.is_starter_selected:
                                            game.classic_panel.ingame_window.close()
                                    elif game.classic_panel.ingame_window.buttons.min_button_rect.collidepoint(posSouris):
                                        game.classic_panel.ingame_window.minimize()
                                    elif game.classic_panel.ingame_window.is_minimized:
                                        game.classic_panel.ingame_window.maximize()

                        else:
                            if game.classic_panel.ingame_window.is_hovering(posSouris):
                                game.classic_panel.ingame_window.left_clic_interactions(posSouris)

                            else:
                                game.classic_panel.left_clic_interactions(posSouris)

            if event.button == 3:
                if game.is_playing:
                    if not game.classic_panel.ingame_window.is_hovering(posSouris):
                        if game.classic_panel.PK_RECTS[0].collidepoint(posSouris):
                            game.classic_panel.pokemon_info_mode = True
                            game.classic_panel.pokemon_info_i = 0
                        elif game.classic_panel.PK_RECTS[1].collidepoint(posSouris):
                            game.classic_panel.pokemon_info_mode = True
                            game.classic_panel.pokemon_info_i = 1
                        elif game.classic_panel.PK_RECTS[2].collidepoint(posSouris):
                            game.classic_panel.pokemon_info_mode = True
                            game.classic_panel.pokemon_info_i = 2
                        elif game.classic_panel.PK_RECTS[3].collidepoint(posSouris):
                            game.classic_panel.pokemon_info_mode = True
                            game.classic_panel.pokemon_info_i = 3
                        elif game.classic_panel.PK_RECTS[4].collidepoint(posSouris):
                            game.classic_panel.pokemon_info_mode = True
                            game.classic_panel.pokemon_info_i = 4
                        elif game.classic_panel.PK_RECTS[5].collidepoint(posSouris):
                            game.classic_panel.pokemon_info_mode = True
                            game.classic_panel.pokemon_info_i = 5

        if event.type == pygame.MOUSEBUTTONDOWN:
            game.mouse_pressed[event.button] = True

    clock.tick(FPS)

pygame.quit()
