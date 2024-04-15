import pygame

from math import cos, sin, tan, radians

GRAPH_LINES_LENGTH = 100
GRAPH_LINES_WIDTH = 6
GRAPH_CIRCLES_RADIUS = 35
GRAPH_CIRCLES_WIDTH = 6


class GrindPanel:

    def __init__(self, game):
        self.game = game

        self.PATH = 'assets/game/ingame_windows/Grind/'

        self.GRAPH_DICT = {
            EcoUpgrade(self.game): {
                InstantGoldWin1000(self.game): {
                    NextTurnGoldWin5000(self.game): {
                        NextTurnGoldWin10000(self.game): {
                            NextTurnGoldWin50000(self.game): {}
                        }
                    },

                    InstantGoldWin2500(self.game): {
                        InstantGoldWin5000(self.game): {

                        }
                    }
                },

                EcoUpgrade2(self.game): {
                    EcoUpgrade3(self.game): {
                        EcoUpgrade4(self.game): {

                        }
                    }
                },

                GoldEarningBoost20(self.game): {
                    GoldEarningBoost50(self.game): {
                        GoldEarningBoost130(self.game): {

                        }
                    }
                }
            },
            CombatUpgrade(self.game): {
            },
            ScienceUpgrade(self.game): {
            },
        }

        self.graph = Graph(self.game, self.GRAPH_DICT)
        self.graph_move_deb_pos = (0, 0)

        self.form_surface = pygame.surface.Surface((1280, 720)).convert_alpha()
        self.form_surface.fill((0, 0, 0, 0))

        self.background = self.img_load('background')

        self.window_pos = (0, 0)

    def update(self, surface, possouris, window):
        self.window_pos = window.basic_window_pos

        self.display(self.background, (-21, -60), surface)

        self.graph.display(surface, possouris, self.form_surface, window)

        self.update_graph_move(window, possouris)

    def update_graph_move(self, window, possouris: list):

        if not self.graph.moving:
            if self.game.mouse_pressed[1] and window.is_hovering(possouris):
                self.graph.moving = True
                self.graph_move_deb_pos = (possouris[0] - self.graph.root.pos[0],
                                           possouris[1] - self.graph.root.pos[1])
        else:
            if not self.game.mouse_pressed[1]:
                self.graph.moving = False
            else:
                self.graph.init_graph(window, (possouris[0] - self.graph_move_deb_pos[0],
                                               possouris[1] - self.graph_move_deb_pos[1]))

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
        if rect is None:
            surface.blit(image, (pos[0] + self.window_pos[0] + 19,
                                 pos[1] + self.window_pos[1] + 39))
        else:
            surface.blit(image, (pos[0] + self.window_pos[0] + 19,
                                 pos[1] + self.window_pos[1] + 39),
                         rect)

    def img_load(self, file_name):
        return pygame.image.load(f'{self.PATH}{file_name}.png')

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

    def mouse_wheel(self, value, window):
        """
        Methode qui gère les interactions utilisateurs avec la molette haut/bas de la souris
        @in : possouris, list → coordonnées du pointeur de souris
        @in : value, int → puissance de l'action molette. Ex : 1 = haut de 1
                                                              -2 = bas de 2
        """
        self.graph.zoom(value, window)

    def is_hovering_buttons(self, possouris) -> bool:
        """
        Méthode qui retourne True si la souris est positionnée sur un bouton du panel.

        @in : possouris, list → coordonnées du pointeur de souris
        @out : bool
        """
        return self.graph.is_hovering_buttons(possouris)


class Graph:

    def __init__(self, game, dico=None):
        self.game = game

        self.GRAPH_MAX_LINE_ANGLE = 75

        self.lines_length = GRAPH_LINES_LENGTH
        self.lines_width = GRAPH_LINES_WIDTH
        self.circles_radius = GRAPH_CIRCLES_RADIUS
        self.circles_width = GRAPH_CIRCLES_WIDTH

        self.zoom_value = 1
        self.moving = False

        self.root = Racine(self.game)

        if dico is None:
            dico = {}

        self.root.set_next_upgrades(dico)

        self.list = self.get_list()

    def display(self, surface, possouris, form_surface, window):
        window_pos = window.basic_window_pos

        i = 0
        nb_upgrades = len(self.root.next)

        for next_upgrade in self.root.next:
            angle = radians(360 / nb_upgrades * i)

            point_arrivee = (
                self.root.pos[0] + self.lines_length * cos(angle),
                self.root.pos[1] + self.lines_length * sin(angle)
            )
            self.draw_forme('line')(form_surface, self.root.pos, point_arrivee, width=round(self.lines_width * 1.4))

            next_upgrade.display(surface, possouris, form_surface)

            i += 1

        i = 0
        for next_upgrade in self.root.next:
            angle = radians(360 / nb_upgrades * i)

            point_arrivee = (
                self.root.pos[0] + self.lines_length * cos(angle),
                self.root.pos[1] + self.lines_length * sin(angle)
            )

            self.draw_forme('line')(form_surface, self.root.pos, point_arrivee, color=(50, 50, 50))

            i += 1

        surface.blit(form_surface, (window_pos[0] + 21, window_pos[1] + window.window_bar_rect.h),
                     (window_pos[0] + 21, window_pos[1] + window.window_bar_rect.h, window.WIDTH, window.HEIGHT))
        form_surface.fill((0, 0, 0, 0))

    def init_graph(self, window, pos=None):
        if pos is None:
            pos = (window.get_width() // 2 + window.basic_window_pos[0],
                    window.get_height() // 2 + window.basic_window_pos[1] + 39)

        angle = radians(0)

        self.root.set_display_infos(pos, angle, window, self)

        i = 0
        nb_upgrades = len(self.root.next)
        for next_upgrade in self.root.next:
            angle = radians(360 / nb_upgrades * i)
            pos = (
                self.root.pos[0] + (self.lines_length + self.circles_radius) * cos(angle),
                self.root.pos[1] + (self.lines_length + self.circles_radius) * sin(angle)
            )
            next_upgrade.set_display_infos(pos, angle, window, self)

            i += 1

    def zoom(self, value, window):
        value = value / 10

        if self.zoom_value + value < 0.4 and self.zoom_value != 0.4:
            self.zoom_value = 0.4 - value

        elif self.zoom_value + value > 5 and self.zoom_value != 5:
            self.zoom_value = 5 - value

        if 0.4 <= self.zoom_value + value <= 5:
            self.zoom_value += value

            self.lines_length = round(GRAPH_LINES_LENGTH * self.zoom_value)
            self.circles_radius = round(GRAPH_CIRCLES_RADIUS * self.zoom_value)
            self.circles_width = round(GRAPH_CIRCLES_WIDTH * self.zoom_value)
            self.lines_width = round(GRAPH_LINES_WIDTH * self.zoom_value)

            self.init_graph(window)

    def draw_forme(self, forme: str):

        def line(surface, pos_deb, pos_fin, color=(255, 255, 255), width=self.lines_width):
            pygame.draw.line(surface, color, pos_deb, pos_fin, width=width)

        def circle(surface, center, color=(255, 255, 255), radius=self.circles_radius,
                   width=self.circles_width):
            pygame.draw.circle(surface, center=center, color=color, radius=radius, width=width)

        formes_functions = {
            'line': line,
            'circle': circle
        }

        return formes_functions[forme]

    def get_list(self):
        """
        Retourne la liste de tous les sommets du graphe ( upgrades )
        """
        liste = []
        for next_upgrade in self.root.next:
            liste += next_upgrade.get_next_list()

        return liste

    def left_clic_interactions(self, possouris):
        for upgrade in self.list:
            if upgrade.is_hovering(possouris):
                upgrade.buy()

    def is_hovering_buttons(self, possouris):
        for upgrade in self.list:
            if upgrade.is_hovering(possouris):
                return True
        return False


class Upgrade:

    def __init__(self,
                 name,
                 game,
                 next_list=None,
                 previous_list=None,
                 cost=(0, 0, 0),  # points d'upgrade, action, argent
                 tier=0):

        self.game = game
        self.graph = None

        self.name = name
        self.tier = tier
        self.description = ""

        # self.icon_image = pygame.image.load(f'assets/icons/upgrades/{self.name}.png').convert()
        self._icon_image = pygame.image.load(f'assets/icons/upgrades/InstantGoldWin1.png').convert_alpha()

        self.pos = (0, 0)
        self.angle = 0
        self.rect = pygame.Rect(0, 0, 0, 0)

        if previous_list is None:
            self.previous = []
        else:
            self.previous = [upgrade for upgrade in previous_list]

        if next_list is None:
            self.next = []
        else:
            self.next = [upgrade for upgrade in next_list]

        self.cost = cost
        self.is_unlock = False

    @property
    def icon_image(self):
        return pygame.transform.scale(self._icon_image,
                                      size=(2 * self.graph.circles_radius - self.graph.circles_width*2,
                                            2 * self.graph.circles_radius - self.graph.circles_width*2))

    def buy(self):
        boolPrevious = True
        for previous_upgrade in self.previous:
            if not previous_upgrade.is_unlock:
                boolPrevious = False

        if not self.is_unlock and boolPrevious:
            if self.game.player.payer(self.cost, ('money', 'actions', 'upgrade points')):
                self.unlock()

    def unlock(self):
        if not self.is_unlock:
            self.is_unlock = True
            self.activate()

    def activate(self):
        pass

    def display(self, surface, possouris, form_surface):
        if self.is_unlock:
            color = (220, 220, 0)
        else:
            color = (0, 0, 0)

        point_accroche = (
            self.pos[0] + self.graph.circles_radius * cos(self.angle),
            self.pos[1] + self.graph.circles_radius * sin(self.angle)
        )

        i = 0
        nb_upgrades = len(self.next)
        for next_upgrade in self.next:
            if nb_upgrades == 1:
                angle = self.angle
            else:
                angle = self.angle + radians(self.graph.GRAPH_MAX_LINE_ANGLE * 2 / nb_upgrades) * (
                            i - (nb_upgrades - 1) / 2)

            point_arrivee = (
                point_accroche[0] + self.graph.lines_length * cos(angle),
                point_accroche[1] + self.graph.lines_length * sin(angle)
            )

            self.graph.draw_forme('line')(form_surface, point_accroche, point_arrivee,
                                          width=round(self.graph.lines_width * 1.4))

            next_upgrade.display(surface, possouris, form_surface)

            i += 1

        i = 0
        for next_upgrade in self.next:
            if nb_upgrades == 1:
                angle = self.angle
            else:
                angle = self.angle + radians(self.graph.GRAPH_MAX_LINE_ANGLE * 2 / nb_upgrades) * (
                            i - (nb_upgrades - 1) / 2)

            point_arrivee = (
                point_accroche[0] + self.graph.lines_length * cos(angle),
                point_accroche[1] + self.graph.lines_length * sin(angle)
            )

            self.graph.draw_forme('line')(form_surface, point_accroche, point_arrivee, color=(50, 50, 50))

            i += 1

        self.graph.draw_forme('circle')(form_surface, center=self.pos, radius=self.graph.circles_radius + 3,
                                        color=(220, 220, 220),
                                        width=round(self.graph.circles_width + 2))
        self.graph.draw_forme('circle')(form_surface, center=self.pos, radius=self.graph.circles_radius + 2,
                                        color=(50, 50, 50),
                                        width=round(self.graph.circles_width + 2))
        self.graph.draw_forme('circle')(form_surface, center=self.pos, color=color)

        form_surface.blit(self.icon_image,
                          (self.pos[0] - self.graph.circles_radius + self.graph.circles_width,
                           self.pos[1] - self.graph.circles_radius + self.graph.circles_width))

    def set_display_infos(self, pos, angle, window, graph):
        self.graph = graph
        self.pos = pos
        self.angle = angle

        rect_posx = self.pos[0] - self.graph.circles_radius
        rect_posy = self.pos[1] - self.graph.circles_radius
        rect_width = self.graph.circles_radius * 2
        rect_height = self.graph.circles_radius * 2

        if rect_posx < window.basic_window_pos[0]:
            rect_width = rect_posx + rect_width - window.basic_window_pos[0]
            rect_posx = window.basic_window_pos[0] + 21

        if rect_posy < window.basic_window_pos[1] + window.window_bar_rect.h:
            rect_height = rect_posy + rect_height - window.basic_window_pos[1] - window.window_bar_rect.h
            rect_posy = window.basic_window_pos[1] + window.window_bar_rect.h

        if rect_posx + rect_width > window.basic_window_pos[0] + window.get_width() + 21:
            rect_width = window.basic_window_pos[0] + window.get_width() + 21 - rect_posx

        if rect_posy + rect_height > window.basic_window_pos[1] + window.get_height() + window.window_bar_rect.h:
            rect_height = window.basic_window_pos[1] + window.get_height() + window.window_bar_rect.h - rect_posy

        self.rect = pygame.Rect(
            rect_posx,
            rect_posy,
            rect_width,
            rect_height
        )

        if self.rect.w < 0:
            self.rect.w = 0
        if self.rect.h < 0:
            self.rect.h = 0

        i = 0
        nb_upgrades = len(self.next)
        for next_upgrade in self.next:
            if nb_upgrades == 1:
                angle = self.angle
            else:
                angle = self.angle + radians(self.graph.GRAPH_MAX_LINE_ANGLE * 2 / nb_upgrades) * (
                            i - (nb_upgrades - 1) / 2)

            pos = (
                self.pos[0] + self.graph.lines_length * cos(angle) + self.graph.circles_radius * cos(
                    self.angle) + self.graph.circles_radius * cos(angle),
                self.pos[1] + self.graph.lines_length * sin(angle) + self.graph.circles_radius * sin(
                    self.angle) + self.graph.circles_radius * sin(angle)
            )
            next_upgrade.set_display_infos(pos, angle, window, graph)

            i += 1

    def set_next_upgrades(self, dico):
        for next_upgrade in dico:
            next_upgrade.set_next_upgrades(dico[next_upgrade])
            self.next.append(next_upgrade)
            next_upgrade.set_previous(self)

    def set_previous(self, upgrade):
        self.previous.append(upgrade)

    def get_next_list(self):
        liste = [self]
        for next_upgrade in self.next:
            liste += next_upgrade.get_next_list()

        return liste

    def is_hovering(self, possouris):
        return self.rect.collidepoint(possouris)


class Racine(Upgrade):
    """
    Racine du graphe d'upgrades
    """

    def __init__(self, game, next_list=None):
        super().__init__(name="Root",
                         game=game,
                         next_list=next_list,
                         cost=(0, 0, 0),
                         tier=0
                         )
        self.is_unlock = True


class EcoUpgrade(Upgrade):
    """
    Upgrade d'origine de la branche Economie
    """

    def __init__(self, game, next_list=None):
        super().__init__(name="Économie",
                         game=game,
                         next_list=next_list,
                         cost=(0, 0, 0),
                         tier=0
                         )


class CombatUpgrade(Upgrade):
    """
    Upgrade d'origine de la branche Combat
    """

    def __init__(self, game, next_list=None):
        super().__init__(name="Combat",
                         game=game,
                         next_list=next_list,
                         cost=(0, 0, 0),
                         tier=0
                         )


class ScienceUpgrade(Upgrade):
    """
    Upgrade d'origine de la branche Science
    """

    def __init__(self, game, next_list=None):
        super().__init__(name="Science",
                         game=game,
                         next_list=next_list,
                         cost=(0, 0, 0),
                         tier=0
                         )


class InstantGoldWin1000(Upgrade):
    """
    Upgrade de gain d'argent instantané (1000)
    """

    def __init__(self, game, next_list=None):
        super().__init__(name="Gagner 1000 Pokédollars",
                         game=game,
                         next_list=next_list,
                         cost=(0, 1, 0),
                         tier=1
                         )

    def activate(self):
        self.game.player.add_money(1000)


class InstantGoldWin2500(Upgrade):
    """
    Upgrade de gain d'argent instantané (2500)
    """

    def __init__(self, game, next_list=None):
        super().__init__(name="Gagner 2500 Pokédollars",
                         game=game,
                         next_list=next_list,
                         cost=(0, 1, 0),
                         tier=2
                         )

    def activate(self):
        self.game.player.add_money(2500)


class InstantGoldWin5000(Upgrade):
    """
    Upgrade de gain d'argent instantané (5000)
    """

    def __init__(self, game, next_list=None):
        super().__init__(name="Gagner 5000 Pokédollars",
                         game=game,
                         next_list=next_list,
                         cost=(0, 1, 0),
                         tier=3
                         )

    def activate(self):
        self.game.player.add_money(10000)


class GoldEarningBoost20(Upgrade):
    """
    Upgrade de boost de gain d'argent futur en pourcentage (20%)
    """

    def __init__(self, game, next_list=None):
        super().__init__(name="Bonus de gain d'argent de 20%",
                         game=game,
                         next_list=next_list,
                         cost=(0, 1, 0),
                         tier=1
                         )

    def activate(self):
        self.game.player.boost_earn_money(20)


class GoldEarningBoost50(Upgrade):
    """
    Upgrade de boost de gain d'argent futur en pourcentage (50%)
    """

    def __init__(self, game, next_list=None):
        super().__init__(name="Bonus de gain d'argent de 50%",
                         game=game,
                         next_list=next_list,
                         cost=(0, 1, 0),
                         tier=2
                         )

    def activate(self):
        self.game.player.boost_earn_money(50)


class GoldEarningBoost130(Upgrade):
    """
    Upgrade de boost de gain d'argent futur en pourcentage (130%)
    """

    def __init__(self, game, next_list=None):
        super().__init__(name="Bonus de gain d'argent de 130%",
                         game=game,
                         next_list=next_list,
                         cost=(0, 1, 0),
                         tier=3
                         )

    def activate(self):
        self.game.player.boost_earn_money(130)


class NextTurnGoldWin5000(Upgrade):
    """
    Upgrade de gain d'argent avec un délai de 1 tour (5000)
    """

    def __init__(self, game, next_list=None):
        super().__init__(name="Gagner 5000 Pokédollars au début du prochain tour",
                         game=game,
                         next_list=next_list,
                         cost=(0, 0, 2000),
                         tier=1
                         )

    def activate(self):
        self.game.player.next_turn_money_to_earn += 5000


class NextTurnGoldWin10000(Upgrade):
    """
    Upgrade de gain d'argent avec un délai de 1 tour (10000)
    """

    def __init__(self, game, next_list=None):
        super().__init__(name="Gagner 10000 Pokédollars au début du prochain tour",
                         game=game,
                         next_list=next_list,
                         cost=(0, 0, 4000),
                         tier=2
                         )

    def activate(self):
        self.game.player.next_turn_money_to_earn += 10000


class NextTurnGoldWin50000(Upgrade):
    """
    Upgrade de gain d'argent avec un délai de 1 tour (50000)
    """

    def __init__(self, game, next_list=None):
        super().__init__(name="Gagner 50000 Pokédollars au début du prochain tour",
                         game=game,
                         next_list=next_list,
                         cost=(0, 0, 20000),
                         tier=3
                         )

    def activate(self):
        self.game.player.next_turn_money_to_earn += 50000


class EcoUpgrade2(Upgrade):

    def __init__(self, game, next_list=None):
        super().__init__(name="Augmenter la taille du porte-feuille à 50000 Pokédollars",
                         game=game,
                         next_list=next_list,
                         cost=(1, 0, 0),
                         tier=1
                         )

    def activate(self):
        self.game.player.max_money = 50000


class EcoUpgrade3(Upgrade):

    def __init__(self, game, next_list=None):
        super().__init__(name="Augmenter la taille du porte-feuille à 100000 Pokédollars",
                         game=game,
                         next_list=next_list,
                         cost=(1, 0, 0),
                         tier=2
                         )

    def activate(self):
        self.game.player.max_money = 100000


class EcoUpgrade4(Upgrade):

    def __init__(self, game, next_list=None):
        super().__init__(name="Augmenter la taille du porte-feuille à 1000000 Pokédollars",
                         game=game,
                         next_list=next_list,
                         cost=(1, 0, 0),
                         tier=3
                         )

    def activate(self):
        self.game.player.max_money = 1000000
