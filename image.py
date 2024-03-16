import pygame
import animation
import random


class ClassicGamePanelButtons:

    def __init__(self):
        self.unlocked_buttons = {'Spawn': True,
                                 'Train': True,
                                 'Grind': True,
                                 'Items': True,
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
        if self.edit_actions_button_rect.collidepoint(possouris) and not ingame_window.is_hovering(possouris):
            surface.blit(self.edit_actions_button_hover, self.edit_actions_button_rect)
        else:
            surface.blit(self.edit_actions_button, self.edit_actions_button_rect)

        if self.unlocked_buttons['Spawn']:
            if self.spawn_button_rect.collidepoint(possouris) and not ingame_window.is_hovering(possouris):
                surface.blit(self.spawn_button, self.spawn_button_pos)
                surface.blit(self.spawn_button_hover, self.spawn_button_pos)
            else:
                surface.blit(self.spawn_button, self.spawn_button_pos)

        if self.unlocked_buttons['Train']:
            if self.train_button_rect.collidepoint(possouris) and not ingame_window.is_hovering(possouris):
                surface.blit(self.train_button, self.train_button_pos)
                surface.blit(self.train_button_hover, self.train_button_pos)
            else:
                surface.blit(self.train_button, self.train_button_pos)

        if self.unlocked_buttons['Grind']:
            if self.grind_button_rect.collidepoint(possouris) and not ingame_window.is_hovering(possouris):
                surface.blit(self.grind_button, self.grind_button_pos)
                surface.blit(self.grind_button_hover, self.grind_button_pos)
            else:
                surface.blit(self.grind_button, self.grind_button_pos)

        if self.unlocked_buttons['Items']:
            if self.items_button_rect.collidepoint(possouris) and not ingame_window.is_hovering(possouris):
                surface.blit(self.items_button, self.items_button_pos)
                surface.blit(self.items_button_hover, self.items_button_pos)
            else:
                surface.blit(self.items_button, self.items_button_pos)

        if self.unlocked_buttons['Evol']:
            if self.evol_button_rect.collidepoint(possouris) and not ingame_window.is_hovering(possouris):
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
