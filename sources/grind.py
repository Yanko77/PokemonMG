import pygame

from math import cos, sin, tan, radians

GRAPH_LINES_LENGTH = 100
GRAPH_LINES_WIDTH = 6
GRAPH_CIRCLES_RADIUS = 35
GRAPH_CIRCLES_WIDTH = 6


class GrindPanel:

    def __init__(self, game, window):
        self.game = game
        self.window = window

        self.PATH = 'assets/game/ingame_windows/Grind/'

        self.GRAPH_DICT = {
            CombatUpgrade: {

            },
            EcoUpgrade: {
                InstantGoldWin1000: {
                    InstantGoldWin2500: {
                        InstantGoldWin5000: {

                        },
                    },
                },

                EcoUpgrade2: {
                    EcoUpgrade3: {
                        EcoUpgrade4: {

                        },
                    },
                },

                GoldEarningBoost20: {
                    GoldEarningBoost50: {
                        GoldEarningBoost130: {
                            NextTurnGoldWin50000: {}
                        },
                        NextTurnGoldWin10000: {}
                    },
                    NextTurnGoldWin5000: {},
                },

            },
            ScienceUpgrade: {
                ScienceUpgrade2: {
                    ScienceUpgrade3: {
                        ScienceUpgrade4: {

                        }
                    },
                    BoostPlayerMaxActions1: {
                        BoostPlayerMaxActions2: {}
                    }
                }
            }
        }

        self.graph = Graph(game=self.game,
                           window=self.window,
                           dico=self.GRAPH_DICT)

        self.background = self.img_load('background')

    def update(self, surface, possouris):

        self.display(self.background, (-21, -60), surface)

        surface.blit(
            self.graph.render(possouris),
            self.window.rect,
            self.window.rect
        )
        self.graph.move(possouris)

    def display(self,
                image: pygame.Surface,
                pos,
                surface: pygame.Surface,
                rect=None):
        """
        Méthode d'affichage d'une image.
        Prend en paramètre une position relative à la fenêtre ingame.

        @in : image, pygame.Surface → image à afficher
        @in : pos, tuple ou pygame.Rect → position souhaitée relative à la fenêtre ingame
        @in : surface, pygame.Surface → fenêtre du jeu
        @in : rect, pygame.Rect ou None → zone de l'image à afficher

        """

        image_pos = (
            pos[0] + self.window.basic_window_pos[0] + 19,
            pos[1] + self.window.basic_window_pos[1] + 39
        )

        if rect is None:
            surface.blit(image, image_pos)
        else:
            surface.blit(image, image_pos,
                         rect)

    def img_load(self, image_name):
        return pygame.image.load(f'{self.PATH}{image_name}.png')

    def reset(self):
        """
        Méthode de réinitialisation du panel.
        Utilisée lors de l'initialisation d'un nouveau tour de jeu.
        """
        pass

    def close(self):
        """
        Méthode classique qui éxécute tout ce qu'il faut faire lorsque le panel est fermé.
        """
        pass

    def left_clic_interactions(self, possouris: list):
        """
        Méthode gérant les intéractions de l'utilisateur avec le clic gauche de la souris.

        @in : possouris, list → coordonnées du pointeur de souris
        """
        self.graph.left_clic_interactions(possouris)

    def right_clic_interactions(self, posssouris: list):
        """
        Méthode gérant les intéractions de l'utilisateur avec le clic droit de la souris.

        @in : possouris, list → coordonnées du pointeur de souris
        """
        pass

    def mouse_wheel(self, value):
        """
        Methode qui gère les interactions utilisateurs avec la molette haut/bas de la souris
        @in : possouris, list → coordonnées du pointeur de souris
        @in : value, int → puissance de l'action molette. Ex : 1 = haut de 1
                                                              -2 = bas de 2
        """
        self.graph.zoom(value)

    def is_hovering_buttons(self, possouris) -> bool:
        """
        Méthode qui retourne True si la souris est positionnée sur un bouton du panel.

        @in : possouris, list → coordonnées du pointeur de souris
        @out : bool
        """
        return self.graph.is_hovering_buttons(possouris)


class Graph:

    def __init__(self, game, window, dico):
        self.game = game
        self.window = window

        self.GRAPH_MAX_LINE_ANGLE = 30
        self.MIN_ZOOM_VALUE = 0.4
        self.MAX_ZOOM_VALUE = 5

        self.lines_length = GRAPH_LINES_LENGTH
        self.lines_width = GRAPH_LINES_WIDTH
        self.circles_radius = GRAPH_CIRCLES_RADIUS
        self.circles_width = GRAPH_CIRCLES_WIDTH

        self.zoom_value = 1

        self.moving = False
        self.moving_gap = (0, 0)

        self.root = Racine(graph=self,
                           pos=None,
                           next_dict=dico)

        self.surface = pygame.surface.Surface((1280, 720)).convert_alpha()
        self.surface.fill((0, 0, 0, 0))

        self._list = self.list

    @property
    def list(self) -> list:
        """
        Retourne la liste de toutes les upgrades du graphe.
        """
        return self.root.next_list

    @property
    def is_visible(self):
        for upgrade in self._list:
            if upgrade.is_visible:
                return True

        if self.root.is_visible:
            return True

        return False

    def render(self, possouris) -> pygame.Surface:
        self.surface.fill((0, 0, 0, 0))
        self.root.display(self.surface, possouris)

        return self.surface

    def move(self, possouris):

        if not self.moving:
            if self.game.mouse_pressed[1] and self.window.is_hovering(possouris):
                if not self.is_hovering_buttons(possouris):
                    self.moving = True
                    self.moving_gap = (possouris[0] - self.root.pos[0],
                                       possouris[1] - self.root.pos[1])
        else:
            if not self.game.mouse_pressed[1]:
                self.moving = False
                if not self.is_visible:
                    self.root.reload(
                        (self.window.get_width() // 2 + self.window.basic_window_pos[0] + 21,
                         self.window.get_height() // 2 + self.window.basic_window_pos[1] + 39)
                    )
            else:
                self.root.reload((possouris[0] - self.moving_gap[0],
                                  possouris[1] - self.moving_gap[1]))

    def zoom(self, value):
        value = value / (self.MAX_ZOOM_VALUE * 2 - self.zoom_value * 2 + 1)

        if self.zoom_value + value > self.MAX_ZOOM_VALUE:
            self.zoom_value = self.MAX_ZOOM_VALUE
        elif self.zoom_value + value < self.MIN_ZOOM_VALUE:
            self.zoom_value = self.MIN_ZOOM_VALUE
        else:
            self.zoom_value += value

        self.lines_length = round(GRAPH_LINES_LENGTH * self.zoom_value)
        self.circles_radius = round(GRAPH_CIRCLES_RADIUS * self.zoom_value)
        self.circles_width = round(GRAPH_CIRCLES_WIDTH * self.zoom_value)
        self.lines_width = round(GRAPH_LINES_WIDTH * self.zoom_value)

        self.root.reload()

    def left_clic_interactions(self, possouris):
        for upgrade in self._list:
            if upgrade.is_hovering(possouris):
                upgrade.buy()

    def is_hovering_buttons(self, possouris):
        for upgrade in self._list:
            if upgrade.is_hovering(possouris):
                return True
        return False


class Upgrade:

    def __init__(self,
                 name,
                 graph: Graph,
                 next_dict,
                 pos=(0, 0),
                 angle=0.,
                 cost=(0, 0, 0),  # points d'upgrade, action, argent
                 tier=0
                 ):
        self.graph = graph

        self._name = name
        self.tier = tier
        self.description = ""

        self.cost = cost
        self.is_unlock = False

        # self._icon_image = pygame.image.load(f'assets/icons/upgrades/{self.name}.png').convert_alpha()
        self._icon_image = pygame.image.load(f'assets/icons/upgrades/InstantGoldWin1.png').convert_alpha()

        self.pos = pos
        self.angle = angle
        self._rect = self.rect

        self.next = []
        self.previous = []
        self.init_next(next_dict)

    @property
    def name(self):
        return self._name

    @property
    def icon_image(self):
        return pygame.transform.scale(
            self._icon_image,
            size=(2 * self.graph.circles_radius - self.graph.circles_width * 2,
                  2 * self.graph.circles_radius - self.graph.circles_width * 2)
        )

    @property
    def rect(self):
        x = self.pos[0] - self.graph.circles_radius
        y = self.pos[1] - self.graph.circles_radius
        w = self.graph.circles_radius * 2
        h = self.graph.circles_radius * 2

        if x < self.graph.window.basic_window_pos[0]:
            w += x - self.graph.window.basic_window_pos[0]
            x = self.graph.window.basic_window_pos[0]
        if y < self.graph.window.basic_window_pos[1]:
            h += y - self.graph.window.basic_window_pos[1] - self.graph.window.window_bar_rect.h
            y = self.graph.window.basic_window_pos[1] + self.graph.window.window_bar_rect.h
        if x > self.graph.window.basic_window_pos[0] + self.graph.window.get_width() + 21 - w:
            w = self.graph.window.basic_window_pos[0] + self.graph.window.get_width() + 21 - x
        if y > self.graph.window.basic_window_pos[
            1] + self.graph.window.get_height() + self.graph.window.window_bar_rect.h - h:
            h = self.graph.window.basic_window_pos[1] + self.graph.window.get_height() - y

        return pygame.Rect(x, y, w, h)

    @property
    def next_list(self):
        liste = []

        for next_upgrade in self.next:
            liste += self.next + next_upgrade.next_list

        return liste

    @property
    def border_color(self):
        return (220 * self.is_unlock,
                220 * self.is_unlock,
                0)

    @property
    def hook_point(self):
        return (
            self.pos[0] + self.graph.circles_radius * cos(self.angle),
            self.pos[1] + self.graph.circles_radius * sin(self.angle),
        )

    @property
    def is_previous_unlock(self):
        for prev_upgrade in self.previous:
            if prev_upgrade.is_unlock:
                return True
        return False

    @property
    def is_visible(self):

        if self.graph.window.basic_window_pos[0] <= self.pos[0] <= self.graph.window.basic_window_pos[0] + self.graph.window.get_width():
            if self.graph.window.basic_window_pos[1] <= self.pos[1] <= self.graph.window.basic_window_pos[1] + self.graph.window.window_bar_rect.h + self.graph.window.get_height():
                return True

        return False

    def buy(self):
        if self.is_previous_unlock and not self.is_unlock:
            if self.graph.game.player.payer(price=self.cost, money=('upgrade_points', 'actions', 'money')):
                self.unlock()

    def unlock(self):
        self.is_unlock = True
        self.activate()

    def activate(self):
        pass

    def _get_end_line_pos(self, angle):
        return (
            self.hook_point[0] + self.graph.lines_length * cos(angle) * 1.2,
            self.hook_point[1] + self.graph.lines_length * sin(angle) * 1.2
        )

    def _get_next_line_color(self, is_next_unlock: bool) -> tuple:
        if is_next_unlock:
            return 255, 255, 255
        else:
            return 100, 100, 100

    def display(self, surface, possouris):
        self.display_icon(surface, possouris)

        for next_upgrade in self.next:
            self.display_next_line(surface, next_upgrade)
            next_upgrade.display(surface, possouris)

    def display_icon(self, surface, possouris):
        pygame.draw.circle(surface=surface,
                           center=self.pos,
                           color=self.border_color,
                           radius=self.graph.circles_radius,
                           width=self.graph.circles_width)

        surface.blit(self.icon_image,
                     (self.pos[0] - self.graph.circles_radius + self.graph.circles_width,
                      self.pos[1] - self.graph.circles_radius + self.graph.circles_width))

    def display_next_line(self, surface, next_upgrade):
        pygame.draw.line(surface=surface,
                         color=(255 * next_upgrade.is_unlock,
                                255 * next_upgrade.is_unlock,
                                255 * next_upgrade.is_unlock),
                         start_pos=self.hook_point,
                         end_pos=self._get_end_line_pos(angle=next_upgrade.angle),
                         width=self.graph.lines_width
                         )

    def reload(self, pos=None, angle=None):

        if pos is not None:
            self.pos = pos
        if angle is not None:
            self.angle = angle

        self._rect = self.rect

        i = 0
        nb_next = len(self.next)
        for next_upgrade in self.next:
            next_upgrade_angle = self._get_next_angle(nb_next, i)
            next_upgrade_pos = self._get_next_pos(next_upgrade_angle)

            next_upgrade.reload(pos=next_upgrade_pos,
                                angle=next_upgrade_angle)

            i += 1

    def add_next(self, upgrade):
        self.next.append(upgrade)

    def add_previous(self, upgrade):
        self.previous.append(upgrade)

    def is_hovering(self, possouris):
        return self._rect.collidepoint(possouris)

    def _get_next_angle(self, nb_next, i):
        if nb_next == 1:
            return self.angle
        else:
            return self.angle + radians(self.graph.GRAPH_MAX_LINE_ANGLE * 2 * nb_next / nb_next) * (i - (nb_next - 1) / 2)

    def _get_next_pos(self, next_angle):
        return (self.pos[0] + self.graph.lines_length * cos(next_angle) + self.graph.circles_radius * (
                cos(self.angle) + cos(next_angle)),
                self.pos[1] + self.graph.lines_length * sin(next_angle) + self.graph.circles_radius * (
                        sin(self.angle) + sin(next_angle)))

    def init_next(self, next_dict):

        i = 0
        nb_next = len(next_dict)
        for next_upgrade in next_dict:
            next_upgrade_angle = self._get_next_angle(nb_next, i)
            next_upgrade_pos = self._get_next_pos(next_upgrade_angle)

            upgrade = next_upgrade(graph=self.graph,
                                   next_dict=next_dict[next_upgrade],
                                   pos=next_upgrade_pos,
                                   angle=next_upgrade_angle)

            upgrade.add_previous(self)
            self.add_next(upgrade)
            i += 1


class Racine(Upgrade):
    """
    Racine du graphe d'upgrades
    """

    def __init__(self, graph: Graph, pos, next_dict=None):
        if pos is None:
            pos = (
                graph.window.get_width() // 2 + graph.window.basic_window_pos[0] + 21,
                graph.window.get_height() // 2 + graph.window.basic_window_pos[1] + 39
            )

        super().__init__(name="Root",
                         graph=graph,
                         next_dict=next_dict,
                         pos=pos,
                         cost=(0, 0, 0),
                         tier=0
                         )
        self.unlock()

    @property
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], 0, 0)

    @property
    def hook_point(self):
        return self.pos

    def _get_next_angle(self, nb_next, i):
        return radians(360 / nb_next * i)

    def _get_next_pos(self, next_angle):
        return (self.pos[0] + self.graph.lines_length * cos(next_angle) + self.graph.circles_radius * cos(next_angle),
                self.pos[1] + self.graph.lines_length * sin(next_angle) + self.graph.circles_radius * sin(next_angle))

    def display_icon(self, surface, possouris):
        pass


class CombatUpgrade(Upgrade):
    """
    Upgrade d'origine de la branche Combat
    """

    def __init__(self, graph, pos, angle, next_dict=None):
        super().__init__(name="Combat",
                         graph=graph,
                         next_dict=next_dict,
                         pos=pos,
                         angle=angle,
                         cost=(0, 0, 0),
                         tier=0
                         )
        self.unlock()


class EcoUpgrade(Upgrade):
    """
    Upgrade d'origine de la branche Economie
    """

    def __init__(self, graph, pos, angle, next_dict=None):
        super().__init__(name="Economie",
                         graph=graph,
                         next_dict=next_dict,
                         pos=pos,
                         angle=angle,
                         cost=(0, 0, 0),
                         tier=0
                         )
        self.unlock()


class ScienceUpgrade(Upgrade):
    """
    Upgrade d'origine de la branche Science
    """

    def __init__(self, graph, pos, angle, next_dict=None):
        super().__init__(name="Science",
                         graph=graph,
                         next_dict=next_dict,
                         pos=pos,
                         angle=angle,
                         cost=(0, 0, 0),
                         tier=0
                         )
        self.unlock()

# ECONOMIE


class InstantGoldWin1000(Upgrade):
    """
    Upgrade de gain d'argent instantané (1000)
    """

    def __init__(self, graph, pos, angle, next_dict=None):
        super().__init__(name="Gagner 1000 Pokédollars",
                         graph=graph,
                         next_dict=next_dict,
                         pos=pos,
                         angle=angle,
                         cost=(0, 1, 0),
                         tier=1
                         )

    def activate(self):
        self.graph.game.player.add_money(1000)


class InstantGoldWin2500(Upgrade):
    """
    Upgrade de gain d'argent instantané (2500)
    """

    def __init__(self, graph, pos, angle, next_dict=None):
        super().__init__(name="Gagner 2500 Pokédollars",
                         graph=graph,
                         next_dict=next_dict,
                         pos=pos,
                         angle=angle,
                         cost=(0, 1, 0),
                         tier=2
                         )

    def activate(self):
        self.graph.game.player.add_money(2500)


class InstantGoldWin5000(Upgrade):
    """
    Upgrade de gain d'argent instantané (5000)
    """

    def __init__(self, graph, pos, angle, next_dict=None):
        super().__init__(name="Gagner 5000 Pokédollars",
                         graph=graph,
                         next_dict=next_dict,
                         pos=pos,
                         angle=angle,
                         cost=(0, 1, 0),
                         tier=3
                         )

    def activate(self):
        self.graph.game.player.add_money(5000)


class GoldEarningBoost20(Upgrade):
    """
    Upgrade de boost de gain d'argent futur en pourcentage (20%)
    """

    def __init__(self,  graph, pos, angle, next_dict=None):
        super().__init__(name="Bonus de gain d'argent de 20%",
                         graph=graph,
                         next_dict=next_dict,
                         pos=pos,
                         angle=angle,
                         cost=(0, 1, 0),
                         tier=1
                         )

    def activate(self):
        self.graph.game.player.boost_earn_money(20)


class GoldEarningBoost50(Upgrade):
    """
    Upgrade de boost de gain d'argent futur en pourcentage (50%)
    """

    def __init__(self,  graph, pos, angle, next_dict=None):
        super().__init__(name="Bonus de gain d'argent de 50%",
                         graph=graph,
                         next_dict=next_dict,
                         pos=pos,
                         angle=angle,
                         cost=(0, 1, 0),
                         tier=2
                         )

    def activate(self):
        self.graph.game.player.boost_earn_money(50)


class GoldEarningBoost130(Upgrade):
    """
    Upgrade de boost de gain d'argent futur en pourcentage (130%)
    """

    def __init__(self,  graph, pos, angle, next_dict=None):
        super().__init__(name="Bonus de gain d'argent de 130%",
                         graph=graph,
                         next_dict=next_dict,
                         pos=pos,
                         angle=angle,
                         cost=(0, 1, 0),
                         tier=3
                         )

    def activate(self):
        self.graph.game.player.boost_earn_money(130)


class NextTurnGoldWin5000(Upgrade):
    """
    Upgrade de gain d'argent avec un délai de 1 tour (5000)
    """

    def __init__(self, graph, pos, angle, next_dict=None):
        super().__init__(name="Gagner 5000 Pokédollars au début du prochain tour",
                         graph=graph,
                         next_dict=next_dict,
                         pos=pos,
                         angle=angle,
                         cost=(0, 0, 2000),
                         tier=1
                         )

    def activate(self):
        self.graph.game.player.next_turn_money_to_earn += 5000


class NextTurnGoldWin10000(Upgrade):
    """
    Upgrade de gain d'argent avec un délai de 1 tour (10000)
    """

    def __init__(self, graph, pos, angle, next_dict=None):
        super().__init__(name="Gagner 10000 Pokédollars au début du prochain tour",
                         graph=graph,
                         next_dict=next_dict,
                         pos=pos,
                         angle=angle,
                         cost=(0, 0, 4000),
                         tier=2
                         )

    def activate(self):
        self.graph.game.player.next_turn_money_to_earn += 10000


class NextTurnGoldWin50000(Upgrade):
    """
    Upgrade de gain d'argent avec un délai de 1 tour (50000)
    """

    def __init__(self, graph, pos, angle, next_dict=None):
        super().__init__(name="Gagner 50000 Pokédollars au début du prochain tour",
                         graph=graph,
                         next_dict=next_dict,
                         pos=pos,
                         angle=angle,
                         cost=(0, 0, 20000),
                         tier=3
                         )

    def activate(self):
        self.graph.game.player.next_turn_money_to_earn += 50000


class EcoUpgrade2(Upgrade):

    def __init__(self, graph, pos, angle, next_dict=None):
        super().__init__(name="Augmenter la taille du porte-feuille à 50000 Pokédollars",
                         graph=graph,
                         next_dict=next_dict,
                         pos=pos,
                         angle=angle,
                         cost=(1, 0, 0),
                         tier=1
                         )

    def activate(self):
        self.graph.game.player.max_money = 50000


class EcoUpgrade3(Upgrade):

    def __init__(self, graph, pos, angle, next_dict=None):
        super().__init__(name="Augmenter la taille du porte-feuille à 100000 Pokédollars",
                         graph=graph,
                         next_dict=next_dict,
                         pos=pos,
                         angle=angle,
                         cost=(1, 0, 0),
                         tier=2
                         )

    def activate(self):
        self.graph.game.player.max_money = 100000


class EcoUpgrade4(Upgrade):

    def __init__(self, graph, pos, angle, next_dict=None):
        super().__init__(name="Augmenter la taille du porte-feuille à 1000000 Pokédollars",
                         graph=graph,
                         next_dict=next_dict,
                         pos=pos,
                         angle=angle,
                         cost=(1, 0, 0),
                         tier=3
                         )

    def activate(self):
        self.graph.game.player.max_money = 1000000


# SCIENCE


class ScienceUpgrade2(Upgrade):
    def __init__(self, graph, pos, angle, next_dict=None):
        super().__init__(name="Augmenter la taille de l'équipe de 2",
                         graph=graph,
                         next_dict=next_dict,
                         pos=pos,
                         angle=angle,
                         cost=(1, 0, 0),
                         tier=1
                         )

    def activate(self):
        self.graph.game.player.unlock_team_emp(2)


class ScienceUpgrade3(Upgrade):
    def __init__(self, graph, pos, angle, next_dict=None):
        super().__init__(name="Augmenter la taille de l'équipe de 2",
                         graph=graph,
                         next_dict=next_dict,
                         pos=pos,
                         angle=angle,
                         cost=(1, 0, 0),
                         tier=2
                         )

    def activate(self):
        self.graph.game.player.unlock_team_emp(2)


class ScienceUpgrade4(Upgrade):

    def __init__(self, graph, pos, angle, next_dict=None):
        super().__init__(name="Augmenter de 1 le nombre d'items tenables par vos Pokémons",
                         graph=graph,
                         next_dict=next_dict,
                         pos=pos,
                         angle=angle,
                         cost=(1, 0, 0),
                         tier=3
                         )

    def activate(self):
        self.graph.game.player.rise_pk_max_items(1)


class BoostPlayerMaxActions1(Upgrade):
    def __init__(self, graph, pos, angle, next_dict=None):
        super().__init__(name="Augmenter de 1 le nombre d'action max",
                         graph=graph,
                         next_dict=next_dict,
                         pos=pos,
                         angle=angle,
                         cost=(2, 0, 0),
                         tier=2
                         )

    def activate(self):
        self.graph.game.player.rise_max_actions_value(1)


class BoostPlayerMaxActions2(Upgrade):
    def __init__(self, graph, pos, angle, next_dict=None):
        super().__init__(name="Augmenter de 1 le nombre d'action max",
                         graph=graph,
                         next_dict=next_dict,
                         pos=pos,
                         angle=angle,
                         cost=(2, 0, 0),
                         tier=3
                         )

    def activate(self):
        self.graph.game.player.rise_max_actions_value(1)