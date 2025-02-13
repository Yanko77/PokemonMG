import math

import pygame

from panel import Panel
from font import Font, IMPACT50

PLAYER_NAME_FONT = IMPACT50


class MainPanel(Panel):

    def __init__(self, game):
        super().__init__(game=game,
                         path='assets/game/panels/classic_panel/')

        self.background = self.img_load('background')

        self.name_bar = PlayerNameBar(self)
        self.team = PlayerTeam(self)

        self.set_components([
            self.name_bar,
            self.team
        ])

    def update(self, possouris):
        self.game.screen.blit(self.background, (0, 0))

        for component in self.components:
            component.update(possouris)

    #def left_clic_interactions(self, possouris):
        #self.name_bar.left_clic_interactions(possouris)

    def keyup_interactions(self, key):
        self.name_bar.keyup_interactions(key)

    def is_hovering_buttons(self, possouris):
        return self.name_bar.is_hovering(possouris)


class PlayerNameBar:

    MAX_NAME_LENGTH = 385

    def __init__(self, panel):
        self.panel: MainPanel = panel

        self.name = PLAYER_NAME_FONT.render(self.panel.game.player.name.get(), (15, 0, 124), load_mode=False)
        self.rect = pygame.Rect(656, 12, 399, 51)

        self.prio = 1

        self.cursor = PlayerNameEditingCursor(self)

        self.hover = self.panel.img_load('player_name_hover')
        self.shadow = self.panel.img_load('name_editing_shadow')

        self.is_editing = False
        
    @property
    def is_name_full(self):
        return self.name.get_width() >= self.MAX_NAME_LENGTH

    def update(self, possouris):
        screen = self.panel.game.screen

        self.display_name(screen)

        if self.rect.collidepoint(possouris):
            screen.blit(self.hover, (0, 0))

        if self.is_editing:
            self.cursor.update(screen)
            screen.blit(self.shadow, (0, 0))

    def display_name(self, screen):
        screen.blit(self.name, (self.rect.x + 6, self.rect.y - 2))

    def update_name(self):
        self.name = PLAYER_NAME_FONT.render(self.panel.game.player.name.get(), (15, 0, 124), load_mode=False)

    def start_editing(self):
        self.is_editing = True
        self.panel.set_component_prio(self, 10)

    def stop_editing(self):
        self.is_editing = False
        self.panel.set_component_prio(self, 1)

    def left_clic_interactions(self, possouris):
        if self.is_editing:
            if not self.rect.collidepoint(possouris):
                self.stop_editing()
        else:
            if self.rect.collidepoint(possouris):
                self.start_editing()

    def keyup_interactions(self, key):
        player = self.panel.game.player
        key_name = pygame.key.name(key)

        if self.is_editing:
            if key_name == 'return':
                self.stop_editing()

            elif key_name == 'backspace':
                player.name.truncate()
                self.update_name()

            if not self.is_name_full:

                if key_name == 'space':
                    player.name.add(" ")
                    self.update_name()

                elif key_name.isalpha() and len(key_name) == 1:
                    letter = key_name

                    if self.panel.game.pressed[pygame.K_LSHIFT]:
                        letter = letter.upper()

                    player.name.add(letter)
                    self.update_name()

    def is_hovering(self, possouris):
        return not self.is_editing and self.rect.collidepoint(possouris) or \
                   self.is_editing


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


class PlayerTeam:

    EMP_BG_COLOR1 = (255, 255, 255)
    EMP_BG_COLOR2 = (163, 171, 255)

    def __init__(self, panel):
        self.panel: MainPanel = panel
        self.game = self.panel.game

        self.prio = 2

        self.emps = [
            PlayerTeamPokemon(self, i) for i in range(6)
        ]
        self.is_emp_moving = False

    def update(self, possouris):
        screen = self.game.screen

        for pk in self.emps:
            pk.update(possouris)

    def is_hovering(self, possouris):
        return any([emp.is_hovering(possouris) for emp in self.emps])


class PlayerTeamPokemon:

    def __init__(self, group,  i):
        self.group: PlayerTeam = group
        self.game = self.group.game

        self.i = i
        self.pokemon = self.game.player.team[self.i]

        self.RECT = pygame.Rect(900,
                                275 + self.i * 73,
                                369,
                                69)
        self.rect = pygame.Rect.copy(self.RECT)

        self.hover_rect = self.group.panel.create_rect_alpha(
            self.rect.size,
            self.background_color
        )

        self.is_moving = False
        self.saved_moving_possouris = (0, 0)

    @property
    def is_hidden(self):
        return self.pokemon is None

    @property
    def background_color(self):
        return self.group.EMP_BG_COLOR1 if self.i % 2 == 0 else self.group.EMP_BG_COLOR2

    @property
    def alpha(self):
        return 1528 + 255 - self.distance_from_area

    @property
    def distance_from_area(self):
        x_distance = (1272 - self.rect.x) ** 2
        y_distance = (637 - self.rect.y) ** 2

        return math.sqrt(x_distance + y_distance)

    def update(self, possouris):
        self.update_sync()
        self.check_moving(possouris)

        if self.is_moving:
            self.move(possouris)

        if not self.is_hidden:
            self.display(possouris)

    def update_sync(self):
        if self.pokemon != self.game.player.team[self.i]:
            self.pokemon = self.game.player.team[self.i]

    def display(self, possouris):
        # Hover
        if self.is_hovering(possouris):
            self.display_hover_rect()

        # Icon
        self.display_icon()

        # Name
        self.display_name()

    def display_hover_rect(self):
        self.game.screen.blit(self.hover_rect, self.rect)

    def display_icon(self):
        icon = self.pokemon.icon

        icon.set_alpha(self.alpha)

        self.game.screen.blit(icon, (self.rect.x, self.rect.y - 5))

    def display_name(self):
        pass

    def check_moving(self, possouris):
        if not self.is_moving:
            if self.game.mouse_pressed[1] and self.rect.collidepoint(possouris):
                if not self.group.is_emp_moving:
                    self.is_moving = True
                    self.saved_moving_possouris = (possouris[0] - self.RECT.x, possouris[1] - self.RECT.y)

        else:
            if not self.game.mouse_pressed[1]:
                self.is_moving = False
                self.reset_rect()

    def move(self, possouris):
        self.rect.topleft = (
            possouris[0] - self.saved_moving_possouris[0],
            possouris[1] - self.saved_moving_possouris[1]
        )

    def reset_rect(self):
        self.rect = pygame.Rect.copy(self.RECT)

    def is_hovering(self, possouris):
        return self.rect.collidepoint(possouris)
