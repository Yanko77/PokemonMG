import pygame
import image
import pokemon
import random
import game_infos


class TrainPanel:

    def __init__(self, game):
        self.game = game
        # LOADING IMAGES --------------------------
        self.background = image.load_image('assets/game/ingame_windows/Train/background.png')
        self.emp_training_pk = image.load_image('assets/game/ingame_windows/Train/emp_training_pk.png')

        # LOADING FONTS ---------------------
        self.difficulty_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 36)
        self.lv_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 45)
        self.ennemy_pk_name_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 36)

        # DEFAULT VARIABLES --------------------------
        self.difficult = None
        self.training_pk = None
        self.ennemy_pks = {
            'easy': self.spawn_ennemy_pk('easy'),
            'normal': self.spawn_ennemy_pk('normal'),
            'hard': self.spawn_ennemy_pk('hard'),
            None: None
        }

    def update(self, surface, possouris, window_pos):
        surface.blit(self.background, (window_pos[0], window_pos[1]))

        if self.training_pk is not None:
            self.update_preview_ennemy(surface, window_pos)

        self.update_emp_training_pk(surface, possouris, window_pos)

    def update_emp_training_pk(self, surface, possouris, window_pos):
        surface.blit(self.emp_training_pk, (83 + window_pos[0], 97 + window_pos[1]))
        if self.difficult == 'easy':
            text = 'EASY'
            color = (31, 83, 0)
            pos = (299, 410)
        elif self.difficult == 'normal':
            text = 'NORM'
            color = (199, 89, 0)
            pos = (291, 410)
        elif self.difficult == 'hard':
            text = 'HARD'
            color = (140, 0, 0)
            pos = (295, 410)
        else:
            text = 'NONE'
            color = (32, 32, 32)
            pos = (295, 410)

        x = pos[0] + window_pos[0]
        y = pos[1] + window_pos[1]
        pos = (x, y)

        surface.blit(self.difficulty_font.render(text, False, color), pos)

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

    def create_rect_alpha(self, dimensions, color, opacite=90):
        rect = pygame.Surface(dimensions)
        rect.set_alpha(opacite)
        rect.fill(color)
        return rect
