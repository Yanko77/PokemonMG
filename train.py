import pygame
import image
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
        self.pk_selected_indicator = self.load_image('pk_selected_indicator.png')
        self.settings_button = self.load_image('settings_button.png')
        self.settings_button_hover = self.load_image('settings_button_hover.png')
        self.diff_ind_easy = self.load_image('diff_ind_easy.png')
        self.diff_ind_normal = self.load_image('diff_ind_normal.png')
        self.diff_ind_hard = self.load_image('diff_ind_hard.png')

        # LOADING FONTS ---------------------
        self.difficulty_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 35)
        self.lv_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 45)
        self.ennemy_pk_name_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 36)

        # DEFAULT VARIABLES --------------------------
        self.background_pos = (-13, -21)
        self.emp_training_pk_pos = (79, 79)
        self.pk_selected_indicator_pos = (135, 414)
        self.settings_button_rect = pygame.Rect(30, 97, 54, 84)
        self.settings_button_pos = (34, 101)
        self.diff_ind_pos = (80, 81)

        self.difficult = 'easy'
        self.training_pk = None
        self.ennemy_pks = {
            'easy': self.spawn_ennemy_pk('easy'),
            'normal': self.spawn_ennemy_pk('normal'),
            'hard': self.spawn_ennemy_pk('hard')
        }

    def update(self, surface, possouris, window_pos):
        self.update_rects_pos(window_pos)

        surface.blit(self.background, (window_pos[0] + self.background_pos[0], window_pos[1] + self.background_pos[1]))

        if self.training_pk is not None:
            self.update_preview_ennemy(surface, window_pos)

        self.update_emp_training_pk(surface, possouris, window_pos)

    def update_emp_training_pk(self, surface, possouris, window_pos):
        surface.blit(self.emp_training_pk, (self.emp_training_pk_pos[0] + window_pos[0],
                                            self.emp_training_pk_pos[1] + window_pos[1]))
        if self.difficult == 'easy':
            color = (0, 150, 0)
            surface.blit(self.diff_ind_easy, (self.diff_ind_pos[0] + window_pos[0],
                                              self.diff_ind_pos[1] + window_pos[1]))
        elif self.difficult == 'normal':
            color = (255, 150, 0)
            surface.blit(self.diff_ind_normal, (self.diff_ind_pos[0] + window_pos[0],
                                              self.diff_ind_pos[1] + window_pos[1]))
        elif self.difficult == 'hard':
            color = (130, 0, 0)
            surface.blit(self.diff_ind_hard, (self.diff_ind_pos[0] + window_pos[0],
                                              self.diff_ind_pos[1] + window_pos[1]))

        surface.blit(self.difficulty_font.render(self.difficult.upper(), False, color), (160 + window_pos[0],
                                                                                         51 + window_pos[1]))

        if self.settings_button_rect.collidepoint(possouris):
            surface.blit(self.settings_button_hover, (self.settings_button_pos[0] + window_pos[0],
                                                      self.settings_button_pos[1] + window_pos[1]))
        else:
            surface.blit(self.settings_button, (self.settings_button_pos[0] + window_pos[0],
                                                self.settings_button_pos[1] + window_pos[1]))

        if self.training_pk is None:
            surface.blit(self.pk_selected_indicator, (self.pk_selected_indicator_pos[0] + window_pos[0],
                                                      self.pk_selected_indicator_pos[1] + window_pos[1]))

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

    def get_spawn_ennemy_pk(self, difficult):

        if self.training_pk is None:
            return None

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

    def update_rects_pos(self, window_pos):
        self.settings_button_rect = pygame.Rect(20 + window_pos[0], 87 + window_pos[1], 75, 105)

    def is_hovering_buttons(self, possouris):
        return self.settings_button_rect.collidepoint(possouris)

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
