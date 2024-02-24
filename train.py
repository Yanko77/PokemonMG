import pygame

import dresseur
import image
import random
import pokemon
import random
import game_infos


class TrainPanel:

    def __init__(self, game):
        self.game = game
        self.path = 'assets/game/ingame_windows/Train/'
        # LOADING IMAGES --------------------------
        self.background = self.load_image('background.png')
        self.emp_training_pk = self.load_image('emp_training_pk.png')
        self.settings_button = self.load_image('settings_button.png')
        self.settings_button_hover = self.load_image('settings_button_hover.png')
        self.diff_ind_easy = self.load_image('diff_ind_easy.png')
        self.diff_ind_normal = self.load_image('diff_ind_normal.png')
        self.diff_ind_hard = self.load_image('diff_ind_hard.png')
        self.locked = self.load_image('locked.png')
        self.add_button = self.load_image('add_button.png')
        self.add_button_hover = self.load_image('add_button_hover.png')
        self.settings_popup = self.load_image('settings_popup.png')
        self.easy_button = self.load_image('easy_button.png')
        self.easy_button_hover = self.load_image('easy_button_hover.png')
        self.normal_button = self.load_image('normal_button.png')
        self.normal_button_hover = self.load_image('normal_button_hover.png')
        self.hard_button = self.load_image('hard_button.png')
        self.hard_button_hover = self.load_image('hard_button_hover.png')
        self.ennemy_pk_popup = pygame.image.load('assets/game/ingame_windows/Train/ennemy_pk_popup.png')
        self.ennemy_pk_infos_stats = pygame.image.load('assets/game/ingame_windows/Train/ennemy_pk_stats.png')
        self.ennemy_pk_infos_stats_button = pygame.image.load('assets/game/ingame_windows/Train/info_stats_button.png')
        self.ennemy_pk_infos_stats_button_hover = pygame.image.load('assets/game/ingame_windows/Train/info_stats_button_hover.png')
        self.fight_button = pygame.image.load('assets/game/ingame_windows/Train/fight_button.png')
        self.fight_button_hover = pygame.image.load('assets/game/ingame_windows/Train/fight_button_hover.png')
        # LOADING FONTS ---------------------
        self.difficulty_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 35)
        self.lv_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 45)
        self.ennemy_pk_name_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 22)
        self.ennemy_pk_type_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 17)
        self.ennemy_pk_stats_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 20)
        self.info_select_pk_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 22)
        # RENDER TEXTS
        self.no_pk_selected_text = self.info_select_pk_font.render('NO POKEMON SELECTED', False, (255, 255, 255))
        self.change_pk_text = self.info_select_pk_font.render('SWAP POKEMON', False, (255, 255, 255))
        # DEFAULT VARIABLES --------------------------
        self.background_pos = (-13, -21)
        self.emp_training_pk_pos = (78, 96)
        self.pk_selected_indicator_pos = (135, 414)
        self.settings_button_rect = pygame.Rect(22, 90, 90, 120)
        self.settings_button_pos = (35, 100)
        self.diff_ind_pos = (80, 177)
        self.locked_pos = (70, 80)
        self.no_pk_selected_text_pos = (90, 65)
        self.add_button_pos = (127, 144)
        self.add_button_rect = image.get_custom_rect(self.add_button, self.add_button_pos[0], self.add_button_pos[1])
        self.settings_popup_pos = (59, 59)
        self.easy_button_pos = (92, 68)
        self.easy_button_rect = image.get_custom_rect(self.easy_button, self.easy_button_pos[0], self.easy_button_pos[1])
        self.normal_button_pos = (171, 68)
        self.normal_button_rect = image.get_custom_rect(self.normal_button, self.normal_button_pos[0], self.normal_button_pos[1])
        self.hard_button_pos = (249, 68)
        self.hard_button_rect = image.get_custom_rect(self.hard_button, self.hard_button_pos[0], self.hard_button_pos[1])
        self.ennemy_pk_infos_stats_button_rect = image.get_custom_rect(self.ennemy_pk_infos_stats_button, 715, 408)

        self.ennemy_pk_popup_pos = (446, 39)
        self.ennemy_pk_info_stats_mode = False

        self.fight_button_pos = (613, 448)
        self.fight_button_rect = image.get_custom_rect(self.fight_button, self.fight_button_pos[0], self.fight_button_pos[1])

        self.difficult = 'easy'
        self.training_pk = None
        self.training_pk_rect = pygame.Rect(111, 123, 252, 252)
        self.ennemy_pks = {
            'easy': self.spawn_ennemy_pk('easy'),
            'normal': self.spawn_ennemy_pk('normal'),
            'hard': self.spawn_ennemy_pk('hard')
        }
        self.boolSettings_popup = False
        self.add_training_pk_mode = False

        self.choose_training_pk_popup = ChooseTrainingPkPopup(self.game)

    def update(self, surface, possouris, window_pos):
        self.update_rects_pos(window_pos)

        surface.blit(self.background, (window_pos[0] + self.background_pos[0], window_pos[1] + self.background_pos[1]))

        self.update_emp_training_pk(surface, possouris, window_pos)

        if self.training_pk is not None:
            self.update_preview_ennemy(surface, window_pos, possouris)
            if self.fight_button_rect.collidepoint(possouris):
                surface.blit(self.fight_button_hover, self.fight_button_rect)
            else:
                surface.blit(self.fight_button, self.fight_button_rect)
        else:
            surface.blit(self.locked, (self.locked_pos[0] + window_pos[0],
                                       self.locked_pos[1] + window_pos[1]))
            surface.blit(self.no_pk_selected_text, (self.no_pk_selected_text_pos[0] + window_pos[0],
                                                    self.no_pk_selected_text_pos[1] + window_pos[1]))

        if self.boolSettings_popup:
            self.update_settings_popup(surface, possouris, window_pos)

        if self.add_training_pk_mode:
            self.choose_training_pk_popup.update(surface, possouris, window_pos)

    def start_training_fight(self):
        self.game.start_fight(self.training_pk, dresseur.Sauvage, self.ennemy_pks[self.difficult], self.difficult)# passage de self.difficult en paramettre

    def update_emp_training_pk(self, surface, possouris, window_pos):
        surface.blit(self.emp_training_pk, (self.emp_training_pk_pos[0] + window_pos[0],
                                            self.emp_training_pk_pos[1] + window_pos[1]))

        if self.difficult == 'easy':
            surface.blit(self.diff_ind_easy, (self.diff_ind_pos[0] + window_pos[0],
                                              self.diff_ind_pos[1] + window_pos[1]))
        elif self.difficult == 'normal':
            surface.blit(self.diff_ind_normal, (self.diff_ind_pos[0] + window_pos[0],
                                              self.diff_ind_pos[1] + window_pos[1]))
        elif self.difficult == 'hard':
            surface.blit(self.diff_ind_hard, (self.diff_ind_pos[0] + window_pos[0],
                                              self.diff_ind_pos[1] + window_pos[1]))

        if self.settings_button_rect.collidepoint(possouris):
            surface.blit(self.settings_button_hover, (self.settings_button_pos[0] + window_pos[0],
                                                      self.settings_button_pos[1] + window_pos[1]))
        else:
            surface.blit(self.settings_button, (self.settings_button_pos[0] + window_pos[0],
                                                self.settings_button_pos[1] + window_pos[1]))

        if self.training_pk is None:
            if not self.add_training_pk_mode:
                if self.add_button_rect.collidepoint(possouris):
                    surface.blit(self.add_button_hover, self.add_button_rect)
                else:
                    surface.blit(self.add_button, self.add_button_rect)

            elif self.training_pk_rect.collidepoint(possouris):
                surface.blit(self.create_rect_alpha((self.training_pk_rect.w, self.training_pk_rect.h), (255, 255, 255)), self.training_pk_rect)

            surface.blit(self.no_pk_selected_text, (self.no_pk_selected_text_pos[0] + window_pos[0],
                                                    self.no_pk_selected_text_pos[1] + window_pos[1]))

        else:
            if self.training_pk_rect.collidepoint(possouris):
                surface.blit(self.create_rect_alpha((self.training_pk_rect.w, self.training_pk_rect.h), (255, 255, 255)), self.training_pk_rect)
                surface.blit(self.change_pk_text, (self.no_pk_selected_text_pos[0] + window_pos[0] + 30,
                                                   self.no_pk_selected_text_pos[1] + window_pos[1]))

            surface.blit(pygame.transform.scale(self.training_pk.icon_image, (504, 252)), (self.training_pk_rect.x, self.training_pk_rect.y - 25), (0, 0, 252, 252))

        surface.blit(self.locked, (self.locked_pos[0] + window_pos[0],
                                   self.locked_pos[1] + window_pos[1]))

    def update_settings_popup(self, surface, possouris, window_pos):
        surface.blit(self.settings_popup, (self.settings_popup_pos[0] + window_pos[0],
                                           self.settings_popup_pos[1] + window_pos[1]))

        if self.easy_button_rect.collidepoint(possouris):
            surface.blit(self.easy_button_hover, self.easy_button_rect)
        else:
            surface.blit(self.easy_button, self.easy_button_rect)

        if self.normal_button_rect.collidepoint(possouris):
            surface.blit(self.normal_button_hover, self.normal_button_rect)
        else:
            surface.blit(self.normal_button,  self.normal_button_rect)

        if self.hard_button_rect.collidepoint(possouris):
            surface.blit(self.hard_button_hover, self.hard_button_rect)
        else:
            surface.blit(self.hard_button, self.hard_button_rect)

    def update_preview_ennemy(self, surface, window_pos, possouris):
        pk = self.ennemy_pks[self.difficult]
        surface.blit(self.ennemy_pk_popup, (self.ennemy_pk_popup_pos[0] + window_pos[0], self.ennemy_pk_popup_pos[1] + window_pos[1]))

        icon = pygame.transform.scale(pk.get_icon(), (300, 150))
        name = self.ennemy_pk_name_font.render(f"{pk.get_name()}  Lv.{pk.get_level()}", False, (0, 0, 0))

        surface.blit(icon, (455 + window_pos[0], 273 + window_pos[1]), (0, 0, 150, 150))
        surface.blit(name, (617 + window_pos[0], 317 + window_pos[1]))

        if not self.ennemy_pk_info_stats_mode:
            type1 = self.ennemy_pk_type_font.render(game_infos.type_names_to_print[pk.get_type()], False,
                                                    game_infos.get_type_color(pk.get_type()))
            surface.blit(type1, (670 + window_pos[0], 346 + window_pos[1]))

            if not pk.get_type2() == 'NoType':
                type2 = self.ennemy_pk_type_font.render(
                    game_infos.type_names_to_print[pk.get_type2()], False,
                    game_infos.get_type_color(pk.get_type2()))
                surface.blit(type2, (675 + type1.get_width() + window_pos[0], 346 + window_pos[1]))

            if self.difficult == 'easy':
                text = 'EASY'
                color = (0, 140, 0)
            elif self.difficult == 'normal':
                text = 'NORMAL'
                color = (255, 180, 0)
            else:
                text = 'HARD'
                color = (150, 0, 0)

            surface.blit(self.ennemy_pk_type_font.render(text, False, color),
                         (700 + window_pos[0], 367 + window_pos[1]))

        else:
            surface.blit(self.ennemy_pk_infos_stats, (612 + window_pos[0], 352 + window_pos[1]))

            pk_stats = pk.get_stats()

            surface.blit(self.ennemy_pk_stats_font.render(str(pk_stats[0]), False, (2, 137, 0)), (653 + window_pos[0],
                                                                                             348 + window_pos[1]))
            surface.blit(self.ennemy_pk_stats_font.render(str(pk_stats[1]), False, (189, 0, 0)), (653 + window_pos[0],
                                                                                             373 + window_pos[1]))
            surface.blit(self.ennemy_pk_stats_font.render(str(pk_stats[2]), False, (191, 200, 0)), (749 + window_pos[0],
                                                                                             348 + window_pos[1]))
            surface.blit(self.ennemy_pk_stats_font.render(str(pk_stats[3]), False, (0, 139, 230)), (749 + window_pos[0],
                                                                                             373 + window_pos[1]))

        if self.ennemy_pk_infos_stats_button_rect.collidepoint(possouris):
            surface.blit(self.ennemy_pk_infos_stats_button_hover, self.ennemy_pk_infos_stats_button_rect)
        else:
            surface.blit(self.ennemy_pk_infos_stats_button, self.ennemy_pk_infos_stats_button_rect)

    def set_difficult(self, diff_value='easy'):
        self.difficult = diff_value

    def set_ennemy_pokemons(self):
        self.ennemy_pks = {
            'easy': self.spawn_ennemy_pk('easy'),
            'normal': self.spawn_ennemy_pk('normal'),
            'hard': self.spawn_ennemy_pk('hard')
        }

    def get_spawn_ennemy_pk(self, difficult):

        if self.training_pk is None:
            return None

        random.seed(self.training_pk.random_seed + self.game.general_seed)

        all_spawnable_pk = game_infos.get_all_diff_pokemons(self.training_pk.get_type(), difficult)
        pokemon_name = random.choice(all_spawnable_pk)

        return pokemon_name

    def spawn_ennemy_pk(self, difficult):
        ennemy_pk_name = self.get_spawn_ennemy_pk(difficult)
        if ennemy_pk_name is None:
            return None

        min_lv = round(0.6*self.game.player.get_moyenne_team() + self.game.player.get_level())
        max_lv = round(1.2*self.game.player.get_moyenne_team() + self.game.player.get_level())
        ennemy_pk_lv = random.randint(min_lv, max_lv)

        return pokemon.Pokemon(self.get_spawn_ennemy_pk(difficult), ennemy_pk_lv, self.game.player)

    def open_settings_popup(self):
        self.boolSettings_popup = True

    def close_settings_popup(self):
        self.boolSettings_popup = False

    def update_rects_pos(self, window_pos):
        self.settings_button_rect = pygame.Rect(22 + window_pos[0], 90 + window_pos[1], 90, 120)
        self.add_button_rect = image.get_custom_rect(self.add_button, self.add_button_pos[0] + window_pos[0],
                                                                      self.add_button_pos[1] + window_pos[1])
        self.easy_button_rect = image.get_custom_rect(self.easy_button, self.easy_button_pos[0] + window_pos[0],
                                                      self.easy_button_pos[1] + window_pos[1])
        self.normal_button_rect = image.get_custom_rect(self.normal_button, self.normal_button_pos[0] + window_pos[0],
                                                      self.normal_button_pos[1] + window_pos[1])
        self.hard_button_rect = image.get_custom_rect(self.hard_button, self.hard_button_pos[0] + window_pos[0],
                                                      self.hard_button_pos[1] + window_pos[1])
        self.training_pk_rect = pygame.Rect(111 + window_pos[0], 123 + window_pos[1], 252, 252)
        self.ennemy_pk_infos_stats_button_rect = image.get_custom_rect(self.ennemy_pk_infos_stats_button,
                                                                       715 + window_pos[0], 408 + window_pos[1])
        self.fight_button_rect = image.get_custom_rect(self.fight_button, self.fight_button_pos[0] + window_pos[0],
                                                       self.fight_button_pos[1] + window_pos[1])

    def is_hovering_settings_popup_buttons(self, possouris):
        if self.boolSettings_popup:
            return (self.easy_button_rect.collidepoint(possouris) or self.normal_button_rect.collidepoint(possouris) or
                    self.hard_button_rect.collidepoint(possouris))
        else:
            return False

    def is_hovering_buttons(self, possouris):
        return (self.settings_button_rect.collidepoint(possouris)
                or self.is_hovering_settings_popup_buttons(possouris)
                or (self.add_button_rect.collidepoint(possouris) and self.training_pk is None and not self.add_training_pk_mode)
                or (self.training_pk_rect.collidepoint(possouris) and self.training_pk is not None)
                or (self.choose_training_pk_popup.is_hovering(possouris) and self.add_training_pk_mode)
                or (self.ennemy_pk_infos_stats_button_rect.collidepoint(possouris) and self.training_pk is not None)
                or (self.fight_button_rect.collidepoint(possouris) and self.training_pk is not None)
                )

    def create_rect_alpha(self, dimensions, color, opacite=90):
        rect = pygame.Surface(dimensions)
        rect.set_alpha(opacite)
        rect.fill(color)
        return rect

    def load_image(self, file_name, boolTransfromScale=False, size=None):
        image = pygame.image.load(self.path + file_name)

        if boolTransfromScale:
            image = pygame.transform.scale(image, size)

        return image


class ChooseTrainingPkPopup:

    def __init__(self, game):
        self.game = game
        self.path = 'assets/game/ingame_windows/Train/'
        self.popup = self.load_image('choose_training_pk_popup.png')
        self.x_button = self.load_image('choose_training_pk_x_button.png')
        self.x_button_hover = self.load_image('choose_training_pk_x_button_hover.png')

        self.popup_pos = (419, 40)
        self.x_button_pos = (802, 57)
        self.x_button_rect = image.get_custom_rect(self.x_button, self.x_button_pos[0], self.x_button_pos[1])

        self.pk_emps = ChooseTrainingPkEmps(self.game)

    def update(self, surface, possouris, window_pos):
        self.update_rects_pos(window_pos)

        surface.blit(self.popup, (self.popup_pos[0] + window_pos[0],
                                  self.popup_pos[1] + window_pos[1]))

        if self.x_button_rect.collidepoint(possouris):
            surface.blit(self.x_button_hover, self.x_button_rect)
        else:
            surface.blit(self.x_button, self.x_button_rect)

        self.pk_emps.update(surface, window_pos, possouris)

    def update_rects_pos(self, window_pos):
        self.x_button_rect = image.get_custom_rect(self.x_button, self.x_button_pos[0] + window_pos[0],
                                                                  self.x_button_pos[1] + window_pos[1])

    def is_hovering(self, possouris):
        return self.x_button_rect.collidepoint(possouris) or self.pk_emps.is_hovering_emp(possouris)

    def load_image(self, file_name, boolTransfromScale=False, size=None):
        image = pygame.image.load(self.path + file_name)

        if boolTransfromScale:
            image = pygame.transform.scale(image, size)

        return image


class ChooseTrainingPkEmps:

    def __init__(self, game):
        self.game = game

        self.emp1 = PkEmp(self.game, 0, (432, 103), self)
        self.emp2 = PkEmp(self.game, 1, (567, 103), self)
        self.emp3 = PkEmp(self.game, 2, (702, 103), self)
        self.emp4 = PkEmp(self.game, 3, (432, 232), self)
        self.emp5 = PkEmp(self.game, 4, (567, 232), self)
        self.emp6 = PkEmp(self.game, 5, (702, 232), self)

        self.emp_moving = False

    def update(self, surface, window_pos, possouris):
        self.emp1.update(surface, window_pos, possouris)
        self.emp2.update(surface, window_pos, possouris)
        self.emp3.update(surface, window_pos, possouris)
        self.emp4.update(surface, window_pos, possouris)
        self.emp5.update(surface, window_pos, possouris)
        self.emp6.update(surface, window_pos, possouris)

    def is_another_pk_moving(self):
        return (self.emp1.moving or
                self.emp2.moving or
                self.emp3.moving or
                self.emp4.moving or
                self.emp5.moving or
                self.emp6.moving)

    def is_hovering_emp(self, possouris):
        return (self.emp1.is_hovering(possouris)
                or self.emp2.is_hovering(possouris)
                or self.emp3.is_hovering(possouris)
                or self.emp4.is_hovering(possouris)
                or self.emp5.is_hovering(possouris)
                or self.emp6.is_hovering(possouris)
                )


class PkEmp:

    def __init__(self, game, i, pos, emp_group):
        self.game = game
        self.group = emp_group
        self.i = i
        self.POS = pos
        self.pos = pos
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 120, 120)

        self.pk = self.game.player.team[self.i]

        self.moving = False
        self.clic_pos = (0, 0)

    def update(self, surface, window_pos, possouris):
        self.update_rects_pos(window_pos)
        self.update_pk()

        if self.pk is not None:
            if self.moving:
                surface.blit(self.create_rect_alpha((self.rect.w - 10, self.rect.h - 10), (255, 255, 255)),
                             (self.rect.x + 5, self.rect.y + 5))
            else:
                if self.rect.collidepoint(possouris) and not self.group.is_another_pk_moving():
                    surface.blit(self.create_rect_alpha((self.rect.w - 10, self.rect.h - 10), (255, 255, 255)),
                                 (self.rect.x + 5, self.rect.y + 5))

            surface.blit(pygame.transform.scale(self.pk.get_icon(), (250, 125)),
                         (self.rect[0] - 5, self.rect[1] - 15), (0, 0, 125, 125))

            if not self.moving:
                if not self.group.is_another_pk_moving():
                    if self.game.mouse_pressed[1] and self.rect.collidepoint(possouris):
                        self.moving = True
                        self.clic_pos = possouris
            else:
                if not self.game.mouse_pressed[1]:
                    if self.game.classic_panel.ingame_window.train_panel.add_button_rect.collidepoint(possouris):
                        self.game.classic_panel.ingame_window.train_panel.training_pk = self.game.player.team[self.i]
                        self.game.classic_panel.ingame_window.train_panel.set_ennemy_pokemons()
                        self.game.classic_panel.ingame_window.train_panel.add_training_pk_mode = False
                    self.moving = False
                    self.pos = self.POS
                else:
                    self.pos = (self.POS[0] + possouris[0] - self.clic_pos[0],
                                self.POS[1] + possouris[1] - self.clic_pos[1])

    def update_pk(self):
        if not self.game.player.team[self.i] == self.pk:
            self.pk = self.game.player.team[self.i]

    def update_rects_pos(self, window_pos):
        self.rect = pygame.Rect(self.pos[0] + window_pos[0], self.pos[1] + window_pos[1], 120, 120)

    def is_hovering(self, possouris):
        return self.rect.collidepoint(possouris) and self.pk is not None

    def create_rect_alpha(self, dimensions, color):
        rect = pygame.Surface(dimensions)
        rect.set_alpha(90)
        rect.fill(color)
        return rect
