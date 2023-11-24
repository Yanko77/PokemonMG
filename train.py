import pygame
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
        # LOADING FONTS ---------------------
        self.difficulty_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 35)
        self.lv_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 45)
        self.ennemy_pk_name_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 36)
        self.info_select_pk_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 22)
        # RENDER TEXTS
        self.no_pk_selected_text = self.info_select_pk_font.render('NO POKEMON SELECTED', False, (255, 255, 255))

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

        self.difficult = 'easy'
        self.training_pk = None
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
            self.update_preview_ennemy(surface, window_pos)
        else:
            surface.blit(self.locked, (self.locked_pos[0] + window_pos[0],
                                       self.locked_pos[1] + window_pos[1]))
            surface.blit(self.no_pk_selected_text, (self.no_pk_selected_text_pos[0] + window_pos[0],
                                                    self.no_pk_selected_text_pos[1] + window_pos[1]))

        if self.boolSettings_popup:
            self.update_settings_popup(surface, possouris, window_pos)

        if self.add_training_pk_mode:
            self.choose_training_pk_popup.update(surface, possouris, window_pos)

    def update_emp_training_pk(self, surface, possouris, window_pos):

        if self.training_pk is None:
             pass

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

        if not self.add_training_pk_mode:
            if self.add_button_rect.collidepoint(possouris):
                surface.blit(self.add_button_hover, self.add_button_rect)
            else:
                surface.blit(self.add_button, self.add_button_rect)

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

    def update_preview_ennemy(self, surface, window_pos):
        bg_x = window_pos[0] + 400
        bg_y = window_pos[1] + 50
        background = self.create_rect_alpha((350, 200), (0, 0, 0), opacite=120)

        bg_pk_icon_x = window_pos[0] + 410
        bg_pk_icon_y = window_pos[1] + 60
        background_pk_icon = self.create_rect_alpha((110, 110), (255, 255, 255), opacite=70)

        border_pk_icon_x = window_pos[0] + 405
        border_pk_icon_y = window_pos[1] + 55
        border_pk_icon = self.create_rect_alpha((120, 120), (0, 0, 0), opacite=150)

        pk_icon_x = window_pos[0] + 412
        pk_icon_y = window_pos[1] + 64
        pk_icon = image.load_image(f'assets/game/pokemons_icons/{self.ennemy_pks[self.difficult].get_name()}.png', True, (190, 95))

        surface.blit(background, (bg_x, bg_y))
        surface.blit(border_pk_icon, (border_pk_icon_x, border_pk_icon_y))
        surface.blit(background_pk_icon, (bg_pk_icon_x, bg_pk_icon_y))
        surface.blit(pk_icon, (pk_icon_x, pk_icon_y), (0, 0, 95, 95))

    def set_difficult(self, diff_value='easy'):
        self.difficult = diff_value

    def set_ennemy_pokemons(self):
        self.ennemy_pks = {
            'easy': self.spawn_ennemy_pk('easy'),
            'normal': self.spawn_ennemy_pk('normal'),
            'hard': self.spawn_ennemy_pk('hard')
        }
        for pk in self.ennemy_pks.values():
            print(pk.name, pk.get_type(), pk.get_level())

    def get_spawn_ennemy_pk(self, difficult):

        if self.training_pk is None:
            return None

        random.seed(self.training_pk.random_seed)

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

        return pokemon.Pokemon(self.get_spawn_ennemy_pk(difficult), ennemy_pk_lv)

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

    def is_hovering_settings_popup_buttons(self, possouris):
        if self.boolSettings_popup:
            return (self.easy_button_rect.collidepoint(possouris) or self.normal_button_rect.collidepoint(possouris) or
                    self.hard_button_rect.collidepoint(possouris))
        else:
            return False

    def is_hovering_buttons(self, possouris):
        return (self.settings_button_rect.collidepoint(possouris) or self.add_button_rect.collidepoint(possouris)
                or self.is_hovering_settings_popup_buttons(possouris))

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

    def is_hovering_buttons(self, possouris):
        return self.x_button_rect.collidepoint(possouris)

    def load_image(self, file_name, boolTransfromScale=False, size=None):
        image = pygame.image.load(self.path + file_name)

        if boolTransfromScale:
            image = pygame.transform.scale(image, size)

        return image


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
