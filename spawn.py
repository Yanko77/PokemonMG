import pygame
import random

import image
import pokemon


class SpawnPanel:
    def __init__(self, game):
        self.game = game

        self.min_spawning_pk_level = 2
        self.max_spawning_pk_level = 5
        self.spawning_pk_level_bonus = 0

        ## Image BACKGROUND
        self.background = pygame.image.load('assets/game/ingame_windows/Spawn/background.png')

        ## Bouton AIDE
        self.button_aide = image.load_image('assets/game/ingame_windows/Spawn/aide_button.png')
        self.button_aide_rect = image.get_custom_rect(self.button_aide, 838, 46)

        self.button_aide_hover = image.load_image('assets/game/ingame_windows/Spawn/aide_button_hover.png')

        self.aide_popup = image.load_image('assets/game/ingame_windows/Spawn/aide_popup.png')

        ## Bouton SPAWN
        self.spawn_button = image.load_image('assets/game/ingame_windows/Spawn/spawn_button.png')
        self.spawn_button_rect = image.get_custom_rect(self.spawn_button, 397, 312)
        self.spawn_button_hover = image.load_image('assets/game/ingame_windows/Spawn/spawn_button_hover.png')
        self.spawn_popup = image.load_image('assets/game/ingame_windows/Spawn/spawn_popup.png')
        self.spawn_popup_lock = image.load_image('assets/game/ingame_windows/Spawn/spawn_popup_lock.png')
        self.spawn_button_lock = image.load_image('assets/game/ingame_windows/Spawn/spawn_button_lock.png')


        self.catch_button = pygame.image.load('assets/game/ingame_windows/Spawn/catch_button.png')
        self.catch_button_rect = self.catch_button.get_rect()
        self.catch_button_rect.x = 397
        self.catch_button_rect.y = 216
        self.catch_button_hover = pygame.image.load('assets/game/ingame_windows/Spawn/catch_button_hover.png')
        self.catch_popup = pygame.image.load('assets/game/ingame_windows/Spawn/catch_popup.png')
        self.catch_button_lock = pygame.image.load('assets/game/ingame_windows/Spawn/catch_button_lock.png')
        self.catch_popup_lock = pygame.image.load('assets/game/ingame_windows/Spawn/catch_popup_lock.png')

        self.spawning_levels_button = pygame.image.load('assets/game/ingame_windows/Spawn/spawning_levels_button.png')
        self.spawning_levels_button_rect = self.spawning_levels_button.get_rect()
        self.spawning_levels_button_rect.x = 32
        self.spawning_levels_button_rect.y = 102
        self.spawning_levels_button_hover = pygame.image.load('assets/game/ingame_windows/Spawn/spawning_levels_button_hover.png')
        self.spawning_levels_popup = pygame.image.load('assets/game/ingame_windows/Spawn/spawning_levels_popup.png')

        self.spawning_pk_lock = pygame.image.load('assets/game/ingame_windows/Spawn/locked.png')
        self.is_spawning_pk_lock = True

        self.spawning_pk_hover = pygame.image.load('assets/game/ingame_windows/Spawn/spawning_pk_hover.png')
        self.spawning_pk_rect = pygame.Rect(104, 117, 267, 267)
        self.spawning_pk_hover_lock = pygame.image.load('assets/game/ingame_windows/Spawn/spawning_pk_hover_lock.png')
        self.spawning_pk = None

        self.SPAWNING_PK_RECT = pygame.Rect(104, 117, 267, 267)
        self.SPAWNING_PK_RECT.x = 104
        self.SPAWNING_PK_RECT.y = 117
        self.spawning_pk_move_mode = False
        self.possouris_rel = [0, 0]
        self.saved_possouris = [0, 0]

        self.spawn_confirm = pygame.image.load('assets/game/ingame_windows/Spawn/confirm.png')
        self.spawn_confirm_rect = self.spawn_confirm.get_rect()
        self.spawn_confirm_rect.x = 391
        self.spawn_confirm_rect.y = 311
        self.spawn_confirm_hover = pygame.image.load('assets/game/ingame_windows/Spawn/confirm_hover.png')
        self.spawn_confirm_popup_rect = pygame.Rect(398, 314, 338, 92)
        self.boolspawn_confirm = False

        self.catch_confirm = pygame.image.load('assets/game/ingame_windows/Spawn/confirm.png')
        self.catch_confirm_rect = self.catch_confirm.get_rect()
        self.catch_confirm_rect.x = 391
        self.catch_confirm_rect.y = 214
        self.catch_confirm_hover = pygame.image.load('assets/game/ingame_windows/Spawn/confirm_hover.png')
        self.catch_confirm_popup_rect = pygame.Rect(398, 217, 338, 92)
        self.boolcatch_confirm = False

        self.infos_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 30)
        self.spawning_pk_level_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 25)

    def update(self, surface, possouris, window_pos):
        self.update_rect_pos(window_pos)
        self.update_spawning_pk_level()

        surface.blit(self.background, (window_pos[0] - 13, window_pos[1] - 21))

        if self.button_aide_rect.collidepoint(possouris):
            surface.blit(self.button_aide_hover, self.button_aide_rect)
            surface.blit(self.aide_popup, (492 + window_pos[0], 46 + window_pos[1]))
        else:
            surface.blit(self.button_aide, self.button_aide_rect)

        if self.spawn_button_rect.collidepoint(possouris):
            if self.boolspawn_confirm:
                surface.blit(self.spawn_confirm_hover, self.spawn_confirm_rect)
            else:
                if not self.spawning_pk_move_mode:
                    if self.game.player.actions > 0:
                        surface.blit(self.spawn_button_hover, self.spawn_button_rect)
                        surface.blit(self.spawn_popup, (507 + window_pos[0], 316 + window_pos[1]))
                    else:
                        surface.blit(self.spawn_button_lock, self.spawn_button_rect)
                        surface.blit(self.spawn_popup_lock, (507 + window_pos[0], 316 + window_pos[1]))
                else:
                    surface.blit(self.spawn_button_lock, self.spawn_button_rect)
        else:
            if self.boolspawn_confirm:
                surface.blit(self.spawn_confirm, self.spawn_confirm_rect)
                if not self.spawn_confirm_popup_rect.collidepoint(possouris):
                    self.boolspawn_confirm = False
            else:
                surface.blit(self.spawn_button, self.spawn_button_rect)

        if self.catch_button_rect.collidepoint(possouris):
            if self.boolcatch_confirm:
                surface.blit(self.catch_confirm_hover, self.catch_confirm_rect)
            else:
                if not self.spawning_pk_move_mode:
                    if self.game.player.actions > 0 and self.spawning_pk is not None:
                        if self.is_spawning_pk_lock:
                            surface.blit(self.catch_button_hover, self.catch_button_rect)
                            surface.blit(self.catch_popup, (507 + window_pos[0], 219 + window_pos[1]))
                        else:
                            surface.blit(self.catch_button_lock, self.catch_button_rect)
                            surface.blit(self.catch_popup_lock, (507 + window_pos[0], 219 + window_pos[1]))
                    else:
                        surface.blit(self.catch_button_lock, self.catch_button_rect)
                        surface.blit(self.catch_popup_lock, (507 + window_pos[0], 219 + window_pos[1]))
                else:
                    surface.blit(self.catch_button_lock, self.catch_button_rect)
        else:
            if self.boolcatch_confirm:
                surface.blit(self.catch_confirm, self.catch_confirm_rect)
                if not self.catch_confirm_popup_rect.collidepoint(possouris):
                    self.boolcatch_confirm = False
            else:
                surface.blit(self.catch_button, self.catch_button_rect)

        if self.spawning_levels_button_rect.collidepoint(possouris):
            surface.blit(self.spawning_levels_button_hover, self.spawning_levels_button_rect)
            surface.blit(self.spawning_levels_popup, (36 + window_pos[0], 46 + window_pos[1]))
        else:
            surface.blit(self.spawning_levels_button, self.spawning_levels_button_rect)

        if self.spawning_pk_rect.collidepoint(possouris):
            if self.is_spawning_pk_lock:
                surface.blit(self.spawning_pk_hover_lock, self.spawning_pk_rect)

        if self.is_spawning_pk_lock:
            if self.spawning_pk_rect.collidepoint(possouris):
                surface.blit(self.spawning_pk_hover_lock, self.spawning_pk_rect)
        else:
            if not self.spawning_pk_move_mode:
                if self.spawning_pk_rect.collidepoint(possouris):
                    if self.game.mouse_pressed[1]:
                        self.spawning_pk_move_mode = True
                        self.possouris_rel = [0, 0]
                        self.saved_possouris = possouris

            else:
                if not self.game.mouse_pressed[1]:
                    self.spawning_pk_move_mode = False

                    if self.game.classic_panel.PK_RECTS[0].collidepoint(possouris):
                        self.spawning_pk_in_team(0)
                    elif self.game.classic_panel.PK_RECTS[1].collidepoint(possouris):
                        self.spawning_pk_in_team(1)
                    elif self.game.classic_panel.PK_RECTS[2].collidepoint(possouris):
                        self.spawning_pk_in_team(2)
                    elif self.game.classic_panel.PK_RECTS[3].collidepoint(possouris):
                        self.spawning_pk_in_team(3)
                    elif self.game.classic_panel.PK_RECTS[4].collidepoint(possouris):
                        self.spawning_pk_in_team(4)
                    elif self.game.classic_panel.PK_RECTS[5].collidepoint(possouris):
                        self.spawning_pk_in_team(5)
                else:
                    self.possouris_rel = (possouris[0] - self.saved_possouris[0], possouris[1] - self.saved_possouris[1])
                    self.spawning_pk_rect.x = self.SPAWNING_PK_RECT.x + self.possouris_rel[0]
                    self.spawning_pk_rect.y = self.SPAWNING_PK_RECT.y + self.possouris_rel[1]

            if self.spawning_pk_rect.collidepoint(possouris):
                surface.blit(self.spawning_pk_hover, self.spawning_pk_rect)

        if self.spawning_pk is not None:
            surface.blit(pygame.transform.scale(self.spawning_pk.icon_image, (600, 300)),
                         (self.spawning_pk_rect.x - 19, self.spawning_pk_rect.y - 47), (0, 0, 300, 300))
            if not self.button_aide_rect.collidepoint(possouris):
                surface.blit(self.infos_font.render('Pokemon : ' + self.spawning_pk.name, False, (255, 255, 255)), (570 + window_pos[0], 90 + window_pos[1]))
                surface.blit(self.infos_font.render('Level : ' + str(self.spawning_pk.level), False, (255, 255, 255)),
                             (570 + window_pos[0], 125 + window_pos[1]))

        if self.is_spawning_pk_lock:
            surface.blit(self.spawning_pk_lock, (74 + window_pos[0], 85 + window_pos[1]))

    def update_rect_pos(self, window_pos):
        self.button_aide_rect.x = 838 + window_pos[0]
        self.button_aide_rect.y = 46 + window_pos[1]
        self.spawn_button_rect.x = 397 + window_pos[0]
        self.spawn_button_rect.y = 312 + window_pos[1]
        self.catch_button_rect.x = 397 + window_pos[0]
        self.catch_button_rect.y = 216 + window_pos[1]
        self.spawning_levels_button_rect.x = 32 + window_pos[0]
        self.spawning_levels_button_rect.y = 102 + window_pos[1]
        if not self.spawning_pk_move_mode:
            self.spawning_pk_rect.x = 104 + window_pos[0]
            self.spawning_pk_rect.y = 117 + window_pos[1]
            self.SPAWNING_PK_RECT.x = 104 + window_pos[0]
            self.SPAWNING_PK_RECT.y = 117 + window_pos[1]
        self.spawn_confirm_rect.x = 391 + window_pos[0]
        self.spawn_confirm_rect.y = 311 + window_pos[1]
        self.spawn_confirm_popup_rect = pygame.Rect(398 + window_pos[0], 314 + window_pos[1], 338, 92)
        self.catch_confirm_rect.x = 391 + window_pos[0]
        self.catch_confirm_rect.y = 214 + window_pos[1]
        self.catch_confirm_popup_rect = pygame.Rect(398 + window_pos[0], 217 + window_pos[1], 338, 92)

    def spawning_pk_in_team(self, team_i):
        if self.game.player.team[team_i] is None:
            self.game.player.team[team_i] = self.spawning_pk
            self.spawning_pk = None
            self.is_spawning_pk_lock = True

    def update_spawning_pk_level(self):
        if not round(self.game.player.level*1.5+2 + self.spawning_pk_level_bonus) == self.min_spawning_pk_level:
            self.min_spawning_pk_level = round(self.game.player.level*1.5+2 + self.spawning_pk_level_bonus)

        if not round(self.game.player.level*1.5+5 + self.spawning_pk_level_bonus) == self.max_spawning_pk_level:
            self.max_spawning_pk_level = round(self.game.player.level*1.5+5 + self.spawning_pk_level_bonus)

    def spawn_pk(self):
        self.spawning_pk = pokemon.Pokemon(self.get_spawning_pokemon(self.game.player.level),
                                           random.randint(self.min_spawning_pk_level, self.max_spawning_pk_level), self.game.player)
        self.is_spawning_pk_lock = True

        self.game.player.use_action()
        self.game.classic_panel.boolNotif = True

    def catch_pk(self):
        self.is_spawning_pk_lock = False

        self.game.player.use_action()

    def left_clic_interactions(self, possouris):
        if self.spawn_button_rect.collidepoint(possouris):

            if self.game.player.actions > 0:
                if not self.boolspawn_confirm:
                    self.boolspawn_confirm = True
                else:
                    self.spawn_pk()
                    self.boolspawn_confirm = False
        elif self.catch_button_rect.collidepoint(possouris):

            if self.game.player.actions > 0 and self.spawning_pk is not None:
                if self.is_spawning_pk_lock:
                    if not self.boolcatch_confirm:
                        self.boolcatch_confirm = True
                    else:
                        self.catch_pk()
                        self.boolcatch_confirm = False

    def is_hovering_buttons(self, possouris):
        if self.button_aide_rect.collidepoint(possouris):
            return True
        if self.catch_button_rect.collidepoint(possouris):
            return True
        if self.spawn_button_rect.collidepoint(possouris):
            return True
        if self.spawning_levels_button_rect.collidepoint(possouris):
            return True
        if self.spawning_pk_rect.collidepoint(possouris) and not self.is_spawning_pk_lock:
            return True
        return False

    def find_pokemon_line(self, name) -> list:
        with open('all_pokemons.txt') as file:
            for line in file.readlines():
                if line.split()[0] == name:
                    return line.split()

    def get_valable_pokemons(self, player_level):
        valable_pks = []
        with open('all_pokemons.txt', 'r') as file:
            for line in file.readlines():
                line = line.split()
                if not (line[0] == "#" or line[0] == "name"):
                    if int(line[9]) <= player_level:
                        valable_pks.append(line[0])
        return valable_pks

    def get_pk_rarity(self, pokemon):
        pokemon_rarity = int(self.find_pokemon_line(pokemon)[1])
        pokemon_rarity = 100 - pokemon_rarity
        return pokemon_rarity

    def get_total_spawn_chances(self, valable_pks):
        total_rarity = 0
        for pokemon in valable_pks:
            pokemon_rarity = self.get_pk_rarity(pokemon)
            total_rarity += pokemon_rarity
        return total_rarity

    def get_spawning_pokemon(self, player_level):
        generated_number = random.randint(0, self.get_total_spawn_chances(self.get_valable_pokemons(player_level)))
        max_spawn_value = 0
        for pokemon in self.get_valable_pokemons(player_level):
            max_spawn_value += self.get_pk_rarity(pokemon)
            if max_spawn_value < generated_number:
                pass
            else:
                return pokemon


