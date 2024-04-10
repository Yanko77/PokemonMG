import pygame

from math import cos, sin, tan, radians

GRAPH_LINES_LENGTH = 75
GRAPH_LINES_WIDTH = 6
GRAPH_CIRCLES_RADIUS = 35
GRAPH_CIRCLES_WIDTH = 6
GRAPH_MAX_LINE_ANGLE = 75


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

    def display(self, surface, possouris, form_surface, window):
        window_pos = window.basic_window_pos

        i = 0
        nb_upgrades = len(self.root.next)

        for next_upgrade in self.root.next:
            angle = radians(360 / nb_upgrades * i)

            point_arrivee = (
                    self.root.pos[0] + GRAPH_LINES_LENGTH * cos(angle),
                    self.root.pos[1] + GRAPH_LINES_LENGTH * sin(angle)
            )
            draw_forme('line')(form_surface, self.root.pos, point_arrivee, width=round(GRAPH_LINES_WIDTH * 1.4))

            next_upgrade.display(surface, possouris, form_surface)

            i += 1

        i = 0
        for next_upgrade in self.root.next:
            angle = radians(360 / nb_upgrades * i)

            point_arrivee = (
                self.root.pos[0] + GRAPH_LINES_LENGTH * cos(angle),
                self.root.pos[1] + GRAPH_LINES_LENGTH * sin(angle)
            )

            draw_forme('line')(form_surface, self.root.pos, point_arrivee, color=(50, 50, 50))

            i += 1

        surface.blit(form_surface, (window_pos[0] + 21, window_pos[1] + window.window_bar_rect.h), (window_pos[0] + 21, window_pos[1] + window.window_bar_rect.h, window.WIDTH, window.HEIGHT))
        form_surface.fill((0, 255, 0))

    def init_graph(self, window):
        pos = (window.get_width() // 2 + window.basic_window_pos[0],
               window.get_height() // 2 + window.basic_window_pos[1] + 39)

        angle = radians(0)

        self.root.set_display_infos(pos, angle, window)

        i = 0
        nb_upgrades = len(self.root.next)
        for next_upgrade in self.root.next:
            angle = radians(360 / nb_upgrades * i)
            pos = (
                self.root.pos[0] + (GRAPH_LINES_LENGTH + GRAPH_CIRCLES_RADIUS) * cos(angle),
                self.root.pos[1] + (GRAPH_LINES_LENGTH + GRAPH_CIRCLES_RADIUS) * sin(angle)
            )
            next_upgrade.set_display_infos(pos, angle, window)

            i += 1


class Upgrade:

    def __init__(self, name, game, next_list=None, cost=0):
        self.game = game

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
            self.pos[0] + GRAPH_CIRCLES_RADIUS * cos(self.angle),
            self.pos[1] + GRAPH_CIRCLES_RADIUS * sin(self.angle)
        )

        i = 0
        nb_upgrades = len(self.next)
        for next_upgrade in self.next:
            if nb_upgrades == 1:
                angle = self.angle
            else:
                angle = self.angle + radians(GRAPH_MAX_LINE_ANGLE * 2 / nb_upgrades) * (i - (nb_upgrades - 1) / 2)

            point_arrivee = (
                point_accroche[0] + GRAPH_LINES_LENGTH * cos(angle),
                point_accroche[1] + GRAPH_LINES_LENGTH * sin(angle)
            )

            draw_forme('line')(form_surface, point_accroche, point_arrivee, width=round(GRAPH_LINES_WIDTH * 1.4))

            next_upgrade.display(surface, possouris, form_surface)

            i += 1

        i = 0
        for next_upgrade in self.next:
            if nb_upgrades == 1:
                angle = self.angle
            else:
                angle = self.angle + radians(GRAPH_MAX_LINE_ANGLE * 2 / nb_upgrades) * (i - (nb_upgrades - 1) / 2)

            point_arrivee = (
                point_accroche[0] + GRAPH_LINES_LENGTH * cos(angle),
                point_accroche[1] + GRAPH_LINES_LENGTH * sin(angle)
            )

            draw_forme('line')(form_surface, point_accroche, point_arrivee, color=(50, 50, 50))

            i += 1

        draw_forme('circle')(form_surface, center=self.pos, radius=GRAPH_CIRCLES_RADIUS + 3, color=(220, 220, 220),
                             width=round(GRAPH_CIRCLES_WIDTH + 2))
        draw_forme('circle')(form_surface, center=self.pos, radius=GRAPH_CIRCLES_RADIUS + 2, color=(50, 50, 50),
                             width=round(GRAPH_CIRCLES_WIDTH + 2))
        draw_forme('circle')(form_surface, center=self.pos, color=color)

        if self.rect.collidepoint(possouris):
            print(self.name)

    def set_display_infos(self, pos, angle, window):
        self.pos = pos
        self.angle = angle

        dist_with_window_border = [
            window.basic_window_pos[0] + window.get_width() - self.pos[0],
            window.basic_window_pos[1] + window.get_height() - self.pos[1]
        ]

        if dist_with_window_border[0] > 0:
            dist_with_window_border[0] = 0

        if dist_with_window_border[1] > 0:
            dist_with_window_border[1] = 1

        self.rect = pygame.Rect(
            self.pos[0] - GRAPH_CIRCLES_RADIUS,
            self.pos[1] - GRAPH_CIRCLES_RADIUS,
            GRAPH_CIRCLES_RADIUS*2 + dist_with_window_border[0],
            GRAPH_CIRCLES_RADIUS*2 + dist_with_window_border[1]
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
                angle = self.angle + radians(GRAPH_MAX_LINE_ANGLE * 2 / nb_upgrades) * (i - (nb_upgrades - 1) / 2)

            pos = (
                self.pos[0] + GRAPH_LINES_LENGTH * cos(angle) + GRAPH_CIRCLES_RADIUS * cos(self.angle) + GRAPH_CIRCLES_RADIUS * cos(angle),
                self.pos[1] + GRAPH_LINES_LENGTH * sin(angle) + GRAPH_CIRCLES_RADIUS * sin(self.angle) + GRAPH_CIRCLES_RADIUS * sin(angle)
            )
            next_upgrade.set_display_infos(pos, angle, window)

            i += 1

    def set_next_upgrades(self, dico):
        for next_upgrade in dico:
            next_upgrade.set_next_upgrades(dico[next_upgrade])
            self.next.append(next_upgrade)


def draw_forme(forme: str):

    def line(surface, pos_deb, pos_fin, color=(255, 255, 255), width=GRAPH_LINES_WIDTH):
        pygame.draw.line(surface, color, pos_deb, pos_fin, width=width)

    def circle(surface, center, color=(255, 255, 255), radius=GRAPH_CIRCLES_RADIUS, width=GRAPH_CIRCLES_WIDTH):
        pygame.draw.circle(surface, center=center, color=color, radius=radius, width=width)

    formes_functions = {
        'line': line,
        'circle': circle
    }

    return formes_functions[forme]


GRAPH_DICT = {
        Upgrade('1', None): {Upgrade('2', None): {},
                             Upgrade('3', None): {Upgrade('4', None): {Upgrade('4', None): {}}},
                             Upgrade('7', None): {},},

        Upgrade('5', None): {Upgrade('6', None): {Upgrade('6', None): {}}, Upgrade('6', None): {}},
        Upgrade('5', None): {},

    }



if __name__ == '__main__':
    screen = pygame.display.set_mode((1280, 720))

    # Définition des fonctions

    running = True
    posSouris = (0, 0)

    g = Graph(None, {
        Upgrade('1', None): {Upgrade('2', None): {},
                             Upgrade('3', None): {Upgrade('4', None): {Upgrade('4', None): {}}},
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
