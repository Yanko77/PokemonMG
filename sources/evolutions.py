"""
Fichier gérant le panel d'action "Evol"
"""

# Importation des modules

import pygame

# Définition des classes


class EvolPanel:
    """
    Classe représentant le panel de l'action Evolution.
    Le joueur peut faire évoluer un Pokémon.
    """

    def __init__(self, game):
        self.game = game
        self.PATH = 'assets/game/ingame_windows/Evolutions/'

        self.pokemon_level_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 15)

        self.background = self.img_load('background')
        self.background_pos = (20, -22)

        self.pk_emp = self.img_load('pk_emp')
        self.pk_emp_pos = (152, 125)

        self.evol_button = self.img_load('evol_button')
        self.evol_button_rect = pygame.Rect(462, 287, 138, 140)

        self.evol_button_logo = self.img_load('evol_button_logo')
        self.evol_button_logo_pos = (492, 296)
        self.evol_button_logo_compteur = 19

        # Variables relatives au pokémon à evoluer
        self.evolving_pk = None
        self.evolving_pk_rect = pygame.Rect(160, 133, 284, 284)
        self.mid_evolving_pk_rect = (298, 275)

        self.pk_move_mode = False
        self.moving_pk_rel_possouris = (0, 0)

        # Variables relatives à la fenetre ingame
        self.window_pos = (1, 1)

    # Méthodes d'affichage

    def update(self, surface, possouris, window_pos):
        """
        Méthode d'actualisation de l'affichage du panel.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        @in : window_pos, list → coordonnées de la fenêtre ingame
        """
        if self.window_pos != window_pos:
            self.update_rects(window_pos)

        surface.blit(self.background, (self.background_pos[0] + 20, self.background_pos[1] - 22))

        self.update_evol_button(surface, possouris)
        self.update_pk_emp(surface, possouris)

    def update_evol_pk(self, surface, possouris):
        """
        Methode d'actualisation de l'affichage du pokémon à évoluer.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """
        if self.pk_move_mode:
            pk_rect = pygame.Rect(possouris[0] - self.moving_pk_rel_possouris[0],
                                  possouris[1] - self.moving_pk_rel_possouris[1],
                                  250,
                                  250)
        else:
            pk_rect = self.evolving_pk_rect.copy()

        if self.evolving_pk is not None:

            d = ((152 + self.window_pos[0] - pk_rect.x) ** 2 + (125 + self.window_pos[1] - pk_rect.y) ** 2) ** 0.5

            alpha = 275 + 255 - d * 3
            if alpha < 0:
                alpha = 0

            # Variables
            icon = pygame.transform.scale(self.evolving_pk.icon_image, (500, 250)).convert_alpha()

            # Alpha
            icon.set_alpha(alpha)
            surface.blit(icon, (pk_rect.x + 15, pk_rect.y), (0, 0, 250, 250))

            # Quand on bouge
            bg_rect = self.create_rect_alpha((86, 86), (255, 255, 255), 200 - alpha)

            bg_rect2 = pygame.Surface((98, 98), pygame.SRCALPHA).convert_alpha()
            bg_rect2.set_alpha(220 - alpha)
            pygame.draw.rect(bg_rect2, (0, 0, 0), bg_rect2.get_rect(), width=4)

            icon2 = pygame.transform.scale(self.evolving_pk.icon_image, (220, 110)).convert_alpha()
            level2 = self.pokemon_level_font.render('Lv.' + str(self.evolving_pk.level), False, (0, 0, 0)).convert_alpha()
            back_bar2 = self.create_rect_alpha((55, 6), (35, 35, 35), 255 - alpha)
            front_bar2 = self.create_rect_alpha((self.evolving_pk.health / self.evolving_pk.pv * 55, 6), (42, 214, 0), 255 - alpha)

            icon2.set_alpha(255 - alpha)
            level2.set_alpha(255 - alpha)

            if self.pk_move_mode:
                surface.blit(bg_rect, (possouris[0] - 43, possouris[1] - 43))
                surface.blit(bg_rect2, (possouris[0] - 49, possouris[1] - 49))
                surface.blit(icon2, (possouris[0] - 55, possouris[1] - 65), (0, 0, 100, 100))
                surface.blit(level2, (possouris[0] + 20, possouris[1] + 24))
                surface.blit(back_bar2, (possouris[0] - 40, possouris[1] + 35))
                surface.blit(front_bar2, (possouris[0] - 40, possouris[1] + 35))

            if not self.pk_move_mode:
                if self.game.mouse_pressed[1] and pk_rect.collidepoint(possouris):
                    if not self.game.classic_panel.pk_move_mode:
                        self.pk_move_mode = True
                        self.moving_pk_rel_possouris = (possouris[0] - self.evolving_pk_rect.x,
                                                        possouris[1] - self.evolving_pk_rect.y)
            else:
                if not self.game.mouse_pressed[1]:
                    self.pk_move_mode = False

                    if self.game.classic_panel.PK_RECTS[0].collidepoint(possouris):
                        self.add_pk_to_team(0)
                    elif self.game.classic_panel.PK_RECTS[1].collidepoint(possouris):
                        self.add_pk_to_team(1)
                    elif self.game.classic_panel.PK_RECTS[2].collidepoint(possouris):
                        self.add_pk_to_team(2)
                    elif self.game.classic_panel.PK_RECTS[3].collidepoint(possouris):
                        self.add_pk_to_team(3)
                    elif self.game.classic_panel.PK_RECTS[4].collidepoint(possouris):
                        self.add_pk_to_team(4)
                    elif self.game.classic_panel.PK_RECTS[5].collidepoint(possouris):
                        self.add_pk_to_team(5)

    def update_pk_emp(self, surface, possouris):
        """
        Methode d'actualisation de l'affichage de l'emplacement pokémon à évoluer.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """
        surface.blit(self.pk_emp, self.pk_emp_pos)

        if self.evolving_pk_rect.collidepoint(possouris):
            surface.blit(self.create_rect_alpha((267, 267), (100, 100, 100)), (self.evolving_pk_rect.x + 9,
                                                                               self.evolving_pk_rect.y + 9))

        self.update_evol_pk(surface, possouris)

    def update_evol_button(self, surface, possouris):
        """
        Methode d'actualisation de l'affichage du bouton pour évoluer.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """

        if self.evol_button_rect.collidepoint(possouris):
            surface.blit(self.evol_button, self.evol_button_rect, (138, 0, 138, 140))

            if self.evol_button_logo_compteur >= 3:

                if self.evol_button_logo_compteur <= 19:
                    self.evol_button_logo_compteur -= 2

            surface.blit(self.evol_button_logo, (self.evol_button_logo_pos[0],
                                                 round(self.evol_button_logo_pos[1] + self.evol_button_logo_compteur)))

        else:
            surface.blit(self.evol_button, self.evol_button_rect, (0, 0, 138, 140))

            if self.evol_button_logo_compteur != 19:
                self.evol_button_logo_compteur = 19

    # Méthodes d'actualisation de variables

    def update_evolving_pk(self):
        """
        Methode permettant de changer le pokémon à évoluer du joueur
        """
        if self.evolving_pk is None:
            self.evolving_pk = self.game.player.team[self.game.classic_panel.moving_pk.index(True)]
            self.game.player.team[self.game.classic_panel.moving_pk.index(True)] = None

    def update_rects(self, window_pos: list):
        """
        Methode d'actualisation des positions des rects du panel en fonction de la position de la fenetre ingame.

        @in : window_pos, list → coordonnées de la fenêtre ingame
        """
        self.window_pos = window_pos.copy()

        self.background_pos = self.window_pos.copy()
        self.pk_emp_pos = (152 + self.window_pos[0],
                           125 + self.window_pos[1])
        self.evol_button_rect = pygame.Rect(462 + self.window_pos[0],
                                            287 + self.window_pos[1],
                                            138,
                                            140)
        self.evol_button_logo_pos = (492 + self.window_pos[0],
                                     296 + self.window_pos[1])
        self.evolving_pk_rect = pygame.Rect(160 + self.window_pos[0],
                                            133 + self.window_pos[1],
                                            284,
                                            284)
        self.mid_evolving_pk_rect = (298 + self.window_pos[0],
                                     275 + self.window_pos[1])

    # Méthodes annexes

    def add_pk_to_team(self, team_i):
        """
        Methode qui ajoute un pokémon à l'équipe (redondance avec une méthode de l'objet Player)

        @in : team_i, int → indice du pokémon dans l'équipe.
        """
        if self.game.player.team[team_i] is None:
            self.game.player.team[team_i] = self.evolving_pk
            self.evolving_pk = None

    def create_rect_alpha(self, dimensions, color, alpha=90):
        rect = pygame.Surface(dimensions)
        rect.set_alpha(alpha)
        rect.fill(color)
        return rect

    def img_load(self, file_name):
        return pygame.image.load(f'{self.PATH}{file_name}.png')

    # Méthodes basiques

    def reset(self):
        """
        Méthode de réinitialisation du panel.
        Utilisée lors de l'initialisation d'un nouveau tour de jeu.
        """
        self.evolving_pk = None

    def close(self):
        """
        Méthode classique qui éxécute tout ce qu'il faut faire lorsque le panel est fermé.
        """

        if self.evolving_pk is not None:
            if self.game.player.get_nb_team_members() < 6:
                self.game.player.add_team_pk(self.evolving_pk)
                self.evolving_pk = None

    # Méthodes de gestion d'intéractions

    def left_clic_interactions(self, possouris):
        """
        Méthode gérant les intéractions de l'utilisateur avec le clic gauche de la souris.

        @in : possouris, list → coordonnées du pointeur de souris
        """
        if self.evolving_pk is not None:
            if self.evol_button_rect.collidepoint(possouris):
                if self.evolving_pk.evolution_name != '0':
                    if self.evolving_pk.level >= self.evolving_pk.evolution_level:
                        self.game.notif(f'{self.evolving_pk.name} a évolué !', (0, 0, 0))
                        self.evolving_pk = self.evolving_pk.evolution()
                    else:
                        self.game.notif(f'{self.evolving_pk.name} évolue level {self.evolving_pk.evolution_level}.', (255, 0, 0))
                else:
                    self.game.notif(f"{self.evolving_pk.name} n'a pas d'évolution.", (255, 0, 0))

    def right_clic_interactions(self, posssouris):
        """
        Méthode gérant les intéractions de l'utilisateur avec le clic droit de la souris.

        @in : possouris, list → coordonnées du pointeur de souris
        """
        pass

    def is_hovering_buttons(self, possouris):
        """
        Méthode qui retourne True si la souris est positionnée sur un bouton du panel.

        @in : possouris, list → coordonnées du pointeur de souris
        @out : bool
        """
        if self.pk_move_mode:
            return True
        elif self.evol_button_rect.collidepoint(possouris):
            return True
        elif self.evolving_pk_rect.collidepoint(possouris):
            return True
        else:
            return False
