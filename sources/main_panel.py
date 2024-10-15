import pygame

from panel import Panel
from font import Font

PLAYER_NAME_FONT = Font("Impact", 50)


class MainPanel(Panel):

    def __init__(self, game):
        super().__init__(game=game,
                         path='assets/game/panels/classic_panel/')

        self.background = self.img_load('background')

        self.name_bar = PlayerNameBar(self)

    def update(self, possouris):
        self.game.screen.blit(self.background, (0, 0))

        self.name_bar.update(possouris)

    def left_clic_interactions(self, possouris):
        self.name_bar.left_clic_interactions(possouris)

    def keyup_interactions(self, key):
        self.name_bar.keyup_interactions(key)


class PlayerNameBar:

    def __init__(self, panel):
        self.panel: MainPanel = panel

        self.name = PLAYER_NAME_FONT.render(self.panel.game.player.name, (15, 0, 124))
        self.rect = pygame.Rect(656, 12, 399, 51)

        self.cursor = PlayerNameEditingCursor(self)

        self.hover = self.panel.img_load('player_name_hover')

        self.is_editing = False

    def update(self, possouris):
        screen = self.panel.game.screen

        self.display_name(screen)

        if self.rect.collidepoint(possouris):
            screen.blit(self.hover, (0, 0))

        if self.is_editing:
            self.cursor.update(screen)

    def display_name(self, screen):
        screen.blit(self.name, (self.rect.x + 6, self.rect.y - 2))

    def edit_name(self, key):
        player = self.panel.game.player

        if key == pygame.K_BACKSPACE:
            player.set_name(player.name[:-1])

        elif key == pygame.K_RETURN:
            self.is_editing = False

        else:
            c = pygame.key.name(key)

            if c.isalpha():
                if self.panel.game.pressed[pygame.K_LSHIFT]:
                    c = c.upper()

                player.set_name(player.name + c)

        self.update_name()

    def update_name(self):
        self.name = PLAYER_NAME_FONT.render(self.panel.game.player.name, (15, 0, 124))

    def left_clic_interactions(self, possouris):
        if self.is_editing:
            if not self.rect.collidepoint(possouris):
                self.is_editing = False
        else:
            if self.rect.collidepoint(possouris):
                self.is_editing = True

    def keyup_interactions(self, key):
        if self.is_editing:
            self.edit_name(key)


class PlayerNameEditingCursor:

    def __init__(self, bar):
        self.bar: PlayerNameBar = bar
        self.image = self.bar.panel.create_rect_alpha(
            (2, self.bar.name.get_height() - 16),
            (0, 0, 0),
            200
        )

        self.counter = 0

    @property
    def is_hidden(self):
        return self.counter < 20

    def update(self, screen):
        if not self.is_hidden:
            screen.blit(self.image, (665 + self.bar.name.get_width(), 16))

        self.increment_counter()

    def increment_counter(self):
        if self.counter >= 40:
            self.counter = 0
        else:
            self.counter += 1

