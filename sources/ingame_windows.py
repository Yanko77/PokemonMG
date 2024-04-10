"""
Fichier gérant la fenêtre ingame du jeu.
"""

# Importation des modules

import pygame

import starters
import train
import grind
import spawn
import sac
import items
import evolutions


# Définition des classes


class IngameWindow:
    """
    Classe représentant la fenêtre ingame du jeu.
    """

    def __init__(self, game):
        self.game = game

        self.WIDTH = 870
        self.HEIGHT = 488

        # Variables
        self.is_open = False
        self.is_minimized = False

        self.current_panel_name = 'Unknown'
        self.current_panel = None

        # Chargement des images
        self.basic_window = self.img_load('main')
        self.min_window = self.img_load('min_main')
        self.min_window_hover = self.img_load('min_main_hover')

        self.icon = pygame.image.load(f'assets/game/ingame_windows/{self.current_panel_name}/icon.png')

        # Chargement des fonts
        self.title_font = pygame.font.Font('assets/fonts/Impact.ttf', 30)
        self.title = self.title_font.render(self.current_panel_name, False, (0, 0, 0))
        self.min_title_marge = 55
        self.title_marge = 75
        self.title_marges = {
            "Spawn": 75,
            "Train": 70,
            "Grind": 95,
            "Items": 70,
            "Evolutions": 75,
            "Sac d'objets": 105,
            "Starters": 120,
        }

        # Variables relatives au positionnement de la fenetre
        self.basic_window_pos = [-16, 4]
        self.basic_window_rect = pygame.Rect(21, 1, 870, 528)
        self.min_window_rect = pygame.Rect(22, 675, 230, 45)

        self.window_bar_rect = pygame.Rect(21, 1, 870, 39)

        # Variables relatives au déplacement de la fenetre
        self.moving = False
        self.rel_pos = (0, 0)

        # Chargement des boutons
        self.x_button = self.img_load('x_button')
        self.x_button_hover = self.img_load('x_button_hover')
        self.x_button_rect = pygame.Rect(self.basic_window_pos[0] + 854,
                                         self.basic_window_pos[1] + 4,
                                         33,
                                         33)

        self.min_button = self.img_load('min_button')
        self.min_button_hover = self.img_load('min_button_hover')
        self.min_button_rect = pygame.Rect(self.basic_window_pos[0] + 816,
                                           self.basic_window_pos[1] + 4,
                                           33,
                                           33)

        # Chargement des panels
        self.sac_panel = sac.SacIngamePanel(self.game)
        self.spawn_panel = spawn.SpawnPanel(self.game)
        self.train_panel = train.TrainPanel(self.game)
        self.grind_panel = grind.GrindPanel(self.game)
        self.grind_panel.graph.init_graph(self)
        self.items_panel = items.ItemsPanel(self.game)
        self.evol_panel = evolutions.EvolPanel(self.game)

        self.all_panels = {
            "Sac d'objets": self.sac_panel,
            "Spawn": self.spawn_panel,
            "Train": self.train_panel,
            "Grind": self.grind_panel,
            "Items": self.items_panel,
            "Evolutions": self.evol_panel,
        }

    # Méthodes d'affichage

    def update(self, surface, possouris):
        """
        Méthode d'actualisation de l'affichage de la fenêtre ingame.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """
        if self.is_open:
            if self.is_minimized:
                surface.blit(self.min_window, self.min_window_rect)
                surface.blit(self.icon, (self.min_window_rect.x - 20, self.min_window_rect.y + 3))

                if self.current_panel_name == "Sac d'objets":
                    surface.blit(self.title_font.render("Sac", False, (0, 0, 0)),
                                 (self.min_window_rect.x + self.title_marges[self.current_panel_name] - 20,
                                  self.min_window_rect.y))
                else:
                    surface.blit(self.title,
                                 (self.min_window_rect.x + self.title_marges[self.current_panel_name] - 20,
                                  self.min_window_rect.y))

                if self.min_window_rect.collidepoint(possouris):
                    surface.blit(self.min_window_hover, self.min_window_rect)

            else:
                surface.blit(self.basic_window, (self.basic_window_pos[0], self.basic_window_pos[1]))
                surface.blit(self.title,
                             (self.basic_window_pos[0] + self.title_marges[self.current_panel_name],
                              self.basic_window_pos[1]))
                surface.blit(self.icon, self.basic_window_pos)

                # self.update_current_panel(surface, possouris)
                self.current_panel.update(surface, possouris, self)
                self.update_buttons(surface, possouris)

                self.update_window_pos(possouris)

    def update_buttons(self, surface, possouris):
        """
        Fonction qui gère l'affichage des boutons.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """

        # Bouton X
        if self.x_button_rect.collidepoint(possouris):
            surface.blit(self.x_button_hover, self.x_button_rect)
        else:
            surface.blit(self.x_button, self.x_button_rect)

        # Bouton MIN
        if self.min_button_rect.collidepoint(possouris):
            surface.blit(self.min_button_hover, self.min_button_rect)
        else:
            surface.blit(self.min_button, self.min_button_rect)

    # Méthodes liées à la position de la fenêtre ingame

    def update_window_pos(self, possouris):
        """
        Méthode d'actualisation de la position de la fenêtre lorsqu'elle est déplacés par le joueur.

        @in : possouris, list → coordonnées du pointeur de souris
        """
        if not self.moving:
            if self.game.mouse_pressed[1] and self.window_bar_rect.collidepoint(possouris) and not self.is_hovering_buttons(possouris):
                self.moving = True
                self.rel_pos = (possouris[0] - self.basic_window_pos[0],
                                possouris[1] - self.basic_window_pos[1])

        else:
            if not self.game.mouse_pressed[1]:
                self.moving = False
                self.rectif_window_rect()
            else:
                self.basic_window_pos[0], self.basic_window_pos[1] = possouris[0] - self.rel_pos[0], possouris[1] - self.rel_pos[1]
                self.update_all_rects()

    def rectif_window_rect(self):
        """
        Fonction qui rectifie la position de la fenetre si celle-ci n'est pas correcte.
        """

        # Rectification en x
        if self.basic_window_pos[0] < -16:
            self.basic_window_pos[0] = -16
        elif self.basic_window_pos[0] > 386:
            self.basic_window_pos[0] = 386

        # Rectification en y
        if self.basic_window_pos[1] < 4:
            self.basic_window_pos[1] = 4
        elif self.basic_window_pos[1] > 188:
            self.basic_window_pos[1] = 188

        self.update_all_rects()

    def update_all_rects(self):
        """
        Fonction qui modifie tous les rects de la fenetre en fonction de sa position sur l'ecran
        """
        self.basic_window_rect.x, self.basic_window_rect.y = self.basic_window_pos[0]+21, self.basic_window_pos[1]+1
        self.window_bar_rect.x, self.window_bar_rect.y = self.basic_window_pos[0], self.basic_window_pos[1]
        self.x_button_rect.x, self.x_button_rect.y = self.basic_window_pos[0] + 854, self.basic_window_pos[1] + 4
        self.min_button_rect.x, self.min_button_rect.y = self.basic_window_pos[0] + 816, self.basic_window_pos[1] + 4

        self.grind_panel.graph.init_graph(self)

    # Méthode d'actualisation de variables

    def update_panel(self, panel_name):
        """
        Méthode d'actualisation du panel courant de la fenêtre.

        @in : panel_name, str
        """
        self.close()
        self.open()
        self.maximize()

        self.current_panel_name, self.current_panel = panel_name, self.all_panels[panel_name]
        self.title = self.title_font.render(self.current_panel_name, False, (0, 0, 0))
        self.icon = self.icon = pygame.image.load(f'assets/game/ingame_windows/{self.current_panel_name}/icon.png')

    # Méthodes basiques

    def get_width(self):
        return self.WIDTH

    def get_height(self):
        return self.HEIGHT

    def open(self):
        """
        Méthode d'ouverture de la fenêtre ingame
        """
        self.is_open = True

    def close(self):
        """
        Méthode de fermeture de la fenêtre ingame
        """
        self.is_open = False
        self.is_minimized = False

        if self.current_panel is not None:
            self.current_panel.close()

    def minimize(self):
        """
        Méthode de minimisation de la fenêtre ingame
        """
        self.is_minimized = True

    def maximize(self):
        """
        Méthode de maximisation de la fenêtre ingame
        """
        self.is_minimized = False

    def reset_all_panels(self):
        """
        Méthode de réinitialisation de tous les panels de la fenêtre ingame
        """
        for panel in self.all_panels.values():
            panel.reset()

    # Méthodes annexes

    def img_load(self, file_name):
        return pygame.image.load(f'assets/game/ingame_windows/basic/{file_name}.png')

    # Méthodes de gestion d'intéractions

    def is_hovering(self, possouris):
        """
        Méthode qui retourne True si la souris est positionnée sur la fenêtre.

        @in : possouris, list → coordonnées du pointeur de souris
        @out : bool
        """

        if self.is_open:
            if self.is_minimized and self.min_window_rect.collidepoint(possouris):
                return True
            elif not self.is_minimized and self.basic_window_rect.collidepoint(possouris):
                return True
            else:
                return False
        else:
            return False

    def is_hovering_buttons(self, possouris):
        """
        Méthode qui retourne True si la souris est positionnée sur un bouton de la fenêtre.

        @in : possouris, list → coordonnées du pointeur de souris
        @out : bool
        """
        if self.x_button_rect.collidepoint(possouris):
            return True
        elif self.min_button_rect.collidepoint(possouris):
            return True
        else:
            return self.current_panel.is_hovering_buttons(possouris)

    def left_clic_interactions(self, possouris):
        """
        Méthode gérant les intéractions de l'utilisateur avec le clic gauche de la souris.

        @in : possouris, list → coordonnées du pointeur de souris
        """
        if self.is_open:
            if self.is_minimized:
                if self.min_window_rect.collidepoint(possouris):
                    self.maximize()
            else:
                # Bouton X
                if self.x_button_rect.collidepoint(possouris):
                    self.close()

                # Bouton MIN
                elif self.min_button_rect.collidepoint(possouris):
                    self.minimize()

                else:
                    self.current_panel.left_clic_interactions(possouris)

    def right_clic_interactions(self, possouris):
        """
        Méthode gérant les intéractions de l'utilisateur avec le clic droit de la souris.

        @in : possouris, list → coordonnées du pointeur de souris
        """
        self.current_panel.right_clic_interactions(possouris)
