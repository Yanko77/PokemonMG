"""
Fichier qui gère le panel du sac du joueur.
"""

# Importation des modules

import pygame

# Définition des classes


class SacIngamePanel:
    """
    Classe qui représente le panel de sac du joueur.
    Dans ce panel, le joueur peut accéder à son sac, modifier l'emplacement des objets, les utiliser sur un pokémon,
        les donner à un pokémon...
    """

    def __init__(self, game, window):
        self.game = game
        self.window = window

        self.background1 = pygame.image.load("assets/game/ingame_windows/Sac d'objets/background1.png")
        self.background2 = pygame.image.load("assets/game/ingame_windows/Sac d'objets/background2.png")
        self.emp_hover = pygame.image.load("assets/game/ingame_windows/Sac d'objets/emp_hover.png")
        self.page1_hover = pygame.image.load("assets/game/ingame_windows/Sac d'objets/page1_hover.png")
        self.page2_hover = pygame.image.load("assets/game/ingame_windows/Sac d'objets/page2_hover.png")
        self.page1_rect = pygame.Rect(331, 40, 52, 52)
        self.page2_rect = pygame.Rect(387, 40, 52, 52)

        self.quantite_font = pygame.font.Font('assets/fonts/Impact.ttf', 30)
        self.title_item_font = pygame.font.Font('assets/fonts/Impact.ttf', 45)
        self.desc_item_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 17)
        self.prices_item_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 25)

        self.ALL_EMP_RECT = {
            1: pygame.Rect(463, 46, 100, 100),
            2: pygame.Rect(570, 46, 100, 100),
            3: pygame.Rect(677, 46, 100, 100),
            4: pygame.Rect(784, 46, 100, 100),
            5: pygame.Rect(463, 153, 100, 100),
            6: pygame.Rect(570, 153, 100, 100),
            7: pygame.Rect(677, 153, 100, 100),
            8: pygame.Rect(784, 153, 100, 100),
            9: pygame.Rect(463, 260, 100, 100),
            10: pygame.Rect(570, 260, 100, 100),
            11: pygame.Rect(677, 260, 100, 100),
            12: pygame.Rect(784, 260, 100, 100)
        }

        self.all_emp_rect = {
            1: pygame.Rect(463, 46, 100, 100),
            2: pygame.Rect(570, 46, 100, 100),
            3: pygame.Rect(677, 46, 100, 100),
            4: pygame.Rect(784, 46, 100, 100),
            5: pygame.Rect(463, 153, 100, 100),
            6: pygame.Rect(570, 153, 100, 100),
            7: pygame.Rect(677, 153, 100, 100),
            8: pygame.Rect(784, 153, 100, 100),
            9: pygame.Rect(463, 260, 100, 100),
            10: pygame.Rect(570, 260, 100, 100),
            11: pygame.Rect(677, 260, 100, 100),
            12: pygame.Rect(784, 260, 100, 100)
        }
        self.page = 1
        self.selected_item = None

        self.emp_move_mode = False
        self.emp_moving = [False, False, False, False, False, False, False, False, False, False, False, False]
        self.rel_possouris = [0, 0]
        self.saved_posouris = [0, 0]

    # Méthodes d'affichage

    def update(self, surface, possouris):
        """
        Méthode d'actualisation de l'affichage du panel.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        @in : window_pos, list → coordonnées de la fenêtre ingame
        """
        window_pos = self.window.basic_window_pos

        if self.page == 1:
            surface.blit(self.background1, window_pos)
        elif self.page == 2:
            surface.blit(self.background2, window_pos)

        if pygame.Rect(331+window_pos[0], 40+window_pos[1], 52, 52).collidepoint(possouris):
            surface.blit(self.page1_hover, window_pos)
        elif pygame.Rect(387+window_pos[0], 40+window_pos[1], 52, 52).collidepoint(possouris):
            surface.blit(self.page2_hover, window_pos)

        self.update_rect_pos(window_pos)

        for i in range(1, 13):
            self.update_emp(surface, possouris, i)

        self.update_rect_pos(window_pos)

        if self.selected_item is not None:
            surface.blit(self.title_item_font.render(self.selected_item.name_.upper(), False, (0, 0, 0)),
                         (window_pos[0] + (885-self.title_item_font.render(self.selected_item.name_.upper(), False, (0, 0, 0)).get_rect().w), window_pos[1] + 380))

            surface.blit(self.desc_item_font.render(self.selected_item.description[0], False, (20, 20, 20)),
                         (window_pos[0] + (885-self.desc_item_font.render(self.selected_item.description[0], False, (0, 0, 0)).get_rect().w), window_pos[1] + 430))
            surface.blit(self.desc_item_font.render(self.selected_item.description[1], False, (20, 20, 20)),
                         (window_pos[0] + (885-self.desc_item_font.render(self.selected_item.description[1], False, (0, 0, 0)).get_rect().w), window_pos[1] + 452))
            surface.blit(self.desc_item_font.render(self.selected_item.description[2], False, (20, 20, 20)),
                         (window_pos[0] + (885-self.desc_item_font.render(self.selected_item.description[2], False, (0, 0, 0)).get_rect().w), window_pos[1] + 475))
            surface.blit(pygame.transform.scale(self.selected_item.icon_image, (100, 100)), (window_pos[0] + 405, window_pos[1] + 420))
            if self.selected_item.boolBuy:
                surface.blit(self.prices_item_font.render(str(self.selected_item.buy_price), False, (0, 42, 255)), (window_pos[0]+602, window_pos[1]+493))
            else:
                surface.blit(self.prices_item_font.render(' /', False, (0, 42, 255)),
                             (window_pos[0] + 602, window_pos[1] + 493))

            if self.selected_item.boolSell:
                surface.blit(self.prices_item_font.render(str(self.selected_item.sell_price), False, (204, 0, 0)), (window_pos[0]+784, window_pos[1]+493))
            else:
                surface.blit(self.prices_item_font.render(' /', False, (204, 0, 0)),
                             (window_pos[0] + 784, window_pos[1] + 493))

    def update_emp(self, surface, possouris, i):
        """
        Méthode d'actualisation de l'affichage de l'emplacement d'un objet.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        @in : i, int → indice de l'emplacement (de 1 à 12)
        """

        if self.page == 1:
            sac_i = i - 1
        else:
            sac_i = 11 + i

        if self.game.player.sac[sac_i] is not None:
            if not self.emp_move_mode and not self.emp_moving[i-1]:
                if self.game.mouse_pressed[1] and self.all_emp_rect[i].collidepoint(possouris) and not self.game.classic_panel.ingame_window.moving:
                    self.emp_move_mode = True
                    self.emp_moving[i-1] = True
                    self.rel_possouris = [0, 0]
                    self.saved_posouris = possouris
                    self.selected_item = self.game.player.sac[sac_i]
                elif self.game.mouse_pressed[3] and self.all_emp_rect[i].collidepoint(possouris):
                    self.selected_item = self.game.player.sac[sac_i]

            if self.emp_move_mode and self.emp_moving[i-1]:
                if not self.game.mouse_pressed[1]:
                    if self.page == 1:
                        for n in range(1, 13):
                            if self.all_emp_rect[n].collidepoint(possouris):
                                self.game.player.swap_sac_items(i, n)
                    else:
                        for n in range(13, 25):
                            if self.all_emp_rect[n-12].collidepoint(possouris):
                                self.game.player.swap_sac_items(i+12, n)

                    # Si l'endroit où on relâche le clic est sur l'emplacement d'un pokemon de la team
                    if self.game.classic_panel.current_hover_pokemon is not None:
                        hover_pk = self.game.player.team[self.game.classic_panel.current_hover_pokemon]
                        if hover_pk is not None:
                            if self.selected_item.target_pokemon == 'all' or self.selected_item.target_pokemon == hover_pk.name:
                                if 'Give' in self.selected_item.fonctionnement:
                                    if hover_pk.objet_tenu is None:
                                        hover_pk.give_item(self.selected_item)
                                elif 'Use' in self.selected_item.fonctionnement:
                                    hover_pk.use_item(self.selected_item)

                        if self.selected_item.quantite <= 0:
                            self.game.player.sac[sac_i] = None

                    # Si l'endoit où on relâche le clic est sur l'emplacement pour Enable un item
                    elif self.game.classic_panel.logo_enable_item_rect.collidepoint(possouris):
                        self.selected_item.enable()
                        if self.selected_item.quantite <= 0:
                            self.game.player.sac[sac_i] = None

                    self.emp_move_mode = False
                    self.emp_moving[i-1] = False
                else:
                    self.rel_possouris = (possouris[0] - self.saved_posouris[0], possouris[1] - self.saved_posouris[1])
                    self.all_emp_rect[i].x = self.ALL_EMP_RECT[i].x + self.rel_possouris[0]
                    self.all_emp_rect[i].y = self.ALL_EMP_RECT[i].y + self.rel_possouris[1]

        if self.all_emp_rect[i].collidepoint(possouris):
            surface.blit(self.emp_hover, (self.all_emp_rect[i].x, self.all_emp_rect[i].y))

        if self.page == 2:
            item = self.game.player.sac[i + 11]
        else:
            item = self.game.player.sac[i - 1]

        if item is not None:
            surface.blit(pygame.transform.scale(item.icon_image, (100, 100)), self.all_emp_rect[i])

            # Quantité < 10
            if item.quantite < 10:
                surface.blit(self.quantite_font.render(str(item.quantite), False, (255, 255, 255)),
                             (self.all_emp_rect[i].x + 81, self.all_emp_rect[i].y + 65))
            # Quantité >= 10
            else:
                surface.blit(self.quantite_font.render(str(item.quantite), False, (255, 255, 255)),
                             (self.all_emp_rect[i].x + 68, self.all_emp_rect[i].y + 65))

    def update_rect_pos(self, window_pos):
        """
        Méthode d'actualisation des rects du panel par rapport à la position de la fenêtre ingame.

        @in : window_pos, list → coordonnées de la fenêtre ingame
        """
        self.ALL_EMP_RECT = {
            1: pygame.Rect(463 + window_pos[0], 46 + window_pos[1], 100, 100),
            2: pygame.Rect(570 + window_pos[0], 46 + window_pos[1], 100, 100),
            3: pygame.Rect(677 + window_pos[0], 46 + window_pos[1], 100, 100),
            4: pygame.Rect(784 + window_pos[0], 46 + window_pos[1], 100, 100),
            5: pygame.Rect(463 + window_pos[0], 153 + window_pos[1], 100, 100),
            6: pygame.Rect(570 + window_pos[0], 153 + window_pos[1], 100, 100),
            7: pygame.Rect(677 + window_pos[0], 153 + window_pos[1], 100, 100),
            8: pygame.Rect(784 + window_pos[0], 153 + window_pos[1], 100, 100),
            9: pygame.Rect(463 + window_pos[0], 260 + window_pos[1], 100, 100),
            10: pygame.Rect(570 + window_pos[0], 260 + window_pos[1], 100, 100),
            11: pygame.Rect(677 + window_pos[0], 260 + window_pos[1], 100, 100),
            12: pygame.Rect(784 + window_pos[0], 260 + window_pos[1], 100, 100)
        }
        self.all_emp_rect = {
            1: pygame.Rect(463 + window_pos[0], 46 + window_pos[1], 100, 100),
            2: pygame.Rect(570 + window_pos[0], 46 + window_pos[1], 100, 100),
            3: pygame.Rect(677 + window_pos[0], 46 + window_pos[1], 100, 100),
            4: pygame.Rect(784 + window_pos[0], 46 + window_pos[1], 100, 100),
            5: pygame.Rect(463 + window_pos[0], 153 + window_pos[1], 100, 100),
            6: pygame.Rect(570 + window_pos[0], 153 + window_pos[1], 100, 100),
            7: pygame.Rect(677 + window_pos[0], 153 + window_pos[1], 100, 100),
            8: pygame.Rect(784 + window_pos[0], 153 + window_pos[1], 100, 100),
            9: pygame.Rect(463 + window_pos[0], 260 + window_pos[1], 100, 100),
            10: pygame.Rect(570 + window_pos[0], 260 + window_pos[1], 100, 100),
            11: pygame.Rect(677 + window_pos[0], 260 + window_pos[1], 100, 100),
            12: pygame.Rect(784 + window_pos[0], 260 + window_pos[1], 100, 100)
        }
        self.page1_rect = pygame.Rect(331+window_pos[0], 40+window_pos[1], 52, 52)
        self.page2_rect = pygame.Rect(387+window_pos[0], 40+window_pos[1], 52, 52)

    # Méthodes essentielles

    def change_page(self, num):
        """
        Méthode de changement de page du sac.

        @in : num, int → numéro de la nouvelle page (1 ou 2)
        """
        self.page = num

    # Méthodes basiques

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

    # Méthode de gestion d'intéractions

    def left_clic_interactions(self, possouris):
        """
        Méthode gérant les intéractions de l'utilisateur avec le clic gauche de la souris.

        @in : possouris, list → coordonnées du pointeur de souris
        """
        if self.page1_rect.collidepoint(possouris):
            self.change_page(1)
        elif self.page2_rect.collidepoint(possouris):
            self.change_page(2)

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

        return (self.all_emp_rect[1].collidepoint(possouris) or self.all_emp_rect[2].collidepoint(possouris) or
                self.all_emp_rect[3].collidepoint(possouris) or self.all_emp_rect[4].collidepoint(possouris) or
                self.all_emp_rect[5].collidepoint(possouris) or self.all_emp_rect[6].collidepoint(possouris) or
                self.all_emp_rect[7].collidepoint(possouris) or self.all_emp_rect[8].collidepoint(possouris) or
                self.all_emp_rect[9].collidepoint(possouris) or self.all_emp_rect[10].collidepoint(possouris) or
                self.all_emp_rect[11].collidepoint(possouris) or self.all_emp_rect[12].collidepoint(possouris)
                )
