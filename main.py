import pygame
from game import Game
import player_name

import pokemon

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
    if game.mouse_pressed[1]:
        if not game.classic_panel.pk_move_mode and not game.classic_panel.ingame_window.sac_panel.emp_move_mode and not \
                game.classic_panel.ingame_window.starters_panel.pk_move_mode and not game.classic_panel.ingame_window.spawn_panel.spawning_pk_move_mode:
            if game.classic_panel.ingame_window.main_window_bar_rect.collidepoint(posSouris):
                game.classic_panel.ingame_window.window_pos_modif_mode = True
            if game.classic_panel.ingame_window.window_pos_modif_mode:
                if posSouris != old_posSouris:
                    game.classic_panel.ingame_window.main_window_pos[0] += posSouris[0] - old_posSouris[0]
                    game.classic_panel.ingame_window.main_window_pos[1] += posSouris[1] - old_posSouris[1]

    game.update(screen, posSouris)

    old_posSouris = posSouris

    pygame.display.flip()  # Update de la fenetre

    for event in pygame.event.get():  # Detection actions du joueur
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            ## Touche de test admin
            if event.key == pygame.K_p:
                game.classic_panel.ingame_window.train_panel.add_training_pk_mode = True
            elif event.key == pygame.K_o:
                game.classic_panel.ingame_window.train_panel.difficult = 'normal'

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
                    if game.player.name_editing_mode:
                        if not game.classic_panel.ingame_window.main_window_rect.collidepoint(posSouris):
                            if not game.classic_panel.player_name_rect.collidepoint(posSouris):
                                if game.player.name == '':
                                    game.player.reset_name()
                                game.player.name_editing_mode = False

                        else:
                            if not game.classic_panel.pk_move_mode:
                                if game.classic_panel.ingame_window.buttons.x_button_rect.collidepoint(posSouris):
                                    if not game.classic_panel.ingame_window.name == 'Starters':
                                        game.classic_panel.ingame_window.close()
                                    elif game.is_starter_selected:
                                        game.classic_panel.ingame_window.close()
                                elif game.classic_panel.ingame_window.buttons.min_button_rect.collidepoint(posSouris):
                                    game.classic_panel.ingame_window.minimize()
                                elif game.classic_panel.ingame_window.is_minimized:
                                    game.classic_panel.ingame_window.maximize()

                    else:
                        if game.classic_panel.ingame_window.main_window_rect.collidepoint(posSouris):
                            if game.classic_panel.ingame_window.is_minimized:
                                game.classic_panel.ingame_window.maximize()
                            elif game.classic_panel.ingame_window.is_open:
                                if game.classic_panel.ingame_window.buttons.x_button_rect.collidepoint(posSouris):
                                    if not game.classic_panel.ingame_window.name == 'Starters':
                                        game.classic_panel.ingame_window.close()
                                    elif game.is_starter_selected:
                                        game.classic_panel.ingame_window.close()
                                elif game.classic_panel.ingame_window.buttons.min_button_rect.collidepoint(posSouris):
                                    game.classic_panel.ingame_window.minimize()
                                elif game.classic_panel.ingame_window.name == "Sac d'objets":
                                    if game.classic_panel.ingame_window.sac_panel.page1_rect.collidepoint(posSouris):
                                        game.classic_panel.ingame_window.sac_panel.change_page(1)
                                    elif game.classic_panel.ingame_window.sac_panel.page2_rect.collidepoint(posSouris):
                                        game.classic_panel.ingame_window.sac_panel.change_page(2)
                                elif game.classic_panel.ingame_window.name == 'Starters':
                                    if game.classic_panel.ingame_window.starters_panel.pk_rects[0].collidepoint(
                                            posSouris):
                                        game.classic_panel.ingame_window.starters_panel.decouvrir_pk(0)
                                    elif game.classic_panel.ingame_window.starters_panel.pk_rects[1].collidepoint(
                                            posSouris):
                                        game.classic_panel.ingame_window.starters_panel.decouvrir_pk(1)
                                    elif game.classic_panel.ingame_window.starters_panel.pk_rects[2].collidepoint(
                                            posSouris):
                                        game.classic_panel.ingame_window.starters_panel.decouvrir_pk(2)
                                elif game.classic_panel.ingame_window.name == 'Spawn':
                                    if game.classic_panel.ingame_window.spawn_panel.spawn_button_rect.collidepoint(posSouris):

                                        if game.player.actions > 0:
                                            if not game.classic_panel.ingame_window.spawn_panel.boolspawn_confirm:
                                                game.classic_panel.ingame_window.spawn_panel.boolspawn_confirm = True
                                            else:
                                                game.classic_panel.ingame_window.spawn_panel.spawn_pk()
                                                game.classic_panel.ingame_window.spawn_panel.boolspawn_confirm = False
                                    elif game.classic_panel.ingame_window.spawn_panel.catch_button_rect.collidepoint(posSouris):

                                        if game.player.actions > 0 and game.classic_panel.ingame_window.spawn_panel.spawning_pk is not None:
                                            if game.classic_panel.ingame_window.spawn_panel.is_spawning_pk_lock:
                                                if not game.classic_panel.ingame_window.spawn_panel.boolcatch_confirm:
                                                    game.classic_panel.ingame_window.spawn_panel.boolcatch_confirm = True
                                                else:
                                                    game.classic_panel.ingame_window.spawn_panel.catch_pk()
                                                    game.classic_panel.ingame_window.spawn_panel.boolcatch_confirm = False
                                elif game.classic_panel.ingame_window.name == 'Train':
                                    if game.classic_panel.ingame_window.train_panel.settings_button_rect.collidepoint(posSouris):
                                        if game.classic_panel.ingame_window.train_panel.boolSettings_popup:
                                            game.classic_panel.ingame_window.train_panel.boolSettings_popup = False
                                        else:
                                            game.classic_panel.ingame_window.train_panel.boolSettings_popup = True

                                    if game.classic_panel.ingame_window.train_panel.boolSettings_popup:
                                        if game.classic_panel.ingame_window.train_panel.easy_button_rect.collidepoint(posSouris):
                                            game.classic_panel.ingame_window.train_panel.set_difficult('easy')
                                            game.classic_panel.ingame_window.train_panel.close_settings_popup()
                                        elif game.classic_panel.ingame_window.train_panel.normal_button_rect.collidepoint(posSouris):
                                            game.classic_panel.ingame_window.train_panel.set_difficult('normal')
                                            game.classic_panel.ingame_window.train_panel.close_settings_popup()
                                        elif game.classic_panel.ingame_window.train_panel.hard_button_rect.collidepoint(posSouris):
                                            game.classic_panel.ingame_window.train_panel.set_difficult('hard')
                                            game.classic_panel.ingame_window.train_panel.close_settings_popup()

                                    if game.classic_panel.ingame_window.train_panel.training_pk is None:
                                        if game.classic_panel.ingame_window.train_panel.add_button_rect.collidepoint(posSouris):
                                            game.classic_panel.ingame_window.train_panel.add_training_pk_mode = True
                                    else:
                                        if game.classic_panel.ingame_window.train_panel.training_pk_rect.collidepoint(posSouris):
                                            game.classic_panel.ingame_window.train_panel.training_pk = None
                                            game.classic_panel.ingame_window.train_panel.add_training_pk_mode = True
                                        elif game.classic_panel.ingame_window.train_panel.ennemy_pk_infos_stats_button_rect.collidepoint(posSouris):
                                            game.classic_panel.ingame_window.train_panel.ennemy_pk_info_stats_mode = not(game.classic_panel.ingame_window.train_panel.ennemy_pk_info_stats_mode)

                                    if game.classic_panel.ingame_window.train_panel.add_training_pk_mode:
                                        if game.classic_panel.ingame_window.train_panel.choose_training_pk_popup.x_button_rect.collidepoint(posSouris):
                                            game.classic_panel.ingame_window.train_panel.add_training_pk_mode = False

                        else:
                            if not game.classic_panel.pk_move_mode:
                                if game.classic_panel.player_name_rect.collidepoint(posSouris):
                                    if game.classic_panel.pokemon_info_mode:
                                        if not game.classic_panel.pokemon_info_popup_rect.collidepoint(posSouris):
                                            game.player.enable_name_editing_mode()
                                            game.classic_panel.pokemon_info_mode = False
                                    else:
                                        game.player.enable_name_editing_mode()

                                    if game.classic_panel.ingame_window.is_open:
                                        game.classic_panel.ingame_window.close()

                                if game.is_starter_selected:
                                    if game.classic_panel.buttons.spawn_button_rect.collidepoint(posSouris):
                                        if game.classic_panel.buttons.unlocked_buttons['Spawn']:
                                            game.classic_panel.ingame_window.update_name('spawn')
                                            game.classic_panel.ingame_window.open()
                                            game.classic_panel.ingame_window.maximize()
                                    elif game.classic_panel.buttons.train_button_rect.collidepoint(posSouris):
                                        if game.classic_panel.buttons.unlocked_buttons['Train']:
                                            game.classic_panel.ingame_window.update_name('train')
                                            game.classic_panel.ingame_window.open()
                                            game.classic_panel.ingame_window.maximize()
                                    elif game.classic_panel.buttons.grind_button_rect.collidepoint(posSouris):
                                        if game.classic_panel.buttons.unlocked_buttons['Grind']:
                                            game.classic_panel.ingame_window.update_name('grind')
                                            game.classic_panel.ingame_window.open()
                                            game.classic_panel.ingame_window.maximize()
                                    elif game.classic_panel.buttons.items_button_rect.collidepoint(posSouris):
                                        if game.classic_panel.buttons.unlocked_buttons['Items']:
                                            game.classic_panel.ingame_window.update_name('items')
                                            game.classic_panel.ingame_window.open()
                                            game.classic_panel.ingame_window.maximize()
                                    elif game.classic_panel.buttons.evol_button_rect.collidepoint(posSouris):
                                        if game.classic_panel.buttons.unlocked_buttons['Evol']:
                                            game.classic_panel.ingame_window.update_name('evolutions')
                                            game.classic_panel.ingame_window.open()
                                            game.classic_panel.ingame_window.maximize()
                                    if game.classic_panel.sac_button_rect.collidepoint(posSouris):
                                        game.classic_panel.ingame_window.update_name("Sac d'objets")
                                        game.classic_panel.ingame_window.open()
                                        game.classic_panel.ingame_window.maximize()

                                if game.classic_panel.pokemon_info_mode:
                                    if pygame.Rect(1210, 9, 59, 59).collidepoint(posSouris):
                                        game.classic_panel.pokemon_info_mode = False

                    if game.classic_panel.ingame_window.window_pos_modif_mode:
                        game.classic_panel.ingame_window.window_pos_modif_mode = False

                        if game.classic_panel.ingame_window.main_window_pos[0] < -16:
                            game.classic_panel.ingame_window.main_window_pos[0] = -16
                        elif game.classic_panel.ingame_window.main_window_pos[0] > 386:
                            game.classic_panel.ingame_window.main_window_pos[0] = 386
                        if game.classic_panel.ingame_window.main_window_pos[1] > 188:
                            game.classic_panel.ingame_window.main_window_pos[1] = 188
                        elif game.classic_panel.ingame_window.main_window_pos[1] < 4:
                            game.classic_panel.ingame_window.main_window_pos[1] = 4

            if event.button == 3:
                if game.is_playing:
                    if not game.classic_panel.ingame_window.main_window_rect.collidepoint(posSouris):
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
