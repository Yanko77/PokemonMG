import pygame

import spawn
import train
import image
import sac
import starters
import items
pygame.font.init()


class IngameWindow:

    def __init__(self, name, game):
        self.is_open = False
        self.is_minimized = False

        self.game = game

        self.name = name[0].upper() + name[1:].lower()
        self.icon = pygame.image.load('assets/game/ingame_windows/' + self.name + '/icon.png')

        self.basic_window = pygame.image.load('assets/game/ingame_windows/basic/main.png')
        self.basic_window_pos = [1, 1]

        self.basic_window_rect = self.basic_window.get_rect()
        self.basic_window_rect.x = 20 + self.basic_window_pos[0]
        self.basic_window_rect.y = 0 + self.basic_window_pos[1]
        self.basic_window_rect.w = 870
        self.basic_window_rect.h = 528

        self.basic_window_bar_rect = pygame.Rect(20, 0, 870, 39)

        self.min_window = pygame.image.load('assets/game/ingame_windows/basic/min_main.png')
        self.min_window_pos = [22, 675]

        self.min_window_rect = self.min_window.get_rect()
        self.min_window_rect.x = self.min_window_pos[0]
        self.min_window_rect.y = self.min_window_pos[1]

        self.min_window_hover = pygame.image.load('assets/game/ingame_windows/basic/min_main_hover.png')

        self.main_window_rect = self.basic_window.get_rect()
        self.main_window_rect.x = 20
        self.main_window_rect.w = 872
        self.main_window_rect.h = 528

        self.main_window_bar_rect = self.basic_window_bar_rect

        self.main_window_pos = [1, 1]
        self.moving = False
        self.rel_pos = (0, 0)

        self.buttons = image.IngameWindowButtons()

        self.title_font = pygame.font.Font('assets/fonts/Impact.ttf', 30)
        self.title = self.title_font.render(self.name, False, (0, 0, 0))
        self.title_marge = 75

        self.sac_panel = sac.SacIngamePanel(self.game)
        self.starters_panel = starters.StartersPanel(self.game)
        self.spawn_panel = spawn.SpawnPanel(self.game)
        self.train_panel = None  # Sera initialisé après la sélection du starter
        self.items_panel = items.ItemsPanel(self.game)

    def update(self, surface, possouris):
        self.update_main_window_rect()

        if self.is_open:
            if self.is_minimized:
                surface.blit(self.min_window, self.main_window_pos)
                surface.blit(self.icon, (self.main_window_pos[0]-20, self.main_window_pos[1]+3))
                if self.name == "Sac d'objets":
                    surface.blit(self.title_font.render("Sac", False, (0, 0, 0)), (self.main_window_pos[0] + self.title_marge-20, self.main_window_pos[1] + 0))
                else:
                    surface.blit(self.title, (self.main_window_pos[0] + self.title_marge-20, self.main_window_pos[1] + 0))

                if self.min_window_rect.collidepoint(possouris):
                    surface.blit(self.min_window_hover, self.main_window_pos)
            else:
                surface.blit(self.basic_window, self.main_window_pos)
                surface.blit(self.title, (self.main_window_pos[0] + self.title_marge, self.main_window_pos[1] + 0))
                surface.blit(self.icon, self.main_window_pos)
                self.buttons.update(surface, possouris)
                self.update_panel(surface, possouris)

    def is_hovering_buttons(self, possouris):
        if self.buttons.is_hovering_buttons(possouris):
            return True
        elif self.name == "Sac d'objets":
            if self.sac_panel.is_hovering_buttons(possouris, self.main_window_pos):
                return True
        elif self.name == 'Starters':
            if self.starters_panel.is_hovering_buttons(possouris):
                return True
        elif self.name == 'Spawn':
            if self.spawn_panel.is_hovering_buttons(possouris):
                return True
        elif self.name == 'Train':
            if self.train_panel.is_hovering_buttons(possouris):
                return True
        return False

    def init_train_panel(self):
        self.train_panel = train.TrainPanel(self.game)

    def update_main_window_rect(self):
        if self.is_open:
            if self.is_minimized:
                self.main_window_rect = self.min_window.get_rect()
                self.main_window_rect.x = self.min_window_pos[0]
                self.main_window_rect.y = self.min_window_pos[1]
                self.main_window_pos = self.min_window_pos

                self.main_window_bar_rect = pygame.Rect(0, 0, 0, 0)
            else:
                self.main_window_rect = self.basic_window.get_rect()
                self.main_window_rect.x = 20 + self.main_window_pos[0]
                self.main_window_rect.y = 0 + self.main_window_pos[1]
                self.main_window_rect.w = 870
                self.main_window_rect.h = 528
                self.main_window_pos = self.basic_window_pos

                self.main_window_bar_rect = pygame.Rect(20+self.main_window_pos[0], 0+self.main_window_pos[1], 870, 39)
                self.buttons.x_button_rect.x = 854 + self.main_window_pos[0]
                self.buttons.x_button_rect.y = 4 + self.main_window_pos[1]
                self.buttons.min_button_rect.x = 816 + self.main_window_pos[0]
                self.buttons.min_button_rect.y = 4 + self.main_window_pos[1]
        else:
            self.main_window_rect = pygame.Rect(0, 0, 0, 0)
            self.main_window_bar_rect = pygame.Rect(0, 0, 0, 0)

    def update_panel(self, surface, possouris):
        if self.name == "Sac d'objets":
            self.sac_panel.update(surface, possouris, self.main_window_pos)
        elif self.name == "Starters":
            self.starters_panel.update(surface, possouris, self.main_window_pos)
        elif self.name == "Spawn":
            self.spawn_panel.update(surface, possouris, self.main_window_pos)
        elif self.name == "Train":
            self.train_panel.update(surface, possouris, self.main_window_pos)

    def update_name(self, new_name):
        self.name = new_name[0].upper() + new_name[1:].lower()
        self.title = self.title_font.render(self.name, False, (0, 0, 0))
        self.icon = pygame.image.load('assets/game/ingame_windows/' + self.name + '/icon.png')
        self.update_title_marge()

    def update_title_marge(self):
        if self.name == 'Spawn':
            self.title_marge = 75
        if self.name == 'Train':
            self.title_marge = 70
        if self.name == 'Grind':
            self.title_marge = 95
        if self.name == 'Items':
            self.title_marge = 70
        if self.name == 'Evolutions':
            self.title_marge = 75
        if self.name == 'Starters':
            self.title_marge = 120
        if self.name == "Sac d'objets":
            self.title_marge = 105

    def open(self):
        self.is_open = True

    def close(self):
        self.update_main_window_rect()
        self.is_open = False
        self.is_minimized = False

    def minimize(self):
        self.update_main_window_rect()
        self.is_minimized = True

    def maximize(self):
        self.update_main_window_rect()
        self.is_minimized = False

'''
if game.classic_panel.ingame_window.is_minimized:
    game.classic_panel.ingame_window.maximize()
elif game.classic_panel.ingame_window.is_open:
    if game.classic_panel.ingame_window.buttons.x_button_rect.collidepoint(posSouris):
        if not game.classic_panel.ingame_window.current_panel_name == 'Starters':
            game.classic_panel.ingame_window.close()
        elif game.is_starter_selected:
            game.classic_panel.ingame_window.close()
    elif game.classic_panel.ingame_window.buttons.min_button_rect.collidepoint(posSouris):
        game.classic_panel.ingame_window.minimize()
    elif game.classic_panel.ingame_window.current_panel_name == "Sac d'objets":
        if game.classic_panel.ingame_window.sac_panel.page1_rect.collidepoint(posSouris):
            game.classic_panel.ingame_window.sac_panel.change_page(1)
        elif game.classic_panel.ingame_window.sac_panel.page2_rect.collidepoint(posSouris):
            game.classic_panel.ingame_window.sac_panel.change_page(2)
    elif game.classic_panel.ingame_window.current_panel_name == 'Starters':
        if game.classic_panel.ingame_window.starters_panel.pk_rects[0].collidepoint(
                posSouris):
            game.classic_panel.ingame_window.starters_panel.decouvrir_pk(0)
        elif game.classic_panel.ingame_window.starters_panel.pk_rects[1].collidepoint(
                posSouris):
            game.classic_panel.ingame_window.starters_panel.decouvrir_pk(1)
        elif game.classic_panel.ingame_window.starters_panel.pk_rects[2].collidepoint(
                posSouris):
            game.classic_panel.ingame_window.starters_panel.decouvrir_pk(2)
    elif game.classic_panel.ingame_window.current_panel_name == 'Spawn':
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
    elif game.classic_panel.ingame_window.current_panel_name == 'Train':
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
            elif game.classic_panel.ingame_window.train_panel.fight_button_rect.collidepoint(posSouris):
                game.classic_panel.ingame_window.train_panel.start_training_fight()
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if game.classic_panel.ingame_window.train_panel.add_training_pk_mode:
            if game.classic_panel.ingame_window.train_panel.choose_training_pk_popup.x_button_rect.collidepoint(posSouris):
                game.classic_panel.ingame_window.train_panel.add_training_pk_mode = False'''