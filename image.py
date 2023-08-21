import pygame
import animation
import random
pygame.font.init()



class Image(animation.AnimateImage):

    def __init__(self, nb_images, image_name):
        super().__init__(nb_images, image_name)
        self.final_image_num = nb_images - 1
        self.loop = False
        self.pas = 1

    def update_animation(self):
        self.animate(loop=self.loop, final_image_num=self.final_image_num, pas=self.pas)


class Background(Image):

    def __init__(self):
        super().__init__(24, "Background")
        self.pas = 2
        self.start_animation()


class GameBar(Image):

    def __init__(self):
        super().__init__(24, 'game_bar')
        self.start_animation()


class RandomPokemon:

    def __init__(self):
        self.is_animation_over = False
        self.after_animation_over_compteur = 0

        self.num = random.randint(0, 8)
        self.image = pygame.image.load(f'assets/accueil/pokemons/{self.num}.png')
        self.image.set_alpha(0)

        self.image_opacity = 0

    def update_animation(self):
        self.image.set_alpha(self.image_opacity)
        if self.image_opacity < 255:
            self.image_opacity += 10
        else:
            if not self.is_animation_over:
                self.after_animation_over_compteur += 1
            if self.after_animation_over_compteur > 20:
                self.is_animation_over = True


class IntroAccueil(Image):

    def __init__(self):
        super().__init__(147, 'intro')
        self.start_animation()
        self.pas = 2


class CursorChangePseudoMode:

    def __init__(self):
        self.image = pygame.image.load('assets/game/panels/classic_panel/curseur_changement_pseudo.png')

        self.compteur_animation = 0

    def update(self, surface, player_name_pixels=0):
        self.compteur_animation += 1

        if self.compteur_animation < 25:
            surface.blit(self.image, (1+player_name_pixels, 1))

        if self.compteur_animation > 57:
            self.compteur_animation = 0


class AccueilButtons:

    def __init__(self):
        self.start_game = pygame.image.load('assets/accueil/Buttons/Start_game/start_game.png')
        self.start_game_rect = self.start_game.get_rect()
        self.start_game_rect.x = 30
        self.start_game_rect.y = 155
        self.start_game_h = pygame.image.load('assets/accueil/Buttons/Start_game/start_game_hover.png')

        self.settings = pygame.image.load('assets/accueil/Buttons/Settings/settings.png')
        self.settings = pygame.transform.scale(self.settings, (422, 83))
        self.settings_rect = self.settings.get_rect()
        self.settings_rect.x = 30
        self.settings_rect.y = 280
        self.settings_h = pygame.image.load('assets/accueil/Buttons/Settings/settings_hover.png')
        self.settings_h = pygame.transform.scale(self.settings_h, (422, 83))

        self.credits = pygame.image.load('assets/accueil/Buttons/Credits/credits.png')
        self.credits = pygame.transform.scale(self.credits, (359, 83))
        self.credits_rect = self.settings.get_rect()
        self.credits_rect.x = 30
        self.credits_rect.y = 390
        self.credits_h = pygame.image.load('assets/accueil/Buttons/Credits/credits_hover.png')
        self.credits_h = pygame.transform.scale(self.credits_h, (359, 83))

        self.quit = pygame.image.load('assets/accueil/Buttons/Quit/quit.png')
        self.quit = pygame.transform.scale(self.quit, (213, 91))
        self.quit_rect = self.quit.get_rect()
        self.quit_rect.x = 30
        self.quit_rect.y = 500

        self.quit_h = pygame.image.load('assets/accueil/Buttons/Quit/quit_hover.png')
        self.quit_h = pygame.transform.scale(self.quit_h, (213, 91))

    def update(self, surface, possouris, basic_accueil:bool):
        if self.start_game_rect.collidepoint(possouris) and basic_accueil:
            surface.blit(self.start_game_h, self.start_game_rect)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            surface.blit(self.start_game, self.start_game_rect)

        if self.settings_rect.collidepoint(possouris) and basic_accueil:
            surface.blit(self.settings_h, self.settings_rect)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            surface.blit(self.settings, self.settings_rect)

        if self.credits_rect.collidepoint(possouris) and basic_accueil:
            surface.blit(self.credits_h, self.credits_rect)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            surface.blit(self.credits, self.credits_rect)

        if self.quit_rect.collidepoint(possouris) and basic_accueil:
            surface.blit(self.quit_h, self.quit_rect)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            surface.blit(self.quit, self.quit_rect)

        if basic_accueil:
            if not (self.quit_rect.collidepoint(possouris) or self.start_game_rect.collidepoint(possouris) or
                    self.credits_rect.collidepoint(possouris) or self.settings_rect.collidepoint(possouris)):

                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


class ClassicGamePanelButtons:

    def __init__(self):
        self.unlocked_buttons = {'Spawn': True,
                                 'Train': True,
                                 'Grind': False,
                                 'Items': False,
                                 'Evol': True
                                 }
        # SPAWN BUTTON
        self.spawn_button = pygame.image.load('assets/game/panels/classic_panel/spawn_button.png')
        self.spawn_button_rect = self.spawn_button.get_rect()
        self.spawn_button_rect.x = 20 + 22
        self.spawn_button_rect.y = 12 + 126
        self.spawn_button_rect.w = 250
        self.spawn_button_rect.h = 250

        self.spawn_button_hover = pygame.image.load('assets/game/panels/classic_panel/spawn_button_hover.png')

        self.spawn_button_pos = (22, 126)

        # TRAIN BUTTON
        self.train_button = pygame.image.load('assets/game/panels/classic_panel/train_button.png')
        self.train_button_rect = self.train_button.get_rect()
        self.train_button_rect.x = 20 + 307
        self.train_button_rect.y = 12 + 126
        self.train_button_rect.w = 250
        self.train_button_rect.h = 250

        self.train_button_hover = pygame.image.load('assets/game/panels/classic_panel/train_button_hover.png')

        self.train_button_pos = (307, 126)

        # GRIND BUTTON
        self.grind_button = pygame.image.load('assets/game/panels/classic_panel/grind_button.png')
        self.grind_button_rect = self.grind_button.get_rect()
        self.grind_button_rect.x = 20 + 592
        self.grind_button_rect.y = 12 + 126
        self.grind_button_rect.w = 250
        self.grind_button_rect.h = 250

        self.grind_button_hover = pygame.image.load('assets/game/panels/classic_panel/grind_button_hover.png')

        self.grind_button_pos = (592, 126)

        # ITEMS BUTTON
        self.items_button = pygame.image.load('assets/game/panels/classic_panel/items_button.png')
        self.items_button_rect = self.items_button.get_rect()
        self.items_button_rect.x = 20 + 58
        self.items_button_rect.y = 12 + 410
        self.items_button_rect.w = 250
        self.items_button_rect.h = 250

        self.items_button_hover = pygame.image.load('assets/game/panels/classic_panel/items_button_hover.png')

        self.items_button_pos = (58, 410)

        # EVOL BUTTON
        self.evol_button = pygame.image.load('assets/game/panels/classic_panel/evol_button.png')
        self.evol_button_rect = self.evol_button.get_rect()
        self.evol_button_rect.x = 20 + 342
        self.evol_button_rect.y = 12 + 410
        self.evol_button_rect.w = 250
        self.evol_button_rect.h = 250

        self.evol_button_hover = pygame.image.load('assets/game/panels/classic_panel/evol_button_hover.png')

        self.evol_button_pos = (342, 410)

    def update(self, surface, possouris, ingame_window):

        if self.unlocked_buttons['Spawn']:
            if self.spawn_button_rect.collidepoint(possouris) and not ingame_window.main_window_rect.collidepoint(possouris):
                surface.blit(self.spawn_button, self.spawn_button_pos)
                surface.blit(self.spawn_button_hover, self.spawn_button_pos)
            else:
                surface.blit(self.spawn_button, self.spawn_button_pos)

        if self.unlocked_buttons['Train']:
            if self.train_button_rect.collidepoint(possouris) and not ingame_window.main_window_rect.collidepoint(possouris):
                surface.blit(self.train_button, self.train_button_pos)
                surface.blit(self.train_button_hover, self.train_button_pos)
            else:
                surface.blit(self.train_button, self.train_button_pos)

        if self.unlocked_buttons['Grind']:
            if self.grind_button_rect.collidepoint(possouris) and not ingame_window.main_window_rect.collidepoint(possouris):
                surface.blit(self.grind_button, self.grind_button_pos)
                surface.blit(self.grind_button_hover, self.grind_button_pos)
            else:
                surface.blit(self.grind_button, self.grind_button_pos)

        if self.unlocked_buttons['Items']:
            if self.items_button_rect.collidepoint(possouris) and not ingame_window.main_window_rect.collidepoint(possouris):
                surface.blit(self.items_button, self.items_button_pos)
                surface.blit(self.items_button_hover, self.items_button_pos)
            else:
                surface.blit(self.items_button, self.items_button_pos)

        if self.unlocked_buttons['Evol']:
            if self.evol_button_rect.collidepoint(possouris) and not ingame_window.main_window_rect.collidepoint(possouris):
                surface.blit(self.evol_button, self.evol_button_pos)
                surface.blit(self.evol_button_hover, self.evol_button_pos)
            else:
                surface.blit(self.evol_button, self.evol_button_pos)

    def is_hovering_button(self, possouris):
        '''
        if not self.spawn_button_rect.collidepoint(possouris) and not self.train_button_rect.collidepoint(possouris):
            if not self.grind_button_rect.collidepoint(possouris) and not self.items_button_rect.collidepoint(
                    possouris):
                if not self.evol_button_rect.collidepoint(possouris):
                    return False
        return True'''
        if self.spawn_button_rect.collidepoint(possouris):
            if self.unlocked_buttons['Spawn']:
                return True
        elif self.train_button_rect.collidepoint(possouris):
            if self.unlocked_buttons['Train']:
                return True
        elif self.grind_button_rect.collidepoint(possouris):
            if self.unlocked_buttons['Grind']:
                return True
        elif self.items_button_rect.collidepoint(possouris):
            if self.unlocked_buttons['Items']:
                return True
        elif self.evol_button_rect.collidepoint(possouris):
            if self.unlocked_buttons['Evol']:
                return True
        else:
            return False


class IngameWindowButtons:

    def __init__(self):
        self.x_button = pygame.image.load('assets/game/ingame_windows/basic/x_button.png')
        self.x_button_rect = self.x_button.get_rect()
        self.x_button_rect.x = 854
        self.x_button_rect.y = 4

        self.x_button_hover = pygame.image.load('assets/game/ingame_windows/basic/x_button_hover.png')

        self.min_button = pygame.image.load('assets/game/ingame_windows/basic/min_button.png')
        self.min_button_rect = self.min_button.get_rect()
        self.min_button_rect.x = 816
        self.min_button_rect.y = 4

        self.min_button_hover = pygame.image.load('assets/game/ingame_windows/basic/min_button_hover.png')

    def update(self, surface, possouris):

        if self.x_button_rect.collidepoint(possouris):
            surface.blit(self.x_button_hover, self.x_button_rect)

        else:
            surface.blit(self.x_button, self.x_button_rect)

        if self.min_button_rect.collidepoint(possouris):
            surface.blit(self.min_button_hover, self.min_button_rect)

        else:
            surface.blit(self.min_button, self.min_button_rect)

    def is_hovering_buttons(self, possouris):
        if not self.x_button_rect.collidepoint(possouris) and not self.min_button_rect.collidepoint(possouris):
            return False
        return True
