import pygame

from math import cos, sin, tan, radians

GRAPH_LINES_LENGTH = 50
GRAPH_LINES_WIDTH = 5
GRAPH_CIRCLES_RADIUS = 25
GRAPH_CIRCLES_WIDTH = 5
GRAPH_MAX_LINE_ANGLE = 75


class GrindPanel:

    def __init__(self, game):
        self.game = game

        self.PATH = 'assets/game/ingame_windows/Grind/'

        self.graph = Graph(self.game, GRAPH_DICT)

        self.background = self.img_load('background')

        self.window_pos = (0, 0)

    def update(self, surface, possouris, window_pos):
        self.window_pos = window_pos

        self.display(self.background, (-21, -60), surface)

        self.graph.display(surface, possouris)

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

        self.root = Upgrade('Root', self.game)

        if dico is None:
            dico = {}

        self.root.set_next_upgrades(dico)

    def display(self, surface, possouris):

        i = 0
        nb_upgrades = len(self.root.next)

        for next_upgrade in self.root.next:
            angle = radians(360 / nb_upgrades * i)

            point_arrivee = (
                    self.root.pos[0] + GRAPH_LINES_LENGTH * cos(angle),
                    self.root.pos[1] + GRAPH_LINES_LENGTH * sin(angle)
            )
            draw_forme('line')(surface, self.root.pos, point_arrivee)

            next_upgrade.display(surface, possouris)

            i += 1

    def init_graph(self, window):
        pos = (window.get_width() // 2 + window.basic_window_pos[0],
               window.get_height() // 2 + window.basic_window_pos[1])

        angle = radians(0)

        self.root.set_display_infos(pos, angle)

        i = 0
        nb_upgrades = len(self.root.next)
        for next_upgrade in self.root.next:
            angle = radians(360 / nb_upgrades * i)
            pos = (
                self.root.pos[0] + (GRAPH_LINES_LENGTH + GRAPH_CIRCLES_RADIUS) * cos(angle),
                self.root.pos[1] + (GRAPH_LINES_LENGTH + GRAPH_CIRCLES_RADIUS) * sin(angle)
            )
            next_upgrade.set_display_infos(pos, angle)

            i += 1


class Upgrade:

    def __init__(self, name, game, next_list=None, cost=0):
        self.game = game

        self.name = name
        self.pos = (0, 0)
        self.angle = 0

        if next_list is None:
            self.next = []
        else:
            self.next = [upgrade for upgrade in next_list]

        self.cost = cost
        self.is_unlock = False

    def display(self, surface, possouris):
        draw_forme('circle')(surface, center=self.pos)

        point_accroche = (
            self.pos[0] + GRAPH_CIRCLES_RADIUS * cos(self.angle),
            self.pos[1] + GRAPH_CIRCLES_RADIUS * sin(self.angle)
        )

        i = 0
        nb_upgrades = len(self.next)
        for next_upgrade in self.next:
            if nb_upgrades == 1:
                angle = self.angle
            else:
                angle = angle = self.angle + radians(GRAPH_MAX_LINE_ANGLE * 2 / nb_upgrades) * (i - (nb_upgrades - 1) / 2)

            point_arrivee = (
                point_accroche[0] + GRAPH_LINES_LENGTH * cos(angle),
                point_accroche[1] + GRAPH_LINES_LENGTH * sin(angle)
            )

            draw_forme('line')(surface, point_accroche, point_arrivee)

            next_upgrade.display(surface, possouris)

            i += 1

    def set_display_infos(self, pos, angle):
        self.pos = pos
        self.angle = angle

        i = 0
        nb_upgrades = len(self.next)
        for next_upgrade in self.next:
            if nb_upgrades == 1:
                angle = self.angle
            else:
                angle = self.angle + radians(GRAPH_MAX_LINE_ANGLE * 2 / nb_upgrades) * (i - (nb_upgrades - 1) / 2)

            pos = (
                self.pos[0] + GRAPH_LINES_LENGTH * cos(angle) + GRAPH_CIRCLES_RADIUS * cos(self.angle) + GRAPH_CIRCLES_RADIUS * cos(angle),
                self.pos[1] + GRAPH_LINES_LENGTH * sin(angle) + GRAPH_CIRCLES_RADIUS * sin(self.angle) + GRAPH_CIRCLES_RADIUS * sin(angle)
            )
            next_upgrade.set_display_infos(pos, angle)

            i += 1

    def set_next_upgrades(self, dico):
        for next_upgrade in dico:
            next_upgrade.set_next_upgrades(dico[next_upgrade])
            self.next.append(next_upgrade)


def draw_forme(forme: str):

    def line(surface, pos_deb, pos_fin, color=(255, 255, 255)):
        pygame.draw.line(surface, color, pos_deb, pos_fin, width=GRAPH_LINES_WIDTH)

    def circle(surface, center, color=(255, 255, 255)):
        pygame.draw.circle(surface, center=center, color=color, radius=GRAPH_CIRCLES_RADIUS, width=GRAPH_CIRCLES_WIDTH)

    formes_functions = {
        'line': line,
        'circle': circle
    }

    return formes_functions[forme]


GRAPH_DICT = {
        Upgrade('1', None): {Upgrade('2', None): {},
                             Upgrade('3', None): {Upgrade('4', None): {}},
                             Upgrade('7', None): {},},

        Upgrade('5', None): {Upgrade('6', None): {}, Upgrade('6', None): {}},
        Upgrade('5', None): {},

    }



if __name__ == '__main__':
    screen = pygame.display.set_mode((1280, 720))

    # Définition des fonctions

    running = True
    posSouris = (0, 0)

    g = Graph(None, {
        Upgrade('1', None): {Upgrade('2', None): {},
                             Upgrade('3', None): {Upgrade('4', None): {}},
                             Upgrade('7', None): {},},

        Upgrade('5', None): {Upgrade('6', None): {}, Upgrade('6', None): {}},
        Upgrade('5', None): {},

    })
    g.init_graph(screen)

    # Boucle du jeu
    while running:
        posSouris = list(pygame.mouse.get_pos())

        g.display(screen, posSouris)

        for event in pygame.event.get():  # Detection actions du joueur
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()  # Update de la fenetre

    pygame.quit()
