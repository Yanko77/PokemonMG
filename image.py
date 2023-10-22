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
        # print(player_name_pixels)
        self.compteur_animation += 1

        if self.compteur_animation < 25:
            surface.blit(self.image, (1 + player_name_pixels, 1))

        if self.compteur_animation > 57:
            self.compteur_animation = 0


class AccueilButtons:

    def __init__(self):
        ## Bouton START
        self.start_game = load_image('assets/accueil/Buttons/Start_game/start_game.png')
        self.start_game_rect = get_custom_rect(self.start_game, 30, 155)

        self.start_game_h = load_image('assets/accueil/Buttons/Start_game/start_game_hover.png')

        ## Bouton SETTINGS
        self.settings = load_image('assets/accueil/Buttons/Settings/settings.png', True, (422, 83))
        self.settings_rect = get_custom_rect(self.settings, 30, 280)

        self.settings_h = load_image('assets/accueil/Buttons/Settings/settings_hover.png', True, (422, 83))

        ## Bouton CREDITS
        self.credits = load_image('assets/accueil/Buttons/Credits/credits.png', True, (359, 83))
        self.credits_rect = get_custom_rect(self.credits, 30, 390)

        self.credits_h = load_image('assets/accueil/Buttons/Credits/credits_hover.png', True, (359, 83))

        ## Bouton QUIT
        self.quit = load_image('assets/accueil/Buttons/Quit/quit.png', True, (213, 91))
        self.quit_rect = get_custom_rect(self.quit, 30, 500)

        self.quit_h = load_image('assets/accueil/Buttons/Quit/quit_hover.png', True, (213, 91))

    def update(self, surface, possouris, basic_accueil: bool):
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
        self.spawn_button = load_image('assets/game/panels/classic_panel/spawn_button.png')
        self.spawn_button_rect = get_custom_rect(self.spawn_button, 42, 138, 250, 250)

        self.spawn_button_hover = load_image('assets/game/panels/classic_panel/spawn_button_hover.png')
        self.spawn_button_pos = (22, 126)

        # TRAIN BUTTON
        self.train_button = load_image('assets/game/panels/classic_panel/train_button.png')
        self.train_button_rect = get_custom_rect(self.train_button, 327, 138, 250, 250)

        self.train_button_hover = load_image('assets/game/panels/classic_panel/train_button_hover.png')

        self.train_button_pos = (307, 126)

        # GRIND BUTTON
        self.grind_button = load_image('assets/game/panels/classic_panel/grind_button.png')
        self.grind_button_rect = get_custom_rect(self.grind_button, 612, 138, 250, 250)

        self.grind_button_hover = load_image('assets/game/panels/classic_panel/grind_button_hover.png')

        self.grind_button_pos = (592, 126)

        # ITEMS BUTTON
        self.items_button = load_image('assets/game/panels/classic_panel/items_button.png')
        self.items_button_rect = get_custom_rect(self.items_button, 78, 422, 250, 250)

        self.items_button_hover = load_image('assets/game/panels/classic_panel/items_button_hover.png')

        self.items_button_pos = (58, 410)

        # EVOL BUTTON
        self.evol_button = load_image('assets/game/panels/classic_panel/evol_button.png')
        self.evol_button_rect = get_custom_rect(self.evol_button, 362, 422, 250, 250)

        self.evol_button_hover = load_image('assets/game/panels/classic_panel/evol_button_hover.png')

        self.evol_button_pos = (342, 410)

        # EDIT BUTTON
        self.edit_actions_button = load_image('assets/game/panels/classic_panel/edit_actions_button.png')
        self.edit_actions_button_rect = get_custom_rect(self.edit_actions_button, 515, 11)

        self.edit_actions_button_hover = load_image('assets/game/panels/classic_panel/edit_actions_button_hover.png')

    def update(self, surface, possouris, ingame_window):
        if self.edit_actions_button_rect.collidepoint(possouris) and not ingame_window.main_window_rect.collidepoint(
                possouris):
            surface.blit(self.edit_actions_button_hover, self.edit_actions_button_rect)
        else:
            surface.blit(self.edit_actions_button, self.edit_actions_button_rect)

        if self.unlocked_buttons['Spawn']:
            if self.spawn_button_rect.collidepoint(possouris) and not ingame_window.main_window_rect.collidepoint(
                    possouris):
                surface.blit(self.spawn_button, self.spawn_button_pos)
                surface.blit(self.spawn_button_hover, self.spawn_button_pos)
            else:
                surface.blit(self.spawn_button, self.spawn_button_pos)

        if self.unlocked_buttons['Train']:
            if self.train_button_rect.collidepoint(possouris) and not ingame_window.main_window_rect.collidepoint(
                    possouris):
                surface.blit(self.train_button, self.train_button_pos)
                surface.blit(self.train_button_hover, self.train_button_pos)
            else:
                surface.blit(self.train_button, self.train_button_pos)

        if self.unlocked_buttons['Grind']:
            if self.grind_button_rect.collidepoint(possouris) and not ingame_window.main_window_rect.collidepoint(
                    possouris):
                surface.blit(self.grind_button, self.grind_button_pos)
                surface.blit(self.grind_button_hover, self.grind_button_pos)
            else:
                surface.blit(self.grind_button, self.grind_button_pos)

        if self.unlocked_buttons['Items']:
            if self.items_button_rect.collidepoint(possouris) and not ingame_window.main_window_rect.collidepoint(
                    possouris):
                surface.blit(self.items_button, self.items_button_pos)
                surface.blit(self.items_button_hover, self.items_button_pos)
            else:
                surface.blit(self.items_button, self.items_button_pos)

        if self.unlocked_buttons['Evol']:
            if self.evol_button_rect.collidepoint(possouris) and not ingame_window.main_window_rect.collidepoint(
                    possouris):
                surface.blit(self.evol_button, self.evol_button_pos)
                surface.blit(self.evol_button_hover, self.evol_button_pos)
            else:
                surface.blit(self.evol_button, self.evol_button_pos)

    def is_hovering_button(self, possouris):
        if self.edit_actions_button_rect.collidepoint(possouris):
            return True
        elif self.spawn_button_rect.collidepoint(possouris):
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
        # Bouton CLOSE
        self.x_button = load_image('assets/game/ingame_windows/basic/x_button.png')
        self.x_button_rect = get_custom_rect(self.x_button, 854, 4)

        self.x_button_hover = load_image('assets/game/ingame_windows/basic/x_button_hover.png')

        # Bouton MINIMIZE
        self.min_button = load_image('assets/game/ingame_windows/basic/min_button.png')
        self.min_button_rect = get_custom_rect(self.min_button, 816, 4)

        self.min_button_hover = load_image('assets/game/ingame_windows/basic/min_button_hover.png')

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


def load_image(path, boolTransfromScale=False, size=None):
    image = pygame.image.load(path)

    if boolTransfromScale:
        image = pygame.transform.scale(image, size)

    return image


def get_custom_rect(image, rectx=None, recty=None, rectw=None, recth=None):
    image_rect = image.get_rect()
    if rectx is not None:
        image_rect.x = rectx
    if recty is not None:
        image_rect.y = recty
    if rectw is not None:
        image_rect.w = rectw
    if recth is not None:
        image_rect.h = recth

    return image_rect


if __name__ == '__main__':
    pass