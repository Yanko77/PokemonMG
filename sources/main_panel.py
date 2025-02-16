import math

import pygame

from panel import Panel
from font import Font, IMPACT50, OSWALD25, OSWALD18, OSWALD15

PLAYER_NAME_FONT = IMPACT50
TEAM_PK_NAME_FONT = OSWALD25
TEAM_PK_LEVEL_FONT = OSWALD15
TEAM_PK_TYPE_FONT = OSWALD15
TEAM_PK_ITEMS_FONT = OSWALD15
TEAM_PK_HEALTH_FONT = OSWALD18


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

    def left_click_up(self, possouris):
        if self.is_editing:
            if not self.rect.collidepoint(possouris):
                self.stop_editing()
        else:
            if self.rect.collidepoint(possouris):
                self.start_editing()

    def left_click_down(self, possouris):
        pass

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

        self.emps: list[PlayerTeamPokemon] = [
            PlayerTeamPokemon(self, i) for i in range(6)
        ]
        self.is_emp_moving = False

    def update(self, possouris):

        for pk in self.emps:
            pk.update(possouris)

    def sort_emps_by_prio(self):
        self.emps.sort(key=lambda comp: comp.prio)

    def left_click_down(self, possouris):
        for emp in self.emps[::-1]:
            if emp.is_hovering(possouris):
                emp.left_click_down(possouris)
                self.is_emp_moving = True
                self.sort_emps_by_prio()
                break

    def left_click_up(self, possouris):
        for emp in self.emps[::-1]:
            if emp.is_hovering(possouris):
                emp.left_click_up(possouris)
                self.is_emp_moving = False

                for emp2 in self.emps:
                    if emp2 != emp and emp2.rect.collidepoint(possouris):
                        self.game.player.team.swap(emp.i, emp2.i)

                break

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
        self.rect: pygame.Rect = pygame.Rect.copy(self.RECT)

        self.hover_rect = self.group.panel.create_rect_alpha(
            self.rect.size,
            self.background_color
        )

        self.prio = 0

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

    def set_prio(self, value: int):
        self.prio = value

        print([emp.pokemon for emp in self.group.emps])

    def update(self, possouris):
        self.update_sync()

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

        # Infos : Level, Types & Items
        self.display_infos()

        # HP Bar
        self.display_hp_bar()

    def display_hover_rect(self):
        self.game.screen.blit(self.hover_rect, self.rect)

    def display_icon(self):
        icon = self.pokemon.icon

        icon.set_alpha(self.alpha)

        self.game.screen.blit(icon, (self.rect.x, self.rect.y - 5))

    def display_name(self):
        name = TEAM_PK_NAME_FONT.render(self.pokemon.name, (0, 0, 0))

        name.set_alpha(self.alpha)

        self.game.screen.blit(name, (self.rect.x + 70, self.rect.y + 13))

    def display_infos(self):
        # Level
        level = TEAM_PK_LEVEL_FONT.render(f'Lv.{self.pokemon.level}', (0, 0, 0))
        level.set_alpha(self.alpha)
        self.game.screen.blit(level, (self.rect.x + 60, self.rect.y + 42))

        # 1st Type
        pk_type1 = self.pokemon.types[0]
        type1 = TEAM_PK_TYPE_FONT.render(str(pk_type1), pk_type1.color)
        type1.set_alpha(self.alpha)
        self.game.screen.blit(type1, (self.rect.x + level.get_width() + 65, self.rect.y + 42))

        # 2nd Type
        pk_type2 = self.pokemon.types[1]
        if pk_type2 is not None:
            type2 = TEAM_PK_TYPE_FONT.render(str(pk_type2), pk_type2.color)
            type2.set_alpha(self.alpha)
            self.game.screen.blit(type2,
                                  (self.rect.x + level.get_width() + type1.get_width() + 68, self.rect.y + 42))

        # Item
        if not self.pokemon.bag.is_empty:
            item_text = 'ITEM'
            if self.pokemon.bag.count_items() > 1:
                item_text += 'S'

            item = TEAM_PK_ITEMS_FONT.render(item_text, (30, 30, 30))
            item.set_alpha(self.alpha)
            self.game.screen.blit(item, (self.rect.x + 353 - item.get_width(), self.rect.y + 6))

    def display_hp_bar(self):
        # HP Bar
        rect_alpha = self.group.panel.create_rect_alpha

        back_bar = rect_alpha((150, 17), (35, 35, 35), self.alpha)
        front_bar = rect_alpha(
            (self.pokemon.stats.health / self.pokemon.stats.max_health * 150, 17),
            (42, 214, 0),
            self.alpha
        )

        bar_pos = (self.rect.x + 205, self.rect.y + 26)
        self.game.screen.blit(back_bar, bar_pos)
        self.game.screen.blit(front_bar, bar_pos)

        # HP Text
        hp_text = f'{self.pokemon.stats.health}/{self.pokemon.stats.max_health}'
        hp = TEAM_PK_HEALTH_FONT.render(hp_text, (0, 0, 0))
        hp.set_alpha(self.alpha)
        self.game.screen.blit(hp, (self.rect.x + 205, self.rect.y + 40))

    def start_moving(self):
        self.is_moving = True
        self.set_prio(1)

    def stop_moving(self):
        self.is_moving = False
        self.reset_rect()
        self.set_prio(0)

    def save_possouris(self, possouris):
        self.saved_moving_possouris = (possouris[0] - self.RECT.x, possouris[1] - self.RECT.y)

    def move(self, possouris):
        self.rect.topleft = (
            possouris[0] - self.saved_moving_possouris[0],
            possouris[1] - self.saved_moving_possouris[1]
        )

    def reset_rect(self):
        self.rect = pygame.Rect.copy(self.RECT)

    def left_click_down(self, possouris):
        self.start_moving()
        self.save_possouris(possouris)

    def left_click_up(self, possouris):
        self.stop_moving()

    def is_hovering(self, possouris):
        return self.rect.collidepoint(possouris)
