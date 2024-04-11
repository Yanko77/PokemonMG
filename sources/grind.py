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

        self.graph = Graph(self.game, GRAPH_DICT)

        self.form_surface = pygame.surface.Surface((1280, 720))
        self.form_surface.fill((0, 255, 0))
        self.form_surface.set_colorkey((0, 255, 0))

        self.background = self.img_load('background')

        self.window_pos = (0, 0)

    def update(self, surface, possouris, window):
        self.window_pos = window.basic_window_pos

        self.display(self.background, (-21, -60), surface)

        self.graph.display(surface, possouris, self.form_surface, window)

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
        pass

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
        pass


class Graph:

    def __init__(self, game, dico=None):
        self.game = game

        self.GRAPH_MAX_LINE_ANGLE = 75

        self.lines_length = GRAPH_LINES_LENGTH
        self.lines_width = GRAPH_LINES_WIDTH
        self.circles_radius = GRAPH_CIRCLES_RADIUS
        self.circles_width = GRAPH_CIRCLES_WIDTH

        self.zoom_value = 1

        self.root = Upgrade('Root', self.game)

        if dico is None:
            dico = {}

        self.root.set_next_upgrades(dico)

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

        surface.blit(form_surface, (window_pos[0] + 21, window_pos[1] + window.window_bar_rect.h), (window_pos[0] + 21, window_pos[1] + window.window_bar_rect.h, window.WIDTH, window.HEIGHT))
        form_surface.fill((0, 255, 0))

    def init_graph(self, window):
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
        value = value/50

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


class Upgrade:

    def __init__(self, name, game, next_list=None, cost=0):
        self.game = game
        self.graph = None

        self.name = name
        self.pos = (0, 0)
        self.angle = 0
        self.rect = pygame.Rect(0, 0, 0, 0)

        if next_list is None:
            self.next = []
        else:
            self.next = [upgrade for upgrade in next_list]

        self.cost = cost
        self.is_unlock = False

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
                angle = self.angle + radians(self.graph.GRAPH_MAX_LINE_ANGLE * 2 / nb_upgrades) * (i - (nb_upgrades - 1) / 2)

            point_arrivee = (
                point_accroche[0] + self.graph.lines_length * cos(angle),
                point_accroche[1] + self.graph.lines_length * sin(angle)
            )

            self.graph.draw_forme('line')(form_surface, point_accroche, point_arrivee, width=round(self.graph.lines_width * 1.4))

            next_upgrade.display(surface, possouris, form_surface)

            i += 1

        i = 0
        for next_upgrade in self.next:
            if nb_upgrades == 1:
                angle = self.angle
            else:
                angle = self.angle + radians(self.graph.GRAPH_MAX_LINE_ANGLE * 2 / nb_upgrades) * (i - (nb_upgrades - 1) / 2)

            point_arrivee = (
                point_accroche[0] + self.graph.lines_length * cos(angle),
                point_accroche[1] + self.graph.lines_length * sin(angle)
            )

            self.graph.draw_forme('line')(form_surface, point_accroche, point_arrivee, color=(50, 50, 50))

            i += 1

        self.graph.draw_forme('circle')(form_surface, center=self.pos, radius=self.graph.circles_radius + 3, color=(220, 220, 220),
                             width=round(self.graph.circles_width + 2))
        self.graph.draw_forme('circle')(form_surface, center=self.pos, radius=self.graph.circles_radius + 2, color=(50, 50, 50),
                             width=round(self.graph.circles_width + 2))
        self.graph.draw_forme('circle')(form_surface, center=self.pos, color=color)

    def set_display_infos(self, pos, angle, window, graph):
        self.graph = graph
        self.pos = pos
        self.angle = angle

        rect_posx = self.pos[0] - self.graph.circles_radius
        rect_posy = self.pos[1] - self.graph.circles_radius
        rect_width = self.graph.circles_radius*2
        rect_height = self.graph.circles_radius*2

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
                angle = self.angle + radians(self.graph.GRAPH_MAX_LINE_ANGLE * 2 / nb_upgrades) * (i - (nb_upgrades - 1) / 2)

            pos = (
                self.pos[0] + self.graph.lines_length * cos(angle) + self.graph.circles_radius * cos(self.angle) + self.graph.circles_radius * cos(angle),
                self.pos[1] + self.graph.lines_length * sin(angle) + self.graph.circles_radius * sin(self.angle) + self.graph.circles_radius * sin(angle)
            )
            next_upgrade.set_display_infos(pos, angle, window, graph)

            i += 1

    def set_next_upgrades(self, dico):
        for next_upgrade in dico:
            next_upgrade.set_next_upgrades(dico[next_upgrade])
            self.next.append(next_upgrade)


class GoldUpgrade(Upgrade):

    def __init__(self, game):
        super().__init__('Gold Boost', game)


GRAPH_DICT = {
        Upgrade('1', None): {Upgrade('2', None): {},
                             Upgrade('3', None): {Upgrade('4', None): {Upgrade('4', None): {}},
                                                  Upgrade('4', None): {Upgrade('4', None): {Upgrade('4', None): {Upgrade('4', None): {}},
                                                  Upgrade('4', None): {Upgrade('4', None): {}},
                                                  Upgrade('4', None): {Upgrade('4', None): {}}}},
                                                  Upgrade('4', None): {Upgrade('4', None): {}}},
                             Upgrade('7', None): {},},

        Upgrade('5', None): {Upgrade('6', None): {Upgrade('6', None): {}}, Upgrade('6', None): {}},
        Upgrade('5', None): {},

    }
