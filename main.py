import random

import pygame
from game import Game

FPS = 60

screen = pygame.display.set_mode((1280, 720))
icon = pygame.image.load("assets/icon.png")
pygame.display.set_caption("PMG || Pokemon Management Game")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

pygame_alphabet = {
    pygame.K_a: 'a',
    pygame.K_b: 'b',
    pygame.K_c: 'c',
    pygame.K_d: 'd',
    pygame.K_e: 'e',
    pygame.K_f: 'f',
    pygame.K_g: 'g',
    pygame.K_h: 'h',
    pygame.K_i: 'i',
    pygame.K_j: 'j',
    pygame.K_k: 'k',
    pygame.K_l: 'l',
    pygame.K_m: 'm',
    pygame.K_n: 'n',
    pygame.K_o: 'o',
    pygame.K_p: 'p',
    pygame.K_q: 'q',
    pygame.K_r: 'r',
    pygame.K_s: 's',
    pygame.K_t: 't',
    pygame.K_u: 'u',
    pygame.K_v: 'v',
    pygame.K_w: 'w',
    pygame.K_x: 'x',
    pygame.K_y: 'y',
    pygame.K_z: 'z',
    pygame.K_SPACE: ' ',
    pygame.K_LSHIFT: '',
    pygame.K_BACKSPACE: '',
    pygame.K_KP_0: '0',
    pygame.K_KP_1: '1',
    pygame.K_KP_2: '2',
    pygame.K_KP_3: '3',
    pygame.K_KP_4: '4',
    pygame.K_KP_5: '5',
    pygame.K_KP_6: '6',
    pygame.K_KP_7: '7',
    pygame.K_KP_8: '8',
    pygame.K_KP_9: '9',
    pygame.K_COMMA: '.'
}

alphabet_pixels = {
    'a': 20,
    'b': 21,
    'c': 20,
    'd': 21,
    'e': 21,
    'f': 9,
    'g': 21,
    'h': 21,
    'i': 9,
    'j': 9,
    'k': 19,
    'l': 9,
    'm': 34,
    'n': 21,
    'o': 21,
    'p': 21,
    'q': 21,
    'r': 13,
    's': 19,
    't': 10,
    'u': 21,
    'v': 17,
    'w': 28,
    'x': 22,
    'y': 17,
    'z': 14,
    ' ': 3,
    '': 0,
    '0': 18,
    '1': 14,
    '2': 20,
    '3': 22,
    '4': 20,
    '5': 22,
    '6': 22,
    '7': 15.9,
    '8': 22,
    '9': 22,
    '.': 4,
    'intertext': 5,
    'A': 21,
    'B': 23,
    'C': 23,
    'D': 23,
    'E': 16,
    'F': 15,
    'G': 23,
    'H': 23,
    'I': 9,
    'J': 12,
    'K': 22,
    'L': 14,
    'M': 31,
    'N': 22,
    'O': 22,
    'P': 20,
    'Q': 22,
    'R': 22,
    'S': 21,
    'T': 18,
    'U': 22,
    'V': 21,
    'W': 36,
    'X': 19,
    'Y': 19,
    'Z': 15,
}

game = Game(alphabet_pixels)

running = True

# Boucle du jeu
while running:
    posSouris = pygame.mouse.get_pos()

    game.update(screen, posSouris)

    pygame.display.flip()  # Update de la fenetre

    for event in pygame.event.get():  # Detection actions du joueur
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            if game.classic_panel.change_player_name_mode:
                if event.key == pygame.K_RETURN:
                    if game.player_name == '':
                        game.player_name = random.choice(game.player_random_names)
                        game.classic_panel.update_player_name(game.player_name)
                    game.classic_panel.change_player_name_mode = False

                else:
                    if game.classic_panel.calcul_player_name_pixels() < 385:
                        if game.pressed[pygame.K_LSHIFT]:
                            if event.key in pygame_alphabet:
                                game.player_name += pygame_alphabet[event.key].upper()
                        else:
                            if event.key in pygame_alphabet:
                                game.player_name += pygame_alphabet[event.key]
                            else:
                                print('lettre inconnue')

                    if event.key == pygame.K_BACKSPACE:
                        game.player_name = game.player_name[:-1]

        if event.type == pygame.KEYUP:
            game.pressed[event.key] = False

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

                        if game.accueil.start_game_panel.new_game_button_rect.collidepoint(posSouris):
                            game.accueil.start_game = False
                            game.is_accueil = False
                            game.create_new_game()
                            game.reset_save_file()
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                if game.is_playing:
                    if not game.classic_panel.change_player_name_mode:
                        if game.classic_panel.player_name_rect.collidepoint(posSouris):
                            game.classic_panel.change_player_name_mode = True
                            game.player_name = ""
                            game.classic_panel.is_pname_modif = True
                    else:
                        if not game.classic_panel.player_name_rect.collidepoint(posSouris):
                            if game.player_name == '':
                                game.player_name = random.choice(game.player_random_names)
                                game.classic_panel.update_player_name(game.player_name)
                            game.classic_panel.change_player_name_mode = False

    clock.tick(FPS)


pygame.quit()
